import io

import bpy
from mathutils import Matrix, Quaternion

from ...serialization.BinaryTargets import Writer
from ...FileFormats.GFS.SubComponents.Animations import AnimationInterface
from ..Utils.Interpolation import interpolate_keyframe_dict, lerp, slerp
from ..Utils.Maths import transform_node_animations
from .ImportProperties import import_properties


def add_animation(track_name, anim, armature, is_parent_relative):
    action = bpy.data.actions.new(track_name)

    # Base action
    for data_track in anim.node_animations:
        bone_name = data_track.name
        
        actiongroup = action.groups.new(bone_name)

        if bone_name not in armature.data.bones:
            # Throw an error here?
            # Just import with reference to a unit matrix?
            continue
        bpy_bone = armature.data.bones[bone_name]
        if bpy_bone.parent is not None:
            base_matrix = bpy_bone.parent.matrix_local.inverted() @ bpy_bone.matrix_local
        else:
            base_matrix = bpy_bone.matrix_local

        
        fps = 30
        
        rotations = {k: v for k, v in data_track.rotations.items()}
        rotation_frames = list(data_track.rotations.keys())
        
        positions = {k: v for k, v in data_track.positions.items()}
        position_frames = list(data_track.positions.keys())
        
        scales = {k: v for k, v in data_track.scales.items()}
        scale_frames = list(data_track.scales.keys())
        
        # Transform the keyframes to rest relative if they're parent relative
        if is_parent_relative:
            positions, rotations, scales = transform_node_animations(data_track.positions, data_track.rotations, data_track.scales, base_matrix.inverted())
        else:
            # Import scales as a separate addition track later
            scales = {k : [1 + vi for vi in v] for k, v in scales.items()}
          
        # Create animations
        if len(rotation_frames) != 0:
            fcs = []
            for i, quat_idx in enumerate([3, 0, 1, 2]):
                fc = action.fcurves.new(f'pose.bones["{bone_name}"].rotation_quaternion', index=i)
                fc.keyframe_points.add(count=len(rotation_frames))
                fc.keyframe_points.foreach_set("co",
                                               [x for co in zip([float(fps*frame + 1) for frame in rotation_frames],
                                                                [rotations[frame][quat_idx] for frame in rotation_frames]) for x in
                                                co])
                fc.group = actiongroup
                fc.lock = True
                fcs.append(fc)
            for fc in fcs:
                fc.update()
            for fc in fcs:
                fc.lock = False
                

        if len(position_frames) != 0:
            fcs = []
            for i in range(3):
                fc = action.fcurves.new(f'pose.bones["{bone_name}"].location', index=i)
                fc.keyframe_points.add(count=len(position_frames))
                fc.keyframe_points.foreach_set("co",
                                                [x for co in zip([float(fps*frame + 1) for frame in position_frames],
                                                                [positions[frame][i] for frame in position_frames]) for x in
                                                co])
                fc.group = actiongroup
                for k in fc.keyframe_points:
                    k.interpolation = "LINEAR"
                fc.lock = True
                fcs.append(fc)
            for fc in fcs:
                fc.update()
            for fc in fcs:
                fc.lock = False
                

        if len(scale_frames) != 0:
            fcs = []
            for i in range(3):
                fc = action.fcurves.new(f'pose.bones["{bone_name}"].scale', index=i)
                fc.keyframe_points.add(count=len(scale_frames))
                fc.keyframe_points.foreach_set("co",
                                               [x for co in zip([float(fps*frame + 1) for frame in scale_frames],
                                                                [scales[frame][i] for frame in scale_frames]) for x in
                                                co])
                fc.group = actiongroup
                for k in fc.keyframe_points:
                    k.interpolation = "LINEAR"
                fc.lock = True
                fcs.append(fc)
            for fc in fcs:
                fc.update()
            for fc in fcs:
                fc.lock = False

    armature.animation_data.action = action
    track = armature.animation_data.nla_tracks.new()
    track.name = track_name
    track.mute = True
    strip = track.strips.new(action.name, 1, action)
    if anim.speed is not None:
        strip.scale = 1 / anim.speed
    armature.animation_data.action = None
    
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
    
    props.category = "NORMAL"
    
    
    # Store unimported data as a blob
    ai = AnimationInterface()
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
    

