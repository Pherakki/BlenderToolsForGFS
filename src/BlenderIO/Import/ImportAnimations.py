import io
import math

import bpy
from mathutils import Matrix, Quaternion, Vector
import numpy as np

from ...serialization.BinaryTargets import Writer
from ...FileFormats.GFS.SubComponents.Animations import AnimationInterface
from .ImportProperties import import_properties
from ..Preferences import get_preferences
from ..Utils.Animation import gapnames_to_nlatrack

from ..Globals import GFS_MODEL_TRANSFORMS
from ..modelUtilsTest.Skeleton.Transform.Animation import parent_to_bind, parent_to_bind_blend
from ..modelUtilsTest.Skeleton.Transform.Animation import fix_quaternion_signs
from ..modelUtilsTest.Skeleton.Transform.Animation import create_nla_track
from ..modelUtilsTest.Skeleton.Transform.Animation import align_quaternion_signs

######################
# EXPORTED FUNCTIONS #
######################


def import_animations(gfs, bpy_armature_object, filename, is_external, import_policies, gfs_to_bpy_bone_map=None):
    if not is_external and not(len(gfs.animations)) and not(len(gfs.blend_animations)) and gfs.lookat_animations is None:
        return
    
    prev_obj = bpy.context.view_layer.objects.active

    # Refresh animation data
    bpy_armature_object.animation_data_create()
    mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
    active_gap = mprops.get_active_gap()
    if active_gap is not None:
        active_gap.store_animation_pack(bpy_armature_object)
        active_gap.remove_animations_from(bpy_armature_object)
    
    bpy.context.view_layer.objects.active = bpy_armature_object
    
    # Do imports
    ap_props = mprops.animation_packs.add()

    bpy.ops.object.mode_set(mode="POSE")

    if get_preferences().wip_animation_import and get_preferences().developer_mode:
        # Base Animations
        for anim_idx, anim in enumerate(gfs.animations):
            prop_anim_from_gfs_anim(ap_props, filename, "NORMAL", str(anim_idx), anim, bpy_armature_object, False, import_policies, gfs_to_bpy_bone_map)

        # Blend Animations
        for anim_idx, anim in enumerate(gfs.blend_animations):
            prop_anim_from_gfs_anim(ap_props, filename, "BLEND", str(anim_idx), anim, bpy_armature_object, True, import_policies, gfs_to_bpy_bone_map)

        # Lookat Animations
        if gfs.lookat_animations is not None:
            prop_anim_from_gfs_lookat_anims(ap_props, ap_props, filename, "root", gfs.lookat_animations, bpy_armature_object, import_policies, gfs_to_bpy_bone_map)

    else:
        # Base Animations
        for anim_idx, anim in enumerate(gfs.animations):
            action = add_animation(f"{filename}_{anim_idx}", anim, bpy_armature_object, is_blend=False, import_policies=import_policies, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)

            if anim.lookat_animations is not None:
                import_lookat_animations(action.GFSTOOLS_AnimationProperties, bpy_armature_object, anim.lookat_animations, f"{filename}_{anim_idx}", gfs_to_bpy_bone_map, import_policies=import_policies, )

        # Blend Animations
        for anim_idx, anim in enumerate(gfs.blend_animations):
            action = add_animation(f"{filename}_blend_{anim_idx}", anim, bpy_armature_object, is_blend=True, import_policies=import_policies, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)

            if anim.lookat_animations is not None:
                import_lookat_animations(action.GFSTOOLS_AnimationProperties, bpy_armature_object, anim.lookat_animations, f"{filename}_blend_{anim_idx}", gfs_to_bpy_bone_map, import_policies=import_policies, )

        # Lookat Animations
        if gfs.lookat_animations is not None:
            import_lookat_animations(ap_props, bpy_armature_object, gfs.lookat_animations, f"{filename}", gfs_to_bpy_bone_map, import_policies=import_policies)

    ap_props.version = f"0x{gfs.version:0>8x}"
    ap_props.name = filename
    ap_props.flag_0  = gfs.anim_flag_0
    ap_props.flag_1  = gfs.anim_flag_1
    ap_props.flag_3  = gfs.anim_flag_3
    ap_props.flag_4  = gfs.anim_flag_4
    ap_props.flag_5  = gfs.anim_flag_5
    ap_props.flag_6  = gfs.anim_flag_6
    ap_props.flag_7  = gfs.anim_flag_7
    ap_props.flag_8  = gfs.anim_flag_8
    ap_props.flag_9  = gfs.anim_flag_9
    ap_props.flag_10 = gfs.anim_flag_10
    ap_props.flag_11 = gfs.anim_flag_11
    ap_props.flag_12 = gfs.anim_flag_12
    ap_props.flag_13 = gfs.anim_flag_13
    ap_props.flag_14 = gfs.anim_flag_14
    ap_props.flag_15 = gfs.anim_flag_15
    ap_props.flag_16 = gfs.anim_flag_16
    ap_props.flag_17 = gfs.anim_flag_17
    ap_props.flag_18 = gfs.anim_flag_18
    ap_props.flag_19 = gfs.anim_flag_19
    ap_props.flag_20 = gfs.anim_flag_20
    ap_props.flag_21 = gfs.anim_flag_21
    ap_props.flag_22 = gfs.anim_flag_22
    ap_props.flag_23 = gfs.anim_flag_23
    ap_props.flag_24 = gfs.anim_flag_24
    ap_props.flag_25 = gfs.anim_flag_25
    ap_props.flag_26 = gfs.anim_flag_26
    ap_props.flag_27 = gfs.anim_flag_27
    ap_props.flag_28 = gfs.anim_flag_28
    ap_props.flag_29 = gfs.anim_flag_29
    ap_props.flag_30 = gfs.anim_flag_30
    ap_props.flag_31 = gfs.anim_flag_31

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = prev_obj

    # Store animation data
    # Refactor the above when this is the main data management mechanism
    if not is_external:
        mprops.internal_animation_pack_idx = len(mprops.animation_packs) - 1
    mprops.active_animation_pack_idx = len(mprops.animation_packs) - 1
    
    ap_props.store_animation_pack(bpy_armature_object)


