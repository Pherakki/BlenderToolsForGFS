import io

import numpy as np
from mathutils import Quaternion

from ...serialization.BinaryTargets import Reader
from ...FileFormats.GFS.SubComponents.Animations import AnimationInterface, AnimationBinary
from ...FileFormats.GFS.SubComponents.Animations.Binary.AnimationBinary import EPLEntry

from ..Globals import GFS_MODEL_TRANSFORMS
from ..modelUtilsTest.Skeleton.Transform.Animation import bind_to_parent, bind_to_parent_blend
from ..modelUtilsTest.Skeleton.Transform.Animation.Extract import synchronised_quat_bone_data_from_fcurves
from ..modelUtilsTest.Skeleton.Transform.Animation.Extract import synchronised_quat_object_transforms_from_fcurves
from ..modelUtilsTest.Skeleton.Transform.Animation.Extract import extract_fcurves
from ..modelUtilsTest.Skeleton.Transform.Animation import fix_quaternion_signs


def export_gap_props(gfs, bpy_armature_object, ap_props, keep_unused_anims, errorlog):
    mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
    for gap in mprops.animation_packs:
        if gap.is_active:
            gap.update_from_nla(bpy_armature_object)

    gfs.anim_flag_0 = ap_props.flag_0
    gfs.anim_flag_1 = ap_props.flag_1
    gfs.anim_flag_3 = ap_props.flag_3
    gfs.anim_flag_4 = ap_props.flag_4
    gfs.anim_flag_5 = ap_props.flag_5
    gfs.anim_flag_6 = ap_props.flag_6
    gfs.anim_flag_7 = ap_props.flag_7
    gfs.anim_flag_8 = ap_props.flag_8
    gfs.anim_flag_9 = ap_props.flag_9
    gfs.anim_flag_10 = ap_props.flag_10
    gfs.anim_flag_11 = ap_props.flag_11
    gfs.anim_flag_12 = ap_props.flag_12
    gfs.anim_flag_13 = ap_props.flag_13
    gfs.anim_flag_14 = ap_props.flag_14
    gfs.anim_flag_15 = ap_props.flag_15
    gfs.anim_flag_16 = ap_props.flag_16
    gfs.anim_flag_17 = ap_props.flag_17
    gfs.anim_flag_18 = ap_props.flag_18
    gfs.anim_flag_19 = ap_props.flag_19
    gfs.anim_flag_20 = ap_props.flag_20
    gfs.anim_flag_21 = ap_props.flag_21
    gfs.anim_flag_22 = ap_props.flag_22
    gfs.anim_flag_23 = ap_props.flag_23
    gfs.anim_flag_24 = ap_props.flag_24
    gfs.anim_flag_25 = ap_props.flag_25
    gfs.anim_flag_26 = ap_props.flag_26
    gfs.anim_flag_27 = ap_props.flag_27
    gfs.anim_flag_28 = ap_props.flag_28
    gfs.anim_flag_29 = ap_props.flag_29
    gfs.anim_flag_30 = ap_props.flag_30
    gfs.anim_flag_31 = ap_props.flag_31

    lookat_collection = ap_props.test_lookat_anims
    lookat_map        = ap_props.lookat_anims_as_dict()
    for prop_anim in ap_props.test_anims:
        export_prop_to_anim(gfs, gfs.add_animation(), prop_anim, bpy_armature_object, lookat_collection, lookat_map, keep_unused_anims, errorlog, [], extract_base_anim_keyframes)
    for prop_anim in ap_props.test_blend_anims:
        export_prop_to_anim(gfs, gfs.add_animation(), prop_anim, bpy_armature_object, lookat_collection, lookat_map, keep_unused_anims, errorlog, [], extract_blend_anim_keyframes)

    export_prop_lookat_anims(gfs, bpy_armature_object, ap_props, gfs, lookat_collection, lookat_map, keep_unused_anims, errorlog, [])


def remap_track_id(track, names, keep_unused_anims):
    elem_idx = next((i for i, nm in enumerate(names) if track.name == nm), None)
    if elem_idx is None:
        if keep_unused_anims:
            track.id = 0
        else:
            return False
    else:
        track.id = elem_idx
    
    return True


