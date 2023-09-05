import math

from .Translation   import parent_to_bind_translation
from .Translation   import bind_to_parent_translation
from .Rotation      import parent_to_bind_rotation
from .Rotation      import bind_to_parent_rotation
from .RotationBlend import parent_to_bind_rotation_blend
from .RotationBlend import bind_to_parent_rotation_blend
from .Scale         import parent_to_bind_scale
from .Scale         import bind_to_parent_scale
from ....TRSTransforms import TRSTransforms


def local_bind_matrix(bpy_bone, model_transforms):
    if bpy_bone.parent is not None:
        # Undo the bone axis rotation to transform the local bind pose from the
        # Blender coordinate system to that of the input data
        pre_transform = model_transforms.bone_axis_permutation.matrix4x4 @ bpy_bone.parent.matrix_local.inverted()
    else:
        # Undo the world rotation to transform the local bind pose from the
        # Blender coordinate system to that of the input data
        pre_transform = model_transforms.world_axis_rotation.matrix4x4_inv
    return pre_transform @ bpy_bone.matrix_local

def local_bind_matrix_transforms(bpy_bone, model_transforms):
    local_bind = local_bind_matrix(bpy_bone, model_transforms)
    t, r, s = local_bind.decompose()
    return TRSTransforms(translation_vector=t, rotation_quat=r)


def fix_quaternion_signs(q_rotations, b_rotations):
    if len(b_rotations) <= 1:
        return b_rotations
    # Fix quaternion signs
    # The furthest two quaternions can be apart is 360 degrees, i.e. q and -q
    # We will detect if a quaternion has inadvertently flipped sign by
    # seeing if neighbouring quaternions are less than or greater than 180
    # degrees apart.
    # If this measurement is different before and after transforming the
    # quaternions, then the quaternion has flipped signs and needs correction.
    q_distances = [((q1.inverted() @ q2).angle < math.pi) for q1, q2 in zip(q_rotations, q_rotations[1:])]
    b_distances = [((q1.inverted() @ q2).angle < math.pi) for q1, q2 in zip(b_rotations, b_rotations[1:])]
    differences = [-2*(b1 ^ b2) + 1 for b1, b2 in zip(q_distances, b_distances)]
    flip_signs = [1]
    for i in range(len(differences)):
        flip_signs.append(differences[i]*flip_signs[i])
    
    return [sgn*v for (v, sgn) in zip(b_rotations, flip_signs)]


def _transform_func(bpy_bone, translations, rotations, scales, model_transforms, 
                    translation_transform, rotation_transform, scale_transform):
    bone_transforms = local_bind_matrix_transforms(bpy_bone, model_transforms)
    b_translations = translation_transform(translations, bone_transforms)
    b_rotations    = rotation_transform   (rotations,    bone_transforms, model_transforms)
    b_scales       = scale_transform      (scales,       model_transforms)
    return b_translations, b_rotations, b_scales


def parent_to_bind(bpy_bone, translations, rotations, scales, model_transforms):
    return _transform_func(bpy_bone, translations, rotations, scales, model_transforms, 
                           parent_to_bind_translation, 
                           parent_to_bind_rotation, 
                           parent_to_bind_scale)


def parent_to_bind_blend(bpy_bone, translations, rotations, scales, model_transforms):
    return _transform_func(bpy_bone, translations, rotations, scales, model_transforms, 
                           parent_to_bind_translation, 
                           parent_to_bind_rotation_blend, 
                           parent_to_bind_scale)


def bind_to_parent(bpy_bone, translations, rotations, scales, model_transforms):
    return _transform_func(bpy_bone, translations, rotations, scales, model_transforms, 
                           bind_to_parent_translation, 
                           bind_to_parent_rotation, 
                           bind_to_parent_scale)


def bind_to_parent_blend(bpy_bone, translations, rotations, scales, model_transforms):
    return _transform_func(bpy_bone, translations, rotations, scales, model_transforms, 
                           bind_to_parent_translation, 
                           bind_to_parent_rotation_blend, 
                           bind_to_parent_scale)