def create_rest_pose(gfs, armature, gfs_to_bpy_bone_map):
    prev_obj = bpy.context.view_layer.objects.active
    
    armature.animation_data_create()
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")

    track_name = "Rest Pose"
    action = bpy.data.actions.new(track_name)

    # Base action
    root_name = armature.data.GFSTOOLS_ModelProperties.root_node_name
    for node_idx, node in enumerate(gfs.bones):
        # Special cases
        if node.name == root_name:
            build_object_fcurves(action, armature, 30, {0: node.position}, {0: node.rotation}, {0: node.scale})
            continue
        elif node_idx not in gfs_to_bpy_bone_map:
            continue

        # General bone
        bone_name = armature.pose.bones[gfs_to_bpy_bone_map[node_idx]].name
        build_transformed_fcurves(action, armature, bone_name, 30, {0: node.position}, {0: node.rotation}, {0: node.scale}, {}, False)
    
    armature.animation_data.action = action
    track = armature.animation_data.nla_tracks.new()
    track.name = track_name
    track.mute = False
    track.strips.new(action.name, 1, action) # All actions imported to frame 1
    armature.animation_data.action = None
    
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = prev_obj

#####################
# PRIVATE UTILITIES #
#####################

def create_fcurves(action, actiongroup, fcurve_name, interpolation_method, fps, transforms, transform_indices, fcurve_bank):
    frames = transforms.keys()
    values = transforms.values()
    if len(frames) != 0:
        fcs = []
        for i, t_idx in enumerate(transform_indices):
            key = (fcurve_name, i)
            if key in fcurve_bank:
                action.fcurves.remove(fcurve_bank[key])
            
            # if fcurve_name in action.fcurves:
            #     action.fcurves.remove(action.fcurves[fcurve_name])
            fc = action.fcurves.new(fcurve_name, index=i)
            fc.keyframe_points.add(count=len(frames))
            fc.keyframe_points.foreach_set("co",
                                           [x for co in zip([float(fps*frame + 1) for frame in frames],
                                                            [value[t_idx]         for value in values]) 
                                            for x in co])
            for k in fc.keyframe_points:
                k.interpolation = interpolation_method
            fc.group = actiongroup
            fc.lock = True
            fcs.append(fc)
            fcurve_bank[key] = fc
        for fc in fcs:
            fc.update()
        for fc in fcs:
            fc.lock = False