def get_action_data(action, bpy_armature_obj, is_blend):
    bone_names = [b.name for b in bpy_armature_obj.data.bones]
    out = []

    fcurves = extract_fcurves(action)
    bone_fcurves = synchronised_quat_bone_data_from_fcurves(fcurves, bpy_armature_obj.pose.bones)
    obj_fcurves  = synchronised_quat_object_transforms_from_fcurves(fcurves, bpy_armature_obj)
    
    # print(fcurve_groups)
    for bone_name, group in bone_fcurves.items():
        if bone_name not in bpy_armature_obj.pose.bones:
            continue

        bpy_bone = bpy_armature_obj.data.bones[bone_name]
        override_name = bpy_bone.GFSTOOLS_NodeProperties.override_name
        
        positions = bone_fcurves[bone_name].get("location", {})
        rotations = bone_fcurves[bone_name].get("rotation_quaternion", {})
        scales    = bone_fcurves[bone_name].get("scale", {})
        if is_blend: g_positions, g_rotations, g_scales = bind_to_parent_blend(bpy_bone, positions.values(), rotations.values(), scales.values(), GFS_MODEL_TRANSFORMS)
        else:        g_positions, g_rotations, g_scales = bind_to_parent      (bpy_bone, positions.values(), rotations.values(), scales.values(), GFS_MODEL_TRANSFORMS)
        g_positions = {k: v for k, v in zip(positions.keys(), g_positions)}
        g_rotations = {k: q for k, q in zip(rotations.keys(), g_rotations)}
        g_scales    = {k: v for k, v in zip(scales.keys(),    g_scales   )}

        g_rotations = {k: [q.x, q.y, q.z, q.w] for k, q in zip(rotations.keys(), fix_quaternion_signs([Quaternion(q) for q in rotations.values()], list(g_rotations.values())))}
        
        export_name = override_name if override_name != "" else bone_name
        fps = 30
        out.append([bone_names.index(bone_name) + 1, export_name, 
                    {(k-1)/fps : v for k, v in g_positions.items()}, 
                    {(k-1)/fps : v for k, v in g_rotations.items()}, 
                    {(k-1)/fps : v for k, v in g_scales.items()}])

    root_animation = None
    if len(obj_fcurves):
        # Extract animation data
        positions = obj_fcurves.get("location", {})
        rotations = obj_fcurves.get("rotation_quaternion", {})
        rotations = {k: [q[1], q[2], q[3], q[0]] for k, q in rotations.items()}
        scales    = obj_fcurves.get("scale", {})
    
        fps = 30
        root_animation = ([0, bpy_armature_obj.data.GFSTOOLS_ModelProperties.root_node_name, 
                          {(k-1)/fps : v for k, v in positions.items()}, 
                          {(k-1)/fps : v for k, v in rotations.items()}, 
                          {(k-1)/fps : v for k, v in scales.items()}])
        
    return out, root_animation


def export_prop_to_anim(gfs_obj, gfs_anim, prop_anim, bpy_armature_object, lookat_collection, lookat_map, keep_unused_anims, errorlog, lookat_stack, extractor):
    if len(prop_anim.node_animation.strips) or prop_anim.has_blendscale_animation:
        animated_nodes = extractor(gfs_anim, prop_anim, bpy_armature_object)
    else:
        animated_nodes = set()
    init_gfs_anim_properties(gfs_obj, gfs_anim, prop_anim, animated_nodes, keep_unused_anims)
    export_prop_lookat_anims(gfs_obj, bpy_armature_object, prop_anim, gfs_anim, lookat_collection, lookat_map, keep_unused_anims, errorlog, lookat_stack)


