import io

import bpy
from mathutils import Matrix, Quaternion

from ...serialization.BinaryTargets import Writer
from .Utils.Interpolation import interpolate_keyframe_dict, lerp, slerp


def add_animation(track_name, anim, armature, is_parent_relative):
    action = bpy.data.actions.new(track_name)

    # Base action
    for data_track in anim.node_animations:
        bone_name = data_track.name
        
        actiongroup = action.groups.new(bone_name)


        # position = Matrix.Translation(node.position)
        # rotation = Quaternion([node.rotation[3], *node.rotation[0:3]]).to_matrix().to_4x4()
        # scale = Matrix.Diagonal([*node.scale, 1])
        # base_matrix = position @ rotation @ scale
        
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
        
        frames = sorted(set([
            *list(data_track.rotations.keys()),
            *list(data_track.positions.keys()),
            *list(data_track.scales.keys())
        ]))
        
        # Get rotations
        rotations = {k: v for k, v in data_track.rotations.items()}
        rotation_frames = list(data_track.rotations.keys())
        
        positions = {k: v for k, v in data_track.positions.items()}
        position_frames = list(data_track.positions.keys())
        
        scales = {k: v for k, v in data_track.scales.items()}
        scale_frames = list(data_track.scales.keys())
        
        # Transform the keyframes to rest relative if they're parent relative
        if is_parent_relative:
            if len(rotations) == 0:
                rotations = {0: [0., 0., 0., 1.]}
                rotation_frames = []
            if len(positions) == 0:
                positions = {0: [0., 0., 0.]}
                position_frames = []
            if len(scales) == 0:
                scales = {0: [1., 1., 1.]}
                scale_frames = []
            
            # Now interpolate...
            for frame in frames:
                if frame not in rotations:
                    rotations[frame] = interpolate_keyframe_dict(rotations, frame, slerp)
                if frame not in positions:
                    positions[frame] = interpolate_keyframe_dict(positions, frame, lerp)
                if frame not in scales:
                    scales[frame] = interpolate_keyframe_dict(scales, frame, lerp)
            
            # Now create transform matrices...
            o_rotations = {}
            o_positions = {}
            o_scales    = {}
            for i in frames:
                pos_mat = Matrix.Translation(positions[i])
                rot_mat = Quaternion([rotations[i][3], *rotations[i][0:3]]).to_matrix().to_4x4()
                scl_mat = Matrix.Diagonal([*scales[i], 1])
                transform = base_matrix.inverted() @ (pos_mat @ rot_mat @ scl_mat)
                pos, rot, scl = transform.decompose()
                
                o_rotations[i] = [rot.x, rot.y, rot.z, rot.w]
                o_positions[i] = [pos.x, pos.y, pos.z]
                o_scales[i]    = [scl.x, scl.y, scl.z]
              
            rotations = o_rotations
            positions = o_positions
            scales = o_scales
        else:
            # WRONG but idk how else to import scales at the moment
            # Blend scales are additive...
            # Choices are to import blend scales relative to an animation,
            # or import them relative to 1 and hope for the best
            # Moreover, Blend animations only really "make sense" in the context
            # of another animation. So bake them into an animation..?
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
    track.strips.new(action.name, 1, action)
    armature.animation_data.action = None
    
    return action
    

def import_animations(gfs, armature, filename):
    prev_obj = bpy.context.view_layer.objects.active

    armature.animation_data_create()
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")
    for anim_idx, anim in enumerate(gfs.animations):
        action = add_animation(f"{filename}_{anim_idx}", anim, armature, is_parent_relative=True)
        
        if anim.extra_track is not None:
            action.has_extra_track = True
        
        if anim.lookat_anims.right is not None:
            a_r = add_animation(f"{filename}_{anim_idx}_right", anim.lookat_anims.right, armature, is_parent_relative=False)
            a_l = add_animation(f"{filename}_{anim_idx}_left",  anim.lookat_anims.left,  armature, is_parent_relative=False)
            a_u = add_animation(f"{filename}_{anim_idx}_up",    anim.lookat_anims.up,    armature, is_parent_relative=False)
            a_d = add_animation(f"{filename}_{anim_idx}_down",  anim.lookat_anims.down,  armature, is_parent_relative=False)
            
            a_r.GFSTOOLS_AnimationProperties.is_lookat = True
            a_l.GFSTOOLS_AnimationProperties.is_lookat = True
            a_u.GFSTOOLS_AnimationProperties.is_lookat = True
            a_d.GFSTOOLS_AnimationProperties.is_lookat = True
            
            action.GFSTOOLS_AnimationProperties.has_lookat_anims = True
            action.GFSTOOLS_AnimationProperties.lookat_right = f"{filename}_{anim_idx}_right"
            action.GFSTOOLS_AnimationProperties.lookat_left  = f"{filename}_{anim_idx}_left"
            action.GFSTOOLS_AnimationProperties.lookat_up    = f"{filename}_{anim_idx}_up"
            action.GFSTOOLS_AnimationProperties.lookat_down  = f"{filename}_{anim_idx}_down"
            action.GFSTOOLS_AnimationProperties.lookat_right_factor = anim.lookat_anims.right_factor
            action.GFSTOOLS_AnimationProperties.lookat_left_factor  = anim.lookat_anims.left_factor
            action.GFSTOOLS_AnimationProperties.lookat_up_factor    = anim.lookat_anims.up_factor
            action.GFSTOOLS_AnimationProperties.lookat_down_factor  = anim.lookat_anims.down_factor
            
    for anim_idx, anim in enumerate(gfs.blend_animations):
        action = add_animation(f"{filename}_blend_{anim_idx}", anim, armature, is_parent_relative=False)
        action.is_blend = True
        
    if gfs.lookat_animations is not None:
        a_r = add_animation(f"{filename}_right", gfs.lookat_animations.right, armature, is_parent_relative=False)
        a_l = add_animation(f"{filename}_left",  gfs.lookat_animations.left,  armature, is_parent_relative=False)
        a_u = add_animation(f"{filename}_up",    gfs.lookat_animations.up,    armature, is_parent_relative=False)
        a_d = add_animation(f"{filename}_down",  gfs.lookat_animations.down,  armature, is_parent_relative=False)
        
        a_r.GFSTOOLS_AnimationProperties.is_lookat = True
        a_l.GFSTOOLS_AnimationProperties.is_lookat = True
        a_u.GFSTOOLS_AnimationProperties.is_lookat = True
        a_d.GFSTOOLS_AnimationProperties.is_lookat = True
        
        action.GFSTOOLS_AnimationProperties.has_lookat_anims = True
        action.GFSTOOLS_AnimationProperties.lookat_right = f"{filename}_right"
        action.GFSTOOLS_AnimationProperties.lookat_left  = f"{filename}_left"
        action.GFSTOOLS_AnimationProperties.lookat_up    = f"{filename}_up"
        action.GFSTOOLS_AnimationProperties.lookat_down  = f"{filename}_down"
        action.GFSTOOLS_AnimationProperties.lookat_right_factor = anim.lookat_anims.right_factor
        action.GFSTOOLS_AnimationProperties.lookat_left_factor  = anim.lookat_anims.left_factor
        action.GFSTOOLS_AnimationProperties.lookat_up_factor    = anim.lookat_anims.up_factor
        action.GFSTOOLS_AnimationProperties.lookat_down_factor  = anim.lookat_anims.down_factor
        
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