def build_object_fcurves(action, object, fps, positions, rotations, scales):
    # Set up action data
    actiongroup = action.groups.new("Object Transforms")

    # Create animations
    q_rotations = {k: Quaternion([q[3], q[0], q[1], q[2]]) for k, q in rotations  .items()}
    e_rotations = {k: q.to_euler()                         for k, q in q_rotations.items()}
    create_fcurves(action, actiongroup, 'rotation_quaternion', "BEZIER", fps, q_rotations, [0, 1, 2, 3], {})
    create_fcurves(action, actiongroup, 'rotation_euler',      "LINEAR", fps, e_rotations, [0, 1, 2]   , {})
    create_fcurves(action, actiongroup, 'location',            "LINEAR", fps, positions,   [0, 1, 2]   , {})
    create_fcurves(action, actiongroup, 'scale',               "LINEAR", fps, scales,      [0, 1, 2]   , {})


def build_transformed_fcurves(action, armature, bone_name, fps, positions, rotations, scales, fcurve_bank, align_quats):
    # Set up action data
    actiongroup = action.groups.new(bone_name)
    
    # Get the matrices required to convert animations from GFS -> Blender
    bpy_bone = armature.data.bones[bone_name]
    
    q_rotations = {k: Quaternion([v[3], v[0], v[1], v[2]]) for k, v in rotations.items()}
    
    b_positions, b_rotations, b_scales = parent_to_bind(bpy_bone, positions.values(), q_rotations.values(), scales.values(), GFS_MODEL_TRANSFORMS)
    b_positions = {k: v for k, v in zip(positions.keys(), b_positions)}
    b_rotations = {k: v for k, v in zip(rotations.keys(), b_rotations)}
    b_scales    = {k: v for k, v in zip(scales   .keys(), b_scales   )}
    
    b_rotations = {k: v for k, v in zip(q_rotations.keys(), fix_quaternion_signs(list(q_rotations.values()), list(b_rotations.values())))}
    if align_quats:
        b_rotations = {k: v for k, v in zip(b_rotations.keys(), align_quaternion_signs(list(b_rotations.values())))}
    
    # Create animations
    # This typically takes up ~90% of execution time
    create_fcurves(action, actiongroup, f'pose.bones["{bone_name}"].rotation_quaternion', "BEZIER", fps, b_rotations, [0, 1, 2, 3], fcurve_bank)
    create_fcurves(action, actiongroup, f'pose.bones["{bone_name}"].location',            "LINEAR", fps, b_positions, [0, 1, 2]   , fcurve_bank)
    create_fcurves(action, actiongroup, f'pose.bones["{bone_name}"].scale',               "LINEAR", fps, b_scales,    [0, 1, 2]   , fcurve_bank)


def build_blend_fcurves(action, scale_action, armature, bone_name, fps, positions, rotations, scales, fcurve_bank, align_quats):
    # Set up action data
    actiongroup       = action      .groups.new(bone_name)
    scale_actiongroup = scale_action.groups.new(bone_name)

    # Get the matrices required to convert animations from GFS -> Blender
    bpy_bone = armature.data.bones[bone_name]
    
    q_rotations = {k: Quaternion([v[3], v[0], v[1], v[2]]) for k, v in rotations.items()}

    b_positions, b_rotations, b_scales = parent_to_bind_blend(bpy_bone, positions.values(), q_rotations.values(), scales.values(), GFS_MODEL_TRANSFORMS)
    b_positions = {k: v for k, v in zip(positions.keys(), b_positions)}
    b_rotations = {k: v for k, v in zip(rotations.keys(), b_rotations)}
    b_scales    = {k: v for k, v in zip(scales   .keys(), b_scales   )}
    
    b_rotations = {k: v for k, v in zip(q_rotations.keys(), fix_quaternion_signs(list(q_rotations.values()), list(b_rotations.values())))}
    if align_quats:
        b_rotations = {k: v for k, v in zip(b_rotations.keys(), align_quaternion_signs(list(b_rotations.values())))}
    
    # Create animations
    # This typically takes up ~90% of execution time
    create_fcurves(action,       actiongroup,       f'pose.bones["{bone_name}"].rotation_quaternion', "BEZIER", fps, b_rotations, [0, 1, 2, 3], fcurve_bank)
    create_fcurves(action,       actiongroup,       f'pose.bones["{bone_name}"].location',            "LINEAR", fps, b_positions, [0, 1, 2]   , fcurve_bank)
    create_fcurves(scale_action, scale_actiongroup, f'pose.bones["{bone_name}"].scale',               "LINEAR", fps, b_scales,    [0, 1, 2]   , fcurve_bank)


