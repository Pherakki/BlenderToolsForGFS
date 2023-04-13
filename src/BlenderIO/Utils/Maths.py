import math

from mathutils import Euler, Matrix, Quaternion

from .Interpolation import interpolate_keyframe_dict, lerp, slerp

upY_to_upZ_matrix = Matrix([[ 1.,  0.,  0.,  0.],
                            [ 0.,  0., -1.,  0.],
                            [ 0.,  1.,  0.,  0.],
                            [ 0.,  0.,  0.,  1.]])

boneY_to_boneX_matrix = Matrix([[ 0.,  1.,  0.,  0.],
                                [-1.,  0.,  0.,  0.],
                                [ 0.,  0.,  1.,  0.],
                                [ 0.,  0.,  0.,  1.]])

colY_to_colX_matrix = Matrix([[ 1.,  0.,  0.,  0.],
                              [ 0.,  0., -1.,  0.],
                              [ 0.,  1.,  0.,  0.],
                              [ 0.,  0.,  0.,  1.]])

# boneY_to_boneX_matrix = Matrix.Identity(4)
# upY_to_upZ_matrix = Matrix.Identity(4)

def convert_XDirBone_to_YDirBone(matrix):
    return matrix @ boneY_to_boneX_matrix

def convert_YDirBone_to_XDirBone(matrix):
    return matrix @ boneY_to_boneX_matrix.inverted()

def convert_Yup_to_Zup(matrix):
    return upY_to_upZ_matrix @ matrix

def convert_Zup_to_Yup(matrix):
    return upY_to_upZ_matrix.inverted() @ matrix

def MayaBoneToBlenderBone(matrix):
    return convert_Yup_to_Zup(convert_XDirBone_to_YDirBone(matrix))

def BlenderBoneToMayaBone(matrix):
    return convert_YDirBone_to_XDirBone(convert_Zup_to_Yup(matrix))

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
        return Euler(rotation_euler, rotation_mode).to_quaternion()


def left_transform(v, inv_transform):
    return inv_transform @ v


def right_transform(v, transform):
    return v @ transform


def conjugate_transform(v, transform, inv_transform):
    return inv_transform @ v @ transform


def transform_node_animations(in_positions, in_rotations, in_scales, base_matrix, axis_conversion):
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
        transform = base_matrix @ axis_conversion(pos_mat @ rot_mat @ scl_mat)
        pos, rot, scl = transform.decompose()
        
        if i in rotation_frames: o_rotations[i] = [rot.x, rot.y, rot.z, rot.w]
        if i in position_frames: o_positions[i] = [pos.x, pos.y, pos.z]
        if i in scale_frames:    o_scales[i]    = [scl.x, scl.y, scl.z]
      
    return o_positions, o_rotations, o_scales

