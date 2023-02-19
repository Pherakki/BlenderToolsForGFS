import io

import bpy
from mathutils import Matrix, Quaternion

from ...serialization.BinaryTargets import Writer
from ...FileFormats.GFS.SubComponents.Animations import AnimationInterface
from ..Utils.Maths import transform_node_animations, convert_XDirBone_to_YDirBone, convert_YDirBone_to_XDirBone, convert_Yup_to_Zup, convert_Zup_to_Yup
from .ImportProperties import import_properties


######################
# EXPORTED FUNCTIONS #
######################

def import_animations(gfs, armature, filename):
    prev_obj = bpy.context.view_layer.objects.active

    armature.animation_data_create()
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")
    actions = []
    for anim_idx, anim in enumerate(gfs.animations):
        action = add_animation(f"{filename}_{anim_idx}", anim, armature, is_blend=False)
    
        if anim.lookat_animations is not None:
            import_lookat_animations(action.GFSTOOLS_AnimationProperties, armature, anim.lookat_animations, f"{filename}_{anim_idx}")

        actions.append(action)
            
    for anim_idx, anim in enumerate(gfs.blend_animations):
        action = add_animation(f"{filename}_blend_{anim_idx}", anim, armature, is_blend=True)
        
    ap_props = armature.data.GFSTOOLS_AnimationPackProperties
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
        import_lookat_animations(ap_props, armature, gfs.lookat_animations, f"{filename}")
        
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = prev_obj


def create_rest_pose(gfs, armature, gfs_to_bpy_bone_map):
    prev_obj = bpy.context.view_layer.objects.active
    
    armature.animation_data_create()
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")

    track_name = "Rest Pose"
    action = bpy.data.actions.new(track_name)

    # Base action
    for node_idx, node in enumerate(gfs.bones):
        if node_idx not in gfs_to_bpy_bone_map:
            continue

        bone_name = armature.pose.bones[gfs_to_bpy_bone_map[node_idx]].name #node.name
        build_transformed_fcurves(action, armature, bone_name, {0: node.position}, {0: node.rotation}, {0: node.scale})
    
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

def create_fcurves(action, actiongroup, fcurve_name, interpolation_method, fps, transforms, transform_indices):
    frames = transforms.keys()
    values = transforms.values()
    if len(frames) != 0:
        fcs = []
        for i, t_idx in enumerate(transform_indices):
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
        for fc in fcs:
            fc.update()
        for fc in fcs:
            fc.lock = False
            
def build_transformed_fcurves(action, armature, bone_name, positions, rotations, scales):
    actiongroup = action.groups.new(bone_name)

    fps = 30

    bpy_bone = armature.data.bones[bone_name]
    if bpy_bone.parent is not None:
        parent_matrix = convert_YDirBone_to_XDirBone(bpy_bone.parent.matrix_local).inverted() 
        local_bind_matrix = parent_matrix @ bpy_bone.matrix_local
    else:
        local_bind_matrix = convert_Zup_to_Yup(bpy_bone.matrix_local)
    
    positions, rotations, scales = transform_node_animations(positions, rotations, scales, local_bind_matrix.inverted(), convert_XDirBone_to_YDirBone)
  
    # Create animations
    create_fcurves(action, actiongroup, f'pose.bones["{bone_name}"].rotation_quaternion', "BEZIER", fps, rotations, [3, 0, 1, 2])
    create_fcurves(action, actiongroup, f'pose.bones["{bone_name}"].location',            "LINEAR", fps, positions, [0, 1, 2]   )
    create_fcurves(action, actiongroup, f'pose.bones["{bone_name}"].scale',               "LINEAR", fps, scales,    [0, 1, 2]   )

