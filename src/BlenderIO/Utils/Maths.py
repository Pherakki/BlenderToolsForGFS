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