def prop_anim_from_gfs_anim(ap_props, gap_name, anim_type, anim_name, gfs_anim, bpy_armature_obj, is_blend, import_policies, gfs_to_bpy_bone_map=None):
    ####################
    # SET UP VARIABLES #
    ####################
    if   anim_type == "NORMAL": prop_collection = ap_props.test_anims
    elif anim_type == "BLEND":  prop_collection = ap_props.test_blend_anims
    elif anim_type == "LOOKAT": prop_collection = ap_props.test_lookat_anims
    else:
        raise NotImplementedError(f"CRITICAL INTERNAL ERROR: UNKNOWN ANIM TYPE '{anim_type}'")

    prop_anim = prop_collection.add()
    prop_anim.name = anim_name
    action_name = gapnames_to_nlatrack(gap_name, anim_type, prop_anim.name)

    nodes_action = bpy.data.actions.new(action_name)
    if is_blend:
        scale_action = bpy.data.actions.new(action_name + "_scale")
        scale_action.GFSTOOLS_AnimationProperties.category = "BLENDSCALE"

    bpy_bones = bpy_armature_obj.data.bones
    available_names = {
        (
            bpy_bone.name
            if bpy_bone.GFSTOOLS_NodeProperties.override_name == ""
            else bpy_bone.GFSTOOLS_NodeProperties.override_name
        ): bpy_bone.name
        for bpy_bone in bpy_bones
    }
    root_name = bpy_armature_obj.data.GFSTOOLS_ModelProperties.root_node_name

    #############################################
    # CONSTRUCT ACTION FROM NODE ANIMATION DATA #
    #############################################
    unimported_node_animations = []
    fcurve_bank = {}
    for track_idx, data_track in enumerate(gfs_anim.node_animations):
        if gfs_to_bpy_bone_map is None:
            bone_name = available_names.get(data_track.name)
        else:
            if data_track.id in gfs_to_bpy_bone_map:
                bone_name = bpy_bones[gfs_to_bpy_bone_map[data_track.id]].name
            else:
                bone_name = None

        fps = 30 / (1 if gfs_anim.speed is None else gfs_anim.speed)

        # Special cases
        if bone_name == root_name:
            build_object_fcurves(nodes_action, bpy_armature_obj, fps, data_track.positions, data_track.rotations, data_track.scales)
            continue
        elif bone_name is None or bone_name not in bpy_bones:
            unimported_node_animations.append(track_idx)
            continue

        if is_blend:
            build_blend_fcurves(nodes_action, scale_action, bpy_armature_obj, bone_name, fps, data_track.positions,
                                data_track.rotations, data_track.scales, fcurve_bank, import_policies.align_quats)
        else:
            build_transformed_fcurves(nodes_action, bpy_armature_obj, bone_name, fps, data_track.positions, data_track.rotations,
                                      data_track.scales, fcurve_bank, import_policies.align_quats)

    ##############################################
    # CONSTRUCT THE NODE ANIMATION PROPERTY DATA #
    ##############################################
    # Actions
    if is_blend:
        if len(scale_action.fcurves):
            prop_anim.has_blendscale_animation = True
            prop_anim.blendscale_node_animation.from_action(scale_action)
        else:
            scale_action.user_clear()
            bpy.data.actions.remove(scale_action)
    prop_anim.node_animation.from_action(nodes_action)

    # Flags
    prop_anim.flag_0 = gfs_anim.flag_0
    prop_anim.flag_1 = gfs_anim.flag_1
    prop_anim.flag_2 = gfs_anim.flag_2
    prop_anim.flag_3 = gfs_anim.flag_3
    prop_anim.flag_4 = gfs_anim.flag_4
    prop_anim.flag_5 = gfs_anim.flag_5
    prop_anim.flag_6 = gfs_anim.flag_6
    prop_anim.flag_7 = gfs_anim.flag_7
    prop_anim.flag_8 = gfs_anim.flag_8
    prop_anim.flag_9 = gfs_anim.flag_9
    prop_anim.flag_10 = gfs_anim.flag_10
    prop_anim.flag_11 = gfs_anim.flag_11
    prop_anim.flag_12 = gfs_anim.flag_12
    prop_anim.flag_13 = gfs_anim.flag_13
    prop_anim.flag_14 = gfs_anim.flag_14
    prop_anim.flag_15 = gfs_anim.flag_15
    prop_anim.flag_16 = gfs_anim.flag_16
    prop_anim.flag_17 = gfs_anim.flag_17
    prop_anim.flag_18 = gfs_anim.flag_18
    prop_anim.flag_19 = gfs_anim.flag_19
    prop_anim.flag_20 = gfs_anim.flag_20
    prop_anim.flag_21 = gfs_anim.flag_21
    prop_anim.flag_22 = gfs_anim.flag_22
    prop_anim.flag_24 = gfs_anim.flag_24
    prop_anim.flag_26 = gfs_anim.flag_26
    prop_anim.flag_27 = gfs_anim.flag_27

    # Bounding box
    boxprops = prop_anim.bounding_box
    if import_policies.anim_boundbox_policy == "AUTO":
        default_policy = "AUTO"
    elif import_policies.anim_boundbox_policy == "MANUAL":
        default_policy = "MANUAL"
    else:
        raise NotImplementedError(
            f"CRITICAL INTERNAL ERROR: Unknown ANIM_BOUNDBOX_POLICY '{import_policies.anim_boundbox_policy}'")
    boxprops.export_policy = default_policy if gfs_anim.keep_bounding_box else "NONE"
    if gfs_anim.keep_bounding_box:
        maxd = np.array(
            gfs_anim.overrides.bounding_box.max_dims) @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy()
        mind = np.array(
            gfs_anim.overrides.bounding_box.min_dims) @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy()
        boxprops.max_dims = np.max([maxd, mind], axis=0)
        boxprops.min_dims = np.min([maxd, mind], axis=0)

    prop_anim.category = anim_type

    # Store unimported data as a blob
    ai = AnimationInterface()
    ai.node_animations     = [gfs_anim.node_animations[tidx] for tidx in unimported_node_animations]
    ai.material_animations = gfs_anim.material_animations
    ai.camera_animations   = gfs_anim.camera_animations
    ai.morph_animations    = gfs_anim.morph_animations
    ai.unknown_animations  = gfs_anim.unknown_animations
    ai.extra_track_data    = gfs_anim.extra_track_data
    ab = ai.to_binary(None, None)

    stream = io.BytesIO()
    wtr = Writer(None)
    wtr.bytestream = stream
    wtr.rw_obj(ab, 0x01105100)
    stream.seek(0)
    prop_anim.unimported_tracks = ''.join(f"{elem:0>2X}" for elem in stream.read())

    # Import properties
    import_properties(gfs_anim.properties, prop_anim.properties)

    # Import EPLs
    # Write the EPL to a blob
    for epl_entry in ai.epls:
        stream = io.BytesIO()
        wtr = Writer(None)
        wtr.bytestream = stream
        wtr.rw_obj(epl_entry.binary, 0x01105100)
        stream.seek(0)

        # Add blob
        item = prop_anim.epls.add()
        item.blob = ''.join(f"{elem:0>2X}" for elem in stream.read())

    # LookAt animations
    if gfs_anim.lookat_animations is not None:
        prop_anim_from_gfs_anim(ap_props, prop_anim, gap_name, anim_name + "_" + anim_type, gfs_anim.lookat_animations, bpy_armature_obj, import_animations, gfs_to_bpy_bone_map)