def import_animations(gfs, armature, filename):
    prev_obj = bpy.context.view_layer.objects.active

    armature.animation_data_create()
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")
    actions = []
    for anim_idx, anim in enumerate(gfs.animations):
        action = add_animation(f"{filename}_{anim_idx}", anim, armature, is_parent_relative=True)
    
        if anim.lookat_animations is not None:
            a_r = add_animation(f"{filename}_{anim_idx}_right", anim.lookat_animations.right, armature, is_parent_relative=False)
            a_l = add_animation(f"{filename}_{anim_idx}_left",  anim.lookat_animations.left,  armature, is_parent_relative=False)
            a_u = add_animation(f"{filename}_{anim_idx}_up",    anim.lookat_animations.up,    armature, is_parent_relative=False)
            a_d = add_animation(f"{filename}_{anim_idx}_down",  anim.lookat_animations.down,  armature, is_parent_relative=False)
            
            a_r.GFSTOOLS_AnimationProperties.category = "LOOKAT"
            a_l.GFSTOOLS_AnimationProperties.category = "LOOKAT"
            a_u.GFSTOOLS_AnimationProperties.category = "LOOKAT"
            a_d.GFSTOOLS_AnimationProperties.category = "LOOKAT"
            
            action.GFSTOOLS_AnimationProperties.has_lookat_anims = True
            action.GFSTOOLS_AnimationProperties.lookat_right = f"{filename}_{anim_idx}_right"
            action.GFSTOOLS_AnimationProperties.lookat_left  = f"{filename}_{anim_idx}_left"
            action.GFSTOOLS_AnimationProperties.lookat_up    = f"{filename}_{anim_idx}_up"
            action.GFSTOOLS_AnimationProperties.lookat_down  = f"{filename}_{anim_idx}_down"
            action.GFSTOOLS_AnimationProperties.lookat_right_factor = anim.lookat_animations.right_factor
            action.GFSTOOLS_AnimationProperties.lookat_left_factor  = anim.lookat_animations.left_factor
            action.GFSTOOLS_AnimationProperties.lookat_up_factor    = anim.lookat_animations.up_factor
            action.GFSTOOLS_AnimationProperties.lookat_down_factor  = anim.lookat_animations.down_factor
        
        actions.append(action)
            
    for anim_idx, anim in enumerate(gfs.blend_animations):
        action = add_animation(f"{filename}_blend_{anim_idx}", anim, armature, is_parent_relative=False)
        action.GFSTOOLS_AnimationProperties.category = "BLEND"
        
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
        ap_props.has_lookat_anims = True
        a_r = add_animation(f"{filename}_right", gfs.lookat_animations.right, armature, is_parent_relative=False)
        a_l = add_animation(f"{filename}_left",  gfs.lookat_animations.left,  armature, is_parent_relative=False)
        a_u = add_animation(f"{filename}_up",    gfs.lookat_animations.up,    armature, is_parent_relative=False)
        a_d = add_animation(f"{filename}_down",  gfs.lookat_animations.down,  armature, is_parent_relative=False)
        
        a_r.GFSTOOLS_AnimationProperties.category = "LOOKAT"
        a_l.GFSTOOLS_AnimationProperties.category = "LOOKAT"
        a_u.GFSTOOLS_AnimationProperties.category = "LOOKAT"
        a_d.GFSTOOLS_AnimationProperties.category = "LOOKAT"
        
        ap_props.has_lookat_anims = True
        ap_props.lookat_right = f"{filename}_right"
        ap_props.lookat_left  = f"{filename}_left"
        ap_props.lookat_up    = f"{filename}_up"
        ap_props.lookat_down  = f"{filename}_down"
        ap_props.lookat_right_factor = gfs.lookat_animations.right_factor
        ap_props.lookat_left_factor  = gfs.lookat_animations.left_factor
        ap_props.lookat_up_factor    = gfs.lookat_animations.up_factor
        ap_props.lookat_down_factor  = gfs.lookat_animations.down_factor
        
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = prev_obj
    
    # IMPORT ALL DATA AS A BINARY
    if len(gfs.animations):
        stream = io.BytesIO()
        wtr = Writer(None)
        wtr.bytestream = stream
        ab = gfs.animation_data
        wtr.rw_obj(ab, 0x01105100)
        stream.seek(0)
        
        armature[f"{filename}_animations"] = "0x" + ''.join(f"{elem:0>2X}" for elem in stream.read())