def build_blend_fcurves(action, scale_action, armature, bone_name, positions, rotations, scales):
    actiongroup       = action      .groups.new(bone_name)
    scale_actiongroup = scale_action.groups.new(bone_name)

    fps = 30
    
    prematrix = convert_YDirBone_to_XDirBone(Matrix.Identity(4))
    postmatrix = convert_XDirBone_to_YDirBone
    positions, _        , _      = transform_node_animations(positions,         {0: [0., 0., 0., 1.]}, {0: [1., 1., 1.]}, prematrix, postmatrix)
    _        , rotations, _      = transform_node_animations({0: [0., 0., 0.]}, rotations,             {0: [1., 1., 1.]}, prematrix, postmatrix)
    _        , _        , scales = transform_node_animations({0: [0., 0., 0.]}, {0: [0., 0., 0., 1.]}, scales,            prematrix, postmatrix)

    # Create animations
    create_fcurves(action,       actiongroup,       f'pose.bones["{bone_name}"].rotation_quaternion', "BEZIER", fps, rotations, [3, 0, 1, 2])
    create_fcurves(action,       actiongroup,       f'pose.bones["{bone_name}"].location',            "LINEAR", fps, positions, [0, 1, 2]   )
    create_fcurves(scale_action, scale_actiongroup, f'pose.bones["{bone_name}"].scale',               "LINEAR", fps, scales,    [0, 1, 2]   )
    
    
def build_track(action, armature, blend_type, speed=None):
    armature.animation_data.action = action
    track = armature.animation_data.nla_tracks.new()
    track.name = action.name
    track.mute = True
    strip = track.strips.new(action.name, 1, action)
    strip.blend_type = blend_type
    if speed is not None:
        strip.scale = 1 / speed
    armature.animation_data.action = None
    
def add_animation(track_name, anim, armature, is_blend):
    action = bpy.data.actions.new(track_name)
    if is_blend:    
        scale_action = bpy.data.actions.new(track_name + "_scale")
        scale_action.GFSTOOLS_AnimationProperties.category = "BLENDSCALE"

    # Base action
    # Need to import root node animations here too
    unimported_node_animations = []
    for track_idx, data_track in enumerate(anim.node_animations):
        bone_name = data_track.name
        
        #if bone_name == armature.GFSTOOLS_ModelProperties.root_node_name:
        #    continue
        if bone_name not in armature.data.bones:
            unimported_node_animations.append(track_idx)
            continue
        
        if is_blend:
            build_blend_fcurves(action, scale_action, armature, bone_name, data_track.positions, data_track.rotations, data_track.scales)
        else:
            build_transformed_fcurves(action, armature, bone_name, data_track.positions, data_track.rotations, data_track.scales)

    if is_blend:    
        if len(scale_action.fcurves):  
            build_track(scale_action, armature, "ADD", anim.speed)
            action.GFSTOOLS_AnimationProperties.has_scale_action   = True
            action.GFSTOOLS_AnimationProperties.blend_scale_action = scale_action.name
        else:
            scale_action.user_clear()
    build_track(action, armature, "COMBINE" if is_blend else "REPLACE", anim.speed)
    
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
    
    return action
    
def import_lookat_animations(props, armature, lookat_animations, anim_name):
    a_r = add_animation(f"{anim_name}_right", lookat_animations.right, armature, is_blend=True)
    a_l = add_animation(f"{anim_name}_left",  lookat_animations.left,  armature, is_blend=True)
    a_u = add_animation(f"{anim_name}_up",    lookat_animations.up,    armature, is_blend=True)
    a_d = add_animation(f"{anim_name}_down",  lookat_animations.down,  armature, is_blend=True)
    
    a_r.GFSTOOLS_AnimationProperties.category = "LOOKAT"
    a_l.GFSTOOLS_AnimationProperties.category = "LOOKAT"
    a_u.GFSTOOLS_AnimationProperties.category = "LOOKAT"
    a_d.GFSTOOLS_AnimationProperties.category = "LOOKAT"
    
    props.has_lookat_anims = True
    props.lookat_right = f"{anim_name}_right"
    props.lookat_left  = f"{anim_name}_left"
    props.lookat_up    = f"{anim_name}_up"
    props.lookat_down  = f"{anim_name}_down"
    props.lookat_right_factor = lookat_animations.right_factor
    props.lookat_left_factor  = lookat_animations.left_factor
    props.lookat_up_factor    = lookat_animations.up_factor
    props.lookat_down_factor  = lookat_animations.down_factor
    
# def import_object_transforms(action, position, rotation, scale):
    