def prop_anim_from_gfs_lookat_anims(ap_props, prop_anim, filename, anim_name, lookat_anims, bpy_armature_object, import_policies, gfs_to_bpy_bone_map):
    anim_right = f"{anim_name}_right"
    anim_left  = f"{anim_name}_left"
    anim_up    = f"{anim_name}_up"
    anim_down  = f"{anim_name}_down"
    prop_anim_from_gfs_anim(ap_props, filename,"LOOKAT", anim_right, lookat_anims.right, bpy_armature_object, True, import_policies, gfs_to_bpy_bone_map)
    prop_anim_from_gfs_anim(ap_props, filename,"LOOKAT", anim_left,  lookat_anims.left,  bpy_armature_object, True, import_policies, gfs_to_bpy_bone_map)
    prop_anim_from_gfs_anim(ap_props, filename,"LOOKAT", anim_up,    lookat_anims.up,    bpy_armature_object, True, import_policies, gfs_to_bpy_bone_map)
    prop_anim_from_gfs_anim(ap_props, filename,"LOOKAT", anim_down,  lookat_anims.down,  bpy_armature_object, True, import_policies, gfs_to_bpy_bone_map)

    prop_anim.has_lookat_anims = True
    prop_anim.test_lookat_right = anim_right
    prop_anim.test_lookat_left  = anim_left
    prop_anim.test_lookat_up    = anim_up
    prop_anim.test_lookat_down  = anim_down
    prop_anim.lookat_right_factor = lookat_anims.right_factor
    prop_anim.lookat_left_factor  = lookat_anims.left_factor
    prop_anim.lookat_up_factor    = lookat_anims.up_factor
    prop_anim.lookat_down_factor  = lookat_anims.down_factor