def create_rest_pose(gfs, armature, gfs_to_bpy_bone_map):
    prev_obj = bpy.context.view_layer.objects.active
    
    armature.animation_data_create()
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")

    track_name = "Rest Pose"
    action = bpy.data.actions.new(track_name)

    #rest_transforms = [None]*len()
    bind_matrices = [Matrix([b.bind_pose_matrix[0:4],
                             b.bind_pose_matrix[4:8],
                             b.bind_pose_matrix[8:12],
                             [0., 0., 0., 1.]]) for b in gfs.bones]
    
    # Base action
    for node_idx, node in enumerate(gfs.bones):
        if node_idx not in gfs_to_bpy_bone_map:
            continue
        
        bone_name = armature.pose.bones[gfs_to_bpy_bone_map[node_idx]].name #node.name
        
        actiongroup = action.groups.new(bone_name)


        parent_bind_matrix = bind_matrices[node.parent_idx] if node.parent_idx > -1 else Matrix.Identity(4)
        local_bind_matrix = parent_bind_matrix.inverted() @ bind_matrices[node_idx]
                
        rest_position = Matrix.Translation(node.position)
        rest_rotation = Quaternion([node.rotation[3], *node.rotation[0:3]]).to_matrix().to_4x4()
        rest_scale    = Matrix.Diagonal([*node.scale, 1])
        rest_matrix   = rest_position @ rest_rotation @ rest_scale
        
        pos, quat, scale = (rest_matrix @ local_bind_matrix.inverted()).decompose()
        position = [pos.x, pos.y, pos.z]
        rotation = [quat.x, quat.y, quat.z, quat.w]
        scale    = [scale.x, scale.y, scale.z]
          
        # Create animations
        fcs = []
        for i, quat_idx in enumerate([3, 0, 1, 2]):
            fc = action.fcurves.new(f'pose.bones["{bone_name}"].rotation_quaternion', index=i)
            fc.keyframe_points.add(count=1)
            fc.keyframe_points.foreach_set("co", [1, rotation[quat_idx]])
            fc.group = actiongroup
            fc.lock = True
            fcs.append(fc)
        for fc in fcs:
            fc.update()
        for fc in fcs:
            fc.lock = False
            
        fcs = []
        for i in range(3):
            fc = action.fcurves.new(f'pose.bones["{bone_name}"].location', index=i)
            fc.keyframe_points.add(count=1)
            fc.keyframe_points.foreach_set("co", [1, position[i]])
            fc.group = actiongroup
            for k in fc.keyframe_points:
                k.interpolation = "LINEAR"
            fc.lock = True
            fcs.append(fc)
        for fc in fcs:
            fc.update()
        for fc in fcs:
            fc.lock = False
        
        fcs = []
        for i in range(3):
            fc = action.fcurves.new(f'pose.bones["{bone_name}"].scale', index=i)
            fc.keyframe_points.add(count=1)
            fc.keyframe_points.foreach_set("co", [1, scale[i]])
            fc.group = actiongroup
            for k in fc.keyframe_points:
                k.interpolation = "LINEAR"
            fc.lock = True
            fcs.append(fc)
        for fc in fcs:
            fc.update()
        for fc in fcs:
            fc.lock = False

    armature.animation_data.action = action
    track = armature.animation_data.nla_tracks.new()
    track.name = track_name
    track.mute = True
    track.strips.new(action.name, 1, action) # All actions imported to frame 1
    armature.animation_data.action = None
    
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = prev_obj
