import math

from mathutils import Matrix, Quaternion

from .Interpolation import interpolate_keyframe_dict, lerp, slerp

upY_to_upZ_matrix = Matrix([[ 1.,  0.,  0.,  0.],
                            [ 0.,  0., -1.,  0.],
                            [ 0.,  1.,  0.,  0.],
                            [ 0.,  0.,  0.,  1.]])

boneY_to_boneX_matrix = Matrix([[ 0.,  1.,  0.,  0.],
                                [-1.,  0.,  0.,  0.],
                                [ 0.,  0.,  1.,  0.],
                                [ 0.,  0.,  0.,  1.]])

def convert_XDirBone_to_YDirBone(matrix):
    return matrix @ boneY_to_boneX_matrix

def convert_YDirBone_to_XDirBone(matrix):
    return matrix @ boneY_to_boneX_matrix.inverted()

def convert_Yup_to_Zup(matrix):
    return matrix @ upY_to_upZ_matrix

def convert_Zup_to_Yup(matrix):
    return matrix @ upY_to_upZ_matrix.inverted()

def decomposableToTRS(matrix, tol=0.001):
    shear_factor = abs(matrix.col[1].dot(matrix.col[2]))
    return shear_factor <= tol


def convert_rotation_to_quaternion(rotation_quat, rotation_euler, rotation_mode):
    if rotation_mode == "QUATERNION":
        # pull out quaternion data, normalise
        q = rotation_quat
        mag = sum(e**2 for e in q)
        return Quaternion([e/mag for e in q])
    else:
        x = rotation_euler[0]/2
        y = rotation_euler[1]/2
        z = rotation_euler[2]/2
        
        x_rotation = Quaternion([math.cos(x), math.sin(x),          0.,          0.])
        y_rotation = Quaternion([math.cos(y),          0., math.sin(y),          0.])
        z_rotation = Quaternion([math.cos(z),          0.,          0., math.sin(z)])
        
        # Check which Euler convention to use
        if   rotation_mode == 'XYZ':
            q = x_rotation @ y_rotation @ z_rotation
        elif rotation_mode == 'XZY':
            q = x_rotation @ z_rotation @ y_rotation
        elif rotation_mode == 'YXZ':
            q = y_rotation @ x_rotation @ z_rotation
        elif rotation_mode == 'YZX':
            q = y_rotation @ z_rotation @ x_rotation
        elif rotation_mode == 'ZXY':
            q = z_rotation @ x_rotation @ y_rotation
        elif rotation_mode == 'ZYX':
            q = z_rotation @ y_rotation @ x_rotation
        else:
            raise NotImplementedError("Failed to find rotation mode: THIS SHOULD NEVER HAPPEN")
            
        return q


def transform_node_animations(in_positions, in_rotations, in_scales, base_matrix, bone_transform):
    # Get Transforms
    rotations = {k: v for k, v in in_rotations.items()}
    rotation_frames = list(rotations.keys())
    positions = {k: v for k, v in in_positions.items()}
    position_frames = list(positions.keys())
    scales = {k: v for k, v in in_scales.items()}
    scale_frames = list(scales.keys())
    
    frames = sorted(set([
        *list(rotations.keys()),
        *list(positions.keys()),
        *list(scales.keys())
    ]))
    
    if len(rotations) == 0:
        rotations = {0: [0., 0., 0., 1.]}
    if len(positions) == 0:
        positions = {0: [0., 0., 0.]}
    if len(scales) == 0:
        scales = {0: [1., 1., 1.]}
    
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
        transform =  base_matrix @ bone_transform.inverted() @ (pos_mat @ rot_mat @ scl_mat) @ bone_transform
        pos, rot, scl = transform.decompose()
        
        if i in rotation_frames: o_rotations[i] = [rot.x, rot.y, rot.z, rot.w]
        if i in position_frames: o_positions[i] = [pos.x, pos.y, pos.z]
        if i in scale_frames:    o_scales[i]    = [scl.x, scl.y, scl.z]
      
    return o_positions, o_rotations, o_scales