def export_prop_lookat_anims(gfs_obj, bpy_armature_object, prop_anim, lookat_holder, lookat_collection, lookat_map, keep_unused_anims, errorlog, lookat_stack):
    if prop_anim.has_lookat_anims:
        la_up, la_down, la_left, la_right = lookat_holder.add_lookat_animations(
            prop_anim.lookat_up_factor,
            prop_anim.lookat_down_factor,
            prop_anim.lookat_left_factor,
            prop_anim.lookat_right_factor
        )

        for lookat_dir, prop_lookat_id, gfs_lookat in [("up",    "test_lookat_up",    la_up),
                                                       ("down",  "test_lookat_down",  la_down),
                                                       ("left",  "test_lookat_left",  la_left),
                                                       ("right", "test_lookat_right", la_right)]:
            prop_lookat_name = getattr(prop_anim, prop_lookat_id)
            idx = lookat_map.get(prop_lookat_name)
            if idx is not None:
                prop_lookat = lookat_collection[idx]
                new_lookat_stack = [*lookat_stack, prop_lookat.name]
                if prop_lookat.name in lookat_stack:
                    errorlog.log_error_message(f"Circular LookAt detected: '->'.join({new_lookat_stack})")
                    return
                export_prop_to_anim(gfs_obj, gfs_lookat, prop_lookat, bpy_armature_object, lookat_collection, lookat_map, keep_unused_anims, errorlog, new_lookat_stack, extract_blend_anim_keyframes)
            else:
                errorlog.log_warning_message(f"'{prop_anim.name}'s '{lookat_dir}' LookAt animation '{prop_lookat_name}' does not exist. An empty animation has been exported in its place.")


def extract_base_anim_keyframes(gfs_anim, prop_anim, bpy_armature_object):
    # Node Animations
    animated_nodes = set()

    # Iterate over strips...
    action = prop_anim.node_animation.strips[0].action
    node_transforms, root_transform = get_action_data(action, bpy_armature_object, False)

    for (bidx, bname, t, r, s) in sorted(node_transforms, key=lambda x: x[0]):
        anim = gfs_anim.add_node_animation(bidx, bname)
        anim.positions = t
        anim.rotations = r
        anim.scales = s
        animated_nodes.add(bname)

    if root_transform is not None:
        bidx, bname, t, r, s = root_transform
        anim = gfs_anim.add_node_animation(bidx, bname)
        anim.positions = t
        anim.rotations = r
        anim.scales = s
        animated_nodes.add(bname)

    return animated_nodes


def extract_blend_anim_keyframes(gfs_anim, prop_anim, bpy_armature_object):
    # Node Animations
    animated_nodes = set()

    full_node_transforms = {}
    full_root_transform  = None
    if prop_anim.has_node_animation:
        # Iterate over strips...
        action = prop_anim.node_animation.strips[0].action
        node_transforms, root_transform = get_action_data(action, bpy_armature_object, True)

        for (bidx, bname, t, r, _) in sorted(node_transforms, key=lambda x: x[0]):
            full_node_transforms[bidx] = [bname, t, r, []]
        full_root_transform = root_transform

    if prop_anim.has_blendscale_animation:
        # Iterate over strips...
        action = prop_anim.blendscale_node_animation.strips[0].action
        node_transforms, root_transform = get_action_data(action, bpy_armature_object, True)

        for (bidx, bname, _, _, s) in sorted(node_transforms, key=lambda x: x[0]):
            if bidx in full_node_transforms:
                full_node_transforms[bidx][3] = s
            else:
                full_node_transforms[bidx] = [bname, [], [], s]

        if full_root_transform is None:
            full_root_transform = root_transform
        elif root_transform is not None:
            full_root_transform[4] = root_transform[4]

    for bidx, (bname, t, r, s) in full_node_transforms.items():
        anim = gfs_anim.add_node_animation(bidx, bname)
        anim.positions = t
        anim.rotations = r
        anim.scales    = s
        animated_nodes.add(bname)

    if full_root_transform is not None:
        bidx, bname, t, r, s = full_root_transform
        anim = gfs_anim.add_node_animation(bidx, bname)
        anim.positions = t
        anim.rotations = r
        anim.scales = s
        animated_nodes.add(bname)

    return animated_nodes


