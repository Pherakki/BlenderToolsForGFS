from mathutils import Quaternion
from .TransformFunc import TransformFunc


# Parent-relative -> Bind-pose-relative
def parent_to_bind_rotation_blend_quaternion(rotations, bone_transforms, model_transforms):
    ba_inv = bone_transforms.rotation.quat_inv
    ba     = bone_transforms.rotation.quat
    return [ba_inv @ Quaternion(v) @ ba for v in rotations]


def parent_to_bind_rotation_blend_matrix3x3(rotations, bone_transforms, model_transforms):
    ba_inv = bone_transforms.rotation.matrix3x3_inv
    ba     = bone_transforms.rotation.matrix3x3
    return [ba_inv @ v @ ba for v in rotations]

def parent_to_bind_rotation_blend_matrix4x4(rotations, bone_transforms, model_transforms):
    ba_inv = bone_transforms.rotation.matrix4x4_inv
    ba     = bone_transforms.rotation.matrix4x4
    return [ba_inv @ v @ ba for v in rotations]


parent_to_bind_rotation_blend = TransformFunc(parent_to_bind_rotation_blend_quaternion,
                                              matrix3x3=parent_to_bind_rotation_blend_matrix3x3,
                                              matrix4x4=parent_to_bind_rotation_blend_matrix4x4,
                                              quat     =parent_to_bind_rotation_blend_quaternion)


# Bind-pose-relative -> Parent-relative
def bind_to_parent_rotation_blend_quaternion(rotations, bone_transforms, model_transforms):
    ba_inv = bone_transforms.rotation.quat_inv
    ba     = bone_transforms.rotation.quat
    return [ba @ Quaternion(v) @ ba_inv for v in rotations]


def bind_to_parent_rotation_blend_matrix3x3(rotations, bone_transforms, model_transforms):
    ba_inv = bone_transforms.rotation.matrix3x3_inv
    ba     = bone_transforms.rotation.matrix3x3
    return [ba @ v @ ba_inv for v in rotations]


def bind_to_parent_rotation_blend_matrix4x4(rotations, bone_transforms, model_transforms):
    ba_inv = bone_transforms.rotation.matrix4x4_inv
    ba     = bone_transforms.rotation.matrix4x4
    return [ba @ v @ ba_inv for v in rotations]


bind_to_parent_rotation_blend = TransformFunc(bind_to_parent_rotation_blend_quaternion,
                                              matrix3x3=bind_to_parent_rotation_blend_matrix3x3,
                                              matrix4x4=bind_to_parent_rotation_blend_matrix4x4,
                                              quat     =bind_to_parent_rotation_blend_quaternion)
