from mathutils import Vector

from .TransformFunc import TransformFunc


# Parent-relative -> Bind-pose-relative
def parent_to_bind_scale_vector(scales, model_transforms):
    inv_bone_axis_permutation = model_transforms.bone_axis_permutation.matrix3x3Sq_inv
    return [inv_bone_axis_permutation @ Vector(s[:3]) for s in scales]


def parent_to_bind_scale_matrix3x3(scales, model_transforms):
    ba_inv = model_transforms.bone_axis_permutation.matrix3x3_inv
    ba     = model_transforms.bone_axis_permutation.matrix3x3
    return [ba_inv @ s @ ba for s in scales]


def parent_to_bind_scale_matrix4x4(scales, model_transforms):
    ba_inv = model_transforms.bone_axis_permutation.matrix4x4_inv
    ba     = model_transforms.bone_axis_permutation.matrix4x4
    return [ba_inv @ s @ ba for s in scales]


parent_to_bind_scale = TransformFunc(parent_to_bind_scale_vector,
                                     vector    =parent_to_bind_scale_vector,
                                     matrix3x3=parent_to_bind_scale_matrix3x3,
                                     matrix4x4=parent_to_bind_scale_matrix4x4)


# Bind-pose-relative -> Parent-relative
def bind_to_parent_scale_vector(scales, model_transforms):
    ba = model_transforms.bone_axis_permutation.matrix3x3Sq
    return [ba @ Vector(s[:3]) for s in scales]


def bind_to_parent_scale_matrix3x3(scales, model_transforms):
    ba_inv = model_transforms.bone_axis_permutation.matrix3x3_inv
    ba     = model_transforms.bone_axis_permutation.matrix3x3
    return [ba @ s @ ba_inv for s in scales]


def bind_to_parent_scale_matrix4x4(scales, model_transforms):
    ba_inv = model_transforms.bone_axis_permutation.matrix4x4_inv
    ba     = model_transforms.bone_axis_permutation.matrix4x4
    return [ba @ s @ ba_inv for s in scales]


bind_to_parent_scale = TransformFunc(bind_to_parent_scale_vector,
                                     vector    =bind_to_parent_scale_vector,
                                     matrix3x3=bind_to_parent_scale_matrix3x3,
                                     matrix4x4=bind_to_parent_scale_matrix4x4)
