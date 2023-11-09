import math

from mathutils import Euler, Matrix, Quaternion

from .Interpolation import interpolate_keyframe_dict, lerp, slerp
from ..Globals import GFS_MODEL_TRANSFORMS

upY_to_upZ_matrix     = GFS_MODEL_TRANSFORMS.world_axis_rotation  .matrix4x4.copy()
boneY_to_boneX_matrix = GFS_MODEL_TRANSFORMS.bone_axis_permutation.matrix4x4.copy()
colY_to_colX_matrix   = GFS_MODEL_TRANSFORMS.world_axis_rotation  .matrix4x4.copy()


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