def init_gfs_anim_properties(gfs_obj, gfs_anim, props, animated_nodes, keep_unused_anims):
    # Export extra data
    gfs_anim.flag_0 = props.flag_0
    gfs_anim.flag_1 = props.flag_1
    gfs_anim.flag_2 = props.flag_2
    gfs_anim.flag_3 = props.flag_3
    gfs_anim.flag_4 = props.flag_4
    gfs_anim.flag_5 = props.flag_5
    gfs_anim.flag_6 = props.flag_6
    gfs_anim.flag_7 = props.flag_7
    gfs_anim.flag_8 = props.flag_8
    gfs_anim.flag_9 = props.flag_9
    gfs_anim.flag_10 = props.flag_10
    gfs_anim.flag_11 = props.flag_11
    gfs_anim.flag_12 = props.flag_12
    gfs_anim.flag_13 = props.flag_13
    gfs_anim.flag_14 = props.flag_14
    gfs_anim.flag_15 = props.flag_15
    gfs_anim.flag_16 = props.flag_16
    gfs_anim.flag_17 = props.flag_17
    gfs_anim.flag_18 = props.flag_18
    gfs_anim.flag_19 = props.flag_19
    gfs_anim.flag_20 = props.flag_20
    gfs_anim.flag_21 = props.flag_21
    gfs_anim.flag_22 = props.flag_22
    gfs_anim.flag_24 = props.flag_24
    gfs_anim.flag_26 = props.flag_26
    gfs_anim.flag_27 = props.flag_27

    # Export extra track + other data
    unimported_tracks = AnimationInterface()
    if len(props.unimported_tracks):
        stream = io.BytesIO()
        stream.write(bytes.fromhex(props.unimported_tracks))
        stream.seek(0)
        rdr = Reader(None)
        rdr.bytestream = stream
        ab = AnimationBinary()
        rdr.rw_obj(ab, 0x01105100)
        unimported_tracks = AnimationInterface.from_binary(ab)

    gfs_anim.extra_track_data = unimported_tracks.extra_track_data

    # Export unused bone animations
    bone_names = [b.name for b in gfs_obj.bones]
    for track in unimported_tracks.node_animations:
        if track.name not in animated_nodes:
            if remap_track_id(track, bone_names, keep_unused_anims):
                gfs_anim.node_animations.append(track)

    # Export unused material animations
    material_names = [m.name for m in gfs_obj.materials]
    for track in unimported_tracks.material_animations:
        if remap_track_id(track, material_names, keep_unused_anims):
            gfs_anim.material_animations.append(track)

    # Export unused camera animations
    camera_names = [bone_names[cam.node] for cam in gfs_obj.cameras]
    for track in unimported_tracks.camera_animations:
        if remap_track_id(track, camera_names, keep_unused_anims):
            gfs_anim.camera_animations.append(track)

    # Export unused morph animations
    morph_names = [bone_names[mesh.node] for mesh in gfs_obj.meshes if len(mesh.morphs)]
    for track in unimported_tracks.morph_animations:
        if remap_track_id(track, morph_names, keep_unused_anims):
            gfs_anim.morph_animations.append(track)

    # Absolutely no idea what these are. Better not do anything important...
    gfs_anim.unknown_animations = unimported_tracks.unknown_animations

    # Bake the speed into the frame times, no sensible way to separate speed and
    # frame times in Blender sadly
    gfs_anim.speed = None

    # Create bounding box if required
    gfs_anim.keep_bounding_box = props.bounding_box.export_policy != "NONE"
    if props.bounding_box.export_policy == "MANUAL":
        dims = np.array([props.bounding_box.max_dims, props.bounding_box.min_dims])
        dims = dims @ np.array(GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3.copy())
        gfs_anim.overrides.bounding_box.max_dims = np.max(dims, axis=0)
        gfs_anim.overrides.bounding_box.min_dims = np.min(dims, axis=0)
        gfs_anim.overrides.bounding_box.enabled = True

    # Export the custom properties
    for prop in props.properties:
        gfs_anim.add_property(*prop.extract_data(prop))

    # Export bone epls
    for epl_prop in props.epls:
        stream = io.BytesIO()
        stream.write(bytes.fromhex(epl_prop.blob))
        stream.seek(0)
        rdr = Reader(None)
        rdr.bytestream = stream
        epl_entry = EPLEntry(endianness=">")
        rdr.rw_obj(epl_entry, 0x01105100)

        gfs_anim.epls.append(epl_entry)
