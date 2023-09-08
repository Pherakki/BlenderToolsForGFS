import io

from ...serialization.BinaryTargets import Reader
from ...FileFormats.GFS.SubComponents.Animations import AnimationInterface, AnimationBinary
from ...FileFormats.GFS.SubComponents.Animations.Binary.AnimationBinary import EPLEntry

from ..Globals import GFS_MODEL_TRANSFORMS
from ..modelUtilsTest.Skeleton.Transform.Animation import bind_to_parent, bind_to_parent_blend
from ..modelUtilsTest.Skeleton.Transform.Animation.Extract import synchronised_quat_bone_data_from_fcurves
from ..modelUtilsTest.Skeleton.Transform.Animation.Extract import synchronised_quat_object_transforms_from_fcurves
from ..modelUtilsTest.Skeleton.Transform.Animation.Extract import extract_fcurves


def export_animations(gfs, armature, keep_unused_anims):
    if armature.animation_data is not None:
        ap_props = armature.data.GFSTOOLS_AnimationPackProperties
        
        gfs.anim_flag_0  = ap_props.flag_0
        gfs.anim_flag_1  = ap_props.flag_1
        gfs.anim_flag_3  = ap_props.flag_3
        gfs.anim_flag_4  = ap_props.flag_4
        gfs.anim_flag_5  = ap_props.flag_5
        gfs.anim_flag_6  = ap_props.flag_6
        gfs.anim_flag_7  = ap_props.flag_7
        gfs.anim_flag_8  = ap_props.flag_8
        gfs.anim_flag_9  = ap_props.flag_9
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

        for track in armature.animation_data.nla_tracks:
            if track.name == "Rest Pose":
                continue
            if not len(track.strips):
                continue
            action = track.strips[0].action
            if   action.GFSTOOLS_AnimationProperties.category == "NORMAL": export_animation(gfs, armature, gfs.add_animation(),       action, is_blend=False, keep_unused_anims=keep_unused_anims)
            elif action.GFSTOOLS_AnimationProperties.category == "BLEND":  export_animation(gfs, armature, gfs.add_blend_animation(), action, is_blend=True,  keep_unused_anims=keep_unused_anims)
        export_lookat_animations(armature, ap_props, gfs, keep_unused_anims)

def export_lookat_animations(armature, props, gfs_obj, keep_unused_anims):
        if props.has_lookat_anims:
            la_up, la_down, la_left, la_right = gfs_obj.add_lookat_animations(
                props.lookat_up_factor, 
                props.lookat_down_factor, 
                props.lookat_left_factor, 
                props.lookat_right_factor
            )
            
            export_animation(gfs_obj, armature, la_up,    props.lookat_up,    is_blend=True, keep_unused_anims=keep_unused_anims)
            export_animation(gfs_obj, armature, la_down,  props.lookat_down,  is_blend=True, keep_unused_anims=keep_unused_anims)
            export_animation(gfs_obj, armature, la_left,  props.lookat_left,  is_blend=True, keep_unused_anims=keep_unused_anims)
            export_animation(gfs_obj, armature, la_right, props.lookat_right, is_blend=True, keep_unused_anims=keep_unused_anims)