def add_animation(track_name, anim, armature, is_blend, import_policies, gfs_to_bpy_bone_map=None):
    action = bpy.data.actions.new(track_name)
    if is_blend:    
        scale_action = bpy.data.actions.new(track_name + "_scale")
        scale_action.GFSTOOLS_AnimationProperties.category = "BLENDSCALE"

    # Base action
    # Need to import root node animations here too
    available_names = {
        (
            bpy_bone.name
            if bpy_bone.GFSTOOLS_NodeProperties.override_name == ""
            else bpy_bone.GFSTOOLS_NodeProperties.override_name
        ): bpy_bone.name
        for bpy_bone in armature.data.bones
    }
    root_name = armature.data.GFSTOOLS_ModelProperties.root_node_name

    # Now import the animations
    unimported_node_animations = []
    fcurve_bank = {}
    for track_idx, data_track in enumerate(anim.node_animations):
        if gfs_to_bpy_bone_map is None:
            bone_name = available_names.get(data_track.name)
        else:
            if data_track.id in gfs_to_bpy_bone_map:
                bone_name = armature.data.bones[gfs_to_bpy_bone_map[data_track.id]].name
            else:
                bone_name = None
        
        fps = 30/(1 if anim.speed is None else anim.speed) # Blender has an FPS of 24
        
        # Special cases
        if bone_name == root_name:
            build_object_fcurves(action, armature, fps, data_track.positions, data_track.rotations, data_track.scales)
            continue
        elif bone_name is None or bone_name not in armature.data.bones:
            unimported_node_animations.append(track_idx)
            continue
        
        if is_blend:
            build_blend_fcurves(action, scale_action, armature, bone_name, fps, data_track.positions, data_track.rotations, data_track.scales, fcurve_bank, import_policies.align_quats)
        else:
            build_transformed_fcurves(action, armature, bone_name, fps, data_track.positions, data_track.rotations, data_track.scales, fcurve_bank, import_policies.align_quats)

    if is_blend:
        if len(scale_action.fcurves):  
            create_nla_track(scale_action, armature, "ADD")
            action.GFSTOOLS_AnimationProperties.has_scale_action   = True
            action.GFSTOOLS_AnimationProperties.blend_scale_action = scale_action
        else:
            scale_action.user_clear()
            bpy.data.actions.remove(scale_action)
    create_nla_track(action, armature, "COMBINE" if is_blend else "REPLACE")
    
    # Put extra common data on
    props = action.GFSTOOLS_AnimationProperties
    props.flag_0 = anim.flag_0
    props.flag_1 = anim.flag_1
    props.flag_2 = anim.flag_2
    props.flag_3 = anim.flag_3
    props.flag_4 = anim.flag_4
    props.flag_5 = anim.flag_5
    props.flag_6 = anim.flag_6
    props.flag_7 = anim.flag_7
    props.flag_8 = anim.flag_8
    props.flag_9 = anim.flag_9
    props.flag_10 = anim.flag_10
    props.flag_11 = anim.flag_11
    props.flag_12 = anim.flag_12
    props.flag_13 = anim.flag_13
    props.flag_14 = anim.flag_14
    props.flag_15 = anim.flag_15
    props.flag_16 = anim.flag_16
    props.flag_17 = anim.flag_17
    props.flag_18 = anim.flag_18
    props.flag_19 = anim.flag_19
    props.flag_20 = anim.flag_20
    props.flag_21 = anim.flag_21
    props.flag_22 = anim.flag_22
    props.flag_24 = anim.flag_24
    props.flag_26 = anim.flag_26
    props.flag_27 = anim.flag_27
    
    # Bounding box
    boxprops = props.bounding_box
    if import_policies.anim_boundbox_policy == "AUTO":
        default_policy = "AUTO"
    elif import_policies.anim_boundbox_policy == "MANUAL":
        default_policy = "MANUAL"
    else:
        raise NotImplementedError(f"CRITICAL INTERNAL ERROR: Unknown ANIM_BOUNDBOX_POLICY '{import_policies.anim_boundbox_policy}'")
    boxprops.export_policy = default_policy if anim.keep_bounding_box else "NONE"
    if anim.keep_bounding_box:
        maxd = np.array(anim.overrides.bounding_box.max_dims) @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy()
        mind = np.array(anim.overrides.bounding_box.min_dims) @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy()
        boxprops.max_dims = np.max([maxd, mind], axis=0)
        boxprops.min_dims = np.min([maxd, mind], axis=0)
    
    if is_blend:
        props.category = "BLEND"
    else:
        props.category = "NORMAL"
    
    
    # Store unimported data as a blob
    ai = AnimationInterface()
    ai.node_animations     = [anim.node_animations[tidx] for tidx in unimported_node_animations]
    ai.material_animations = anim.material_animations
    ai.camera_animations   = anim.camera_animations
    ai.morph_animations    = anim.morph_animations
    ai.unknown_animations  = anim.unknown_animations
    ai.extra_track_data    = anim.extra_track_data
    ab = ai.to_binary(None, None)
    
    stream = io.BytesIO()
    wtr = Writer(None)
    wtr.bytestream = stream
    wtr.rw_obj(ab, 0x01105100)
    stream.seek(0)
    props.unimported_tracks = ''.join(f"{elem:0>2X}" for elem in stream.read())
    
    # Import properties
    import_properties(anim.properties, action.GFSTOOLS_AnimationProperties.properties)
    
    # Import EPLs
    props        = action.GFSTOOLS_AnimationProperties
    
    # Write the EPL to a blob
    for epl_entry in ai.epls:
        stream = io.BytesIO()
        wtr = Writer(None)
        wtr.bytestream = stream
        wtr.rw_obj(epl_entry.binary, 0x01105100)
        stream.seek(0)
        
        # Add blob
        item = props.epls.add()
        item.blob = ''.join(f"{elem:0>2X}" for elem in stream.read())

    
    return action
    
