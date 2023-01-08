import io

import bpy
from mathutils import Matrix, Quaternion

from ...serialization.BinaryTargets import Writer
from .Utils.Interpolation import interpolate_keyframe_dict, lerp, slerp


def import_animations(gfs, model_gfs, armature, filename):
    prev_obj = bpy.context.view_layer.objects.active

    armature.animation_data_create()
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")
    for anim_idx, anim in enumerate(gfs.animations):
        track_name = f"{filename}_{anim_idx}"
        action = bpy.data.actions.new(track_name)

        track_database = {track.name: track for track in anim.tracks}
        # Base action
        for node in model_gfs.bones:
            bone_name = node.name
            
            actiongroup = action.groups.new(bone_name)


            position = Matrix.Translation(node.position)
            rotation = Quaternion([node.rotation[3], *node.rotation[0:3]]).to_matrix().to_4x4()
            scale = Matrix.Diagonal([*node.scale, 1])
            base_matrix = position @ rotation @ scale
            
            if node.name not in track_database:
                continue
            data_track = track_database[node.name]
            
            fps = 30
            
            frames = sorted(set([
                *list(data_track.rotations.keys()),
                *list(data_track.positions.keys()),
                *list(data_track.scales.keys())
            ]))
            
            # Get rotations
            if node.name in track_database:
                rotations = {k: v for k, v in track_database[node.name].rotations.items()}
                rotation_frames = list(track_database[node.name].rotations.keys())
                
                base_pos  = track_database[node.name].base_position
                positions = {k: [bv*bp for bv, bp in zip(v, base_pos)] for k, v in track_database[node.name].positions.items()}
                position_frames = list(track_database[node.name].positions.keys())
                
                base_scale = track_database[node.name].base_scale
                scales = {k: [bv*bp for bv, bp in zip(v, base_scale)] for k, v in track_database[node.name].scales.items()}
                scale_frames = list(track_database[node.name].scales.keys())
                
                if len(rotations) == 0:
                    rotations = {0: [0., 0., 0., 1.]}
                    rotation_frames = []
                if len(positions) == 0:
                    positions = {0: [0., 0., 0.]}
                    position_frames = []
                if len(scales) == 0:
                    scales = {0: [1., 1., 1.]}
                    scale_frames = []
            else:
                rotations = {0: [0., 0., 0., 1.]}
                positions = {0: [0., 0., 0.]}
                scales    = {0: [1., 1., 1.]}
                rotation_frames = []
                position_frames = []
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
        
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = prev_obj
    
    # IMPORT ALL DATA AS A BINARY
    if len(gfs.animations):
        string_data = '0x'
        for anim in gfs.animations:
            ab = anim.to_binary()
            
            stream = io.BytesIO()
            wtr = Writer(None)
            wtr.bytestream = stream
            wtr.rw_obj(ab, 0x01105100)
            stream.seek(0)
            
            string_data += "||" + ''.join(f"{elem:0>2X}" for elem in stream.read())
        armature["animations"] = string_data



def create_rest_pose(armature, nodes, bind_matrices):
    prev_obj = bpy.context.view_layer.objects.active
    
    armature.animation_data_create()
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")

    track_name = "rest_pose"
    action = bpy.data.actions.new(track_name)

    # Base action
    for (node, bind_matrix) in zip(nodes, bind_matrices):
        bone_name = node.name
        
        actiongroup = action.groups.new(bone_name)


        parent_bind_matrix = bind_matrices[node.parent] if node.parent > -1 else Matrix.Identity(4)
        local_bind_matrix = parent_bind_matrix.inverted() @ bind_matrix
                
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