def export_animation(gfs_obj, armature, gfs_anim, action, is_blend, keep_unused_anims):
    # EXPORT NODE ANIMS
    animated_nodes = set()
    node_transforms, root_transform = get_action_data(action, armature, is_blend)
    
    if is_blend:
        # First export the translations and rotations
        node_anims = {}
        for (bidx, bname, t, r, _) in sorted(node_transforms, key=lambda x: x[0]):
            anim = gfs_anim.add_node_animation(bidx, bname)
            anim.positions = t
            anim.rotations = r
            animated_nodes.add(bname)
            node_anims[bname] = anim
        
        if root_transform is not None:
            bidx, bname, t, r, s = root_transform
            root_anim = gfs_anim.add_node_animation(bidx, bname)
            root_anim.positions = t
            root_anim.rotations = r
            animated_nodes.add(bname)
        
        # Now get the scale track
        # The scale track needs to be separated since it's additive, not
        # multiplicative
        if action.GFSTOOLS_AnimationProperties.has_scale_action:
            scale_action = action.GFSTOOLS_AnimationProperties.blend_scale_action
            if scale_action is not None:
                scale_transforms, root_scale = get_action_data(scale_action, armature, is_blend)
                
                for (bidx, bname, _, _, s) in sorted(scale_transforms, key=lambda x: x[0]):
                    node_anim = node_anims.get(bname)
                    if node_anim is None:
                        node_anim = gfs_anim.add_node_animation(bidx, bname)
                    node_anim.scales = s
                    
                if root_transform is not None:
                    root_anim.scales = root_scale[-1]
    else:
        for (bidx, bname, t, r, s) in sorted(node_transforms, key=lambda x: x[0]):
            anim = gfs_anim.add_node_animation(bidx, bname)
            anim.positions = t
            anim.rotations = r
            anim.scales    = s
            animated_nodes.add(bname)
        
        if root_transform is not None:
            bidx, bname, t, r, s = root_transform
            anim = gfs_anim.add_node_animation(bidx, bname)
            anim.positions = t
            anim.rotations = r
            anim.scales    = s
            animated_nodes.add(bname)
    
    # Export extra data
    props = action.GFSTOOLS_AnimationProperties
    gfs_anim.flag_0  = props.flag_0
    gfs_anim.flag_1  = props.flag_1
    gfs_anim.flag_2  = props.flag_2
    gfs_anim.flag_3  = props.flag_3
    gfs_anim.flag_4  = props.flag_4
    gfs_anim.flag_5  = props.flag_5
    gfs_anim.flag_6  = props.flag_6
    gfs_anim.flag_7  = props.flag_7
    gfs_anim.flag_8  = props.flag_8
    gfs_anim.flag_9  = props.flag_9
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
    
    if props.category == "NORMAL":
        export_lookat_animations(armature, props, gfs_anim, keep_unused_anims)
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
    gfs_anim.unknown_animations  = unimported_tracks.unknown_animations
    
    # Bake the speed into the frame times, no sensible way to separate speed and
    # frame times in Blender sadly
    gfs_anim.speed = None
    
    # Create bounding box if required
    if props.export_bounding_box:
        gfs_anim.bounding_box_max_dims = props.bounding_box_max
        gfs_anim.bounding_box_min_dims = props.bounding_box_min
    
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
        if is_blend:
            positions = bone_fcurves[bone_name].get("location", {})
            rotations = bone_fcurves[bone_name].get("rotation_quaternion", {})
            scales    = bone_fcurves[bone_name].get("scale", {})

            g_positions, g_rotations, g_scales = bind_to_parent_blend(bpy_bone, positions.values(), rotations.values(), scales.values(), GFS_MODEL_TRANSFORMS)
            g_positions = {k: v                    for k, v in zip(positions.keys(), g_positions)}
            g_rotations = {k: [q.x, q.y, q.z, q.w] for k, q in zip(rotations.keys(), g_rotations)}
            g_scales    = {k: v                    for k, v in zip(scales.keys(),    g_scales   )}
        else:
            positions = bone_fcurves[bone_name].get("location", {})
            rotations = bone_fcurves[bone_name].get("rotation_quaternion", {})
            scales    = bone_fcurves[bone_name].get("scale", {})
            
            g_positions, g_rotations, g_scales = bind_to_parent(bpy_bone, positions.values(), rotations.values(), scales.values(), GFS_MODEL_TRANSFORMS)
            g_positions = {k: v                    for k, v in zip(positions.keys(), g_positions)}
            g_rotations = {k: [q.x, q.y, q.z, q.w] for k, q in zip(rotations.keys(), g_rotations)}
            g_scales    = {k: v                    for k, v in zip(scales.keys(),    g_scales   )}
            
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
        rotations = {k: [q.x, q.y, q.z, q.w] for k, q in rotations.items()}
        scales    = obj_fcurves.get("scale", {})
    
        fps = 30
        root_animation = ([0, bpy_armature_obj.data.GFSTOOLS_ModelProperties.root_node_name, 
                          {(k-1)/fps : v for k, v in positions.items()}, 
                          {(k-1)/fps : v for k, v in rotations.items()}, 
                          {(k-1)/fps : v for k, v in scales.items()}])
        
    return out, root_animation