def import_lookat_animations(props, armature, lookat_animations, anim_name, gfs_to_bpy_bone_map, import_policies):
    a_r = add_animation(f"{anim_name}_right", lookat_animations.right, armature, is_blend=True, import_policies=import_policies, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)
    a_l = add_animation(f"{anim_name}_left",  lookat_animations.left,  armature, is_blend=True, import_policies=import_policies, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)
    a_u = add_animation(f"{anim_name}_up",    lookat_animations.up,    armature, is_blend=True, import_policies=import_policies, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)
    a_d = add_animation(f"{anim_name}_down",  lookat_animations.down,  armature, is_blend=True, import_policies=import_policies, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)
    
    a_r.GFSTOOLS_AnimationProperties.category = "LOOKAT"
    a_l.GFSTOOLS_AnimationProperties.category = "LOOKAT"
    a_u.GFSTOOLS_AnimationProperties.category = "LOOKAT"
    a_d.GFSTOOLS_AnimationProperties.category = "LOOKAT"
    
    props.has_lookat_anims = True
    props.lookat_right = a_r
    props.lookat_left  = a_l
    props.lookat_up    = a_u
    props.lookat_down  = a_d
    props.lookat_right_factor = lookat_animations.right_factor
    props.lookat_left_factor  = lookat_animations.left_factor
    props.lookat_up_factor    = lookat_animations.up_factor
    props.lookat_down_factor  = lookat_animations.down_factor

