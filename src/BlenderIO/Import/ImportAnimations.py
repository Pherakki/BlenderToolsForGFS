import io
import math

import bpy
from mathutils import Matrix, Quaternion, Vector
import numpy as np

from ...serialization.BinaryTargets import Writer
from ...FileFormats.GFS.SubComponents.Animations import AnimationInterface
from ..Utils.Maths import convert_XDirBone_to_YDirBone, convert_YDirBone_to_XDirBone, convert_Yup_to_Zup, convert_Zup_to_Yup
from .ImportProperties import import_properties

from ..Globals import blenderModelSupportUtils
from ..Globals import GFS_MODEL_TRANSFORMS
from ..modelUtilsTest.Skeleton.Transform.Animation import parent_to_bind, parent_to_bind_blend
from ..modelUtilsTest.Skeleton.Transform.Animation import fix_quaternion_signs
from ..modelUtilsTest.Skeleton.Transform.Animation import create_nla_track


######################
# EXPORTED FUNCTIONS #
######################

def import_animations(gfs, bpy_armature_object, filename, is_external, gfs_to_bpy_bone_map=None):
    if not(len(gfs.animations)) and not(len(gfs.blend_animations)) and gfs.lookat_animations is None:
        return
    
    prev_obj = bpy.context.view_layer.objects.active

    bpy_armature_object.animation_data_create()
    bpy.context.view_layer.objects.active = bpy_armature_object
    
    bpy.ops.object.mode_set(mode="POSE")
    for anim_idx, anim in enumerate(gfs.animations):
        action = add_animation(f"{filename}_{anim_idx}", anim, bpy_armature_object, is_blend=False, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)
                
        if anim.lookat_animations is not None:
            import_lookat_animations(action.GFSTOOLS_AnimationProperties, bpy_armature_object, anim.lookat_animations, f"{filename}_{anim_idx}", gfs_to_bpy_bone_map)

    
    for anim_idx, anim in enumerate(gfs.blend_animations):
        action = add_animation(f"{filename}_blend_{anim_idx}", anim, bpy_armature_object, is_blend=True, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)
        
    ap_props = bpy_armature_object.data.GFSTOOLS_AnimationPackProperties
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
    
    # Lookat Animations
    if gfs.lookat_animations is not None:
        import_lookat_animations(ap_props, bpy_armature_object, gfs.lookat_animations, f"{filename}", gfs_to_bpy_bone_map)
    
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = prev_obj

    # Store animation data
    # Refactor the above when this is the main data management mechanism
    if is_external:
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        ap_props = mprops.external_animation_packs.add()
    else:
        ap_props = mprops.internal_animation_pack
    
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
        bone_name = armature.pose.bones[gfs_to_bpy_bone_map[node_idx]].name #node.name
        build_transformed_fcurves(action, armature, bone_name, 30, {0: node.position}, {0: node.rotation}, {0: node.scale}, {})
    
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


def build_transformed_fcurves(action, armature, bone_name, fps, positions, rotations, scales, fcurve_bank):
    # Set up action data
    actiongroup = action.groups.new(bone_name)
    
    # Get the matrices required to convert animations from GFS -> Blender
    bpy_bone = armature.data.bones[bone_name]
    
    q_rotations = {k: Quaternion([v[3], v[0], v[1], v[2]]) for k, v in rotations.items()}
    
    b_positions, b_rotations, b_scales = parent_to_bind(bpy_bone, positions.values(), q_rotations.values(), scales.values(), GFS_MODEL_TRANSFORMS)
    b_positions = {k: v for k, v in zip(positions.keys(), b_positions)}
    b_rotations = {k: v for k, v in zip(rotations.keys(), b_rotations)}
    b_scales    = {k: v for k, v in zip(scales   .keys(), b_scales   )}
    
    # b_rotations = {k: v for k, v in zip(q_quaternions.keys(), fix_quaternion_signs(q_rotations.values(), b_rotations.values())}
    
    # Create animations
    # This typically takes up ~90% of execution time
    create_fcurves(action, actiongroup, f'pose.bones["{bone_name}"].rotation_quaternion', "BEZIER", fps, b_rotations, [0, 1, 2, 3], fcurve_bank)
    create_fcurves(action, actiongroup, f'pose.bones["{bone_name}"].location',            "LINEAR", fps, b_positions, [0, 1, 2]   , fcurve_bank)
    create_fcurves(action, actiongroup, f'pose.bones["{bone_name}"].scale',               "LINEAR", fps, b_scales,    [0, 1, 2]   , fcurve_bank)


def build_blend_fcurves(action, scale_action, armature, bone_name, fps, positions, rotations, scales, fcurve_bank):
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
    
    # b_rotations = {k: v for k, v in zip(q_quaternions.keys(), fix_quaternion_signs(q_rotations.values(), b_rotations.values())}
    
    # Create animations
    # This typically takes up ~90% of execution time
    create_fcurves(action,       actiongroup,       f'pose.bones["{bone_name}"].rotation_quaternion', "BEZIER", fps, b_rotations, [0, 1, 2, 3], fcurve_bank)
    create_fcurves(action,       actiongroup,       f'pose.bones["{bone_name}"].location',            "LINEAR", fps, b_positions, [0, 1, 2]   , fcurve_bank)
    create_fcurves(scale_action, scale_actiongroup, f'pose.bones["{bone_name}"].scale',               "LINEAR", fps, b_scales,    [0, 1, 2]   , fcurve_bank)

    
def add_animation(track_name, anim, armature, is_blend, gfs_to_bpy_bone_map=None):
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
            build_blend_fcurves(action, scale_action, armature, bone_name, fps, data_track.positions, data_track.rotations, data_track.scales, fcurve_bank)
        else:
            build_transformed_fcurves(action, armature, bone_name, fps, data_track.positions, data_track.rotations, data_track.scales, fcurve_bank)

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
    
    if anim.bounding_box_max_dims is not None:
        props.export_bounding_box = True
        
        # Assumes the world axis rotation is a permutation matrix, which it is
        dims = np.array([anim.bounding_box_max_dims, anim.bounding_box_min_dims])
        dims = dims @ np.array(GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy())
        props.bounding_box_max = np.max(dims, axis=0)
        props.bounding_box_min = np.min(dims, axis=0)        
    else:
        props.export_bounding_box = False
    
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
    ab = ai.to_binary(None)
    
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
    
def import_lookat_animations(props, armature, lookat_animations, anim_name, gfs_to_bpy_bone_map):
    a_r = add_animation(f"{anim_name}_right", lookat_animations.right, armature, is_blend=True, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)
    a_l = add_animation(f"{anim_name}_left",  lookat_animations.left,  armature, is_blend=True, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)
    a_u = add_animation(f"{anim_name}_up",    lookat_animations.up,    armature, is_blend=True, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)
    a_d = add_animation(f"{anim_name}_down",  lookat_animations.down,  armature, is_blend=True, gfs_to_bpy_bone_map=gfs_to_bpy_bone_map)
    
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

