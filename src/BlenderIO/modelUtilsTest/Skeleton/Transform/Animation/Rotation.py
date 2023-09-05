from mathutils import Quaternion
from .TransformFunc import TransformFunc


# Parent-relative -> Bind-pose-relative
def parent_to_bind_rotation_quaternion(rotations, bone_transforms, model_transforms):
    inv_bind_pose_rot     = bone_transforms.rotation.quat_inv
    bone_axis_permutation = model_transforms.bone_axis_permutation.quat
    return [inv_bind_pose_rot @ Quaternion(v) @ bone_axis_permutation for v in rotations]


def parent_to_bind_rotation_matrix3x3(rotations, bone_transforms, model_transforms):
    inv_bind_pose_rot = bone_transforms.rotation.matrix3x3_inv
    bone_axis_permutation  = model_transforms.bone_axis_permutation.matrix3x3
    return [inv_bind_pose_rot @ v @ bone_axis_permutation for v in rotations]


def parent_to_bind_rotation_matrix4x4(rotations, bone_transforms, model_transforms):
    inv_bind_pose_rot = bone_transforms.rotation.matrix4x4_inv
    bone_axis_permutation  = model_transforms.bone_axis_permutation.matrix4x4
    return [inv_bind_pose_rot @ v @ bone_axis_permutation for v in rotations]


parent_to_bind_rotation = TransformFunc(parent_to_bind_rotation_quaternion,
                                        matrix3x3=parent_to_bind_rotation_matrix3x3,
                                        matrix4x4=parent_to_bind_rotation_matrix4x4,
                                        quat     =parent_to_bind_rotation_quaternion)


# Bind-pose-relative -> Parent-relative
def bind_to_parent_rotation_quaternion(rotations, bone_transforms, model_transforms):
    bind_pose_rotation        = bone_transforms.rotation.quat
    inv_bone_axis_permutation = model_transforms.bone_axis_permuation.quat_inv
    return [bind_pose_rotation @ Quaternion(v) @ inv_bone_axis_permutation for v in rotations]


def bind_to_parent_rotation_matrix3x3(rotations, bone_transforms, model_transforms):
    bind_pose_rotation        = bone_transforms.rotation.matrix3x3
    inv_bone_axis_permutation = model_transforms.bone_axis_permuation.matrix3x3_inv
    return [bind_pose_rotation @ v @ inv_bone_axis_permutation for v in rotations]


def bind_to_parent_rotation_matrix4x4(rotations, bone_transforms, model_transforms):
    bind_pose_rotation        = bone_transforms.rotation.matrix4x4
    inv_bone_axis_permutation = model_transforms.bone_axis_permuation.matrix4x4_inv
    return [bind_pose_rotation @ v @ inv_bone_axis_permutation for v in rotations]


bind_to_parent_rotation = TransformFunc(bind_to_parent_rotation_quaternion,
                                        matrix3x3=bind_to_parent_rotation_matrix3x3,
                                        matrix4x4=bind_to_parent_rotation_matrix4x4,
                                        quat     =bind_to_parent_rotation_quaternion)
