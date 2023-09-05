from mathutils import Vector
from .TransformFunc import TransformFunc


# Parent-relative -> Bind-pose-relative
def parent_to_bind_translation_vector(positions, bone_transforms):
    bind_pose_translation  = bone_transforms.translation.vector
    inv_bind_pose_rotation = bone_transforms.rotation.matrix3x3_inv
    return [inv_bind_pose_rotation @ (Vector(v[:3]) - bind_pose_translation) for v in positions]

def parent_to_bind_translation_matrix4x4(positions, bone_transforms):
    inv_bind_pose_translation = bone_transforms.translation.matrix4x4_inv
    bind_pose_rotation        = bone_transforms.rotation.matrix4x4
    inv_bind_pose_rotation    = bone_transforms.rotation.matrix4x4_inv
    return [inv_bind_pose_rotation @ p @ inv_bind_pose_translation @ bind_pose_rotation for p in positions]

parent_to_bind_translation = TransformFunc(parent_to_bind_translation_vector,
                                           vector=parent_to_bind_translation_vector,
                                           matrix4x4=parent_to_bind_translation_matrix4x4)

# Bind-pose-relative -> Parent-relative
def bind_to_parent_translation_vector(positions, bone_transforms):
    bind_pose_translation = bone_transforms.translation.vector
    bind_pose_rotation    = bone_transforms.rotation.matrix3x3
    return [(bind_pose_rotation @ Vector(v[:3])) + bind_pose_translation for v in positions]

def bind_to_parent_translation_matrix4x4(positions, bone_transforms):
    bind_pose_translation     = bone_transforms.translation.matrix4x4
    bind_pose_rotation        = bone_transforms.rotation.matrix4x4
    inv_bind_pose_rotation    = bone_transforms.rotation.matrix4x4_inv
    return [bind_pose_rotation @ p @ inv_bind_pose_rotation @ bind_pose_translation for p in positions]

bind_to_parent_translation = TransformFunc(bind_to_parent_translation_vector,
                                           vector=bind_to_parent_translation_vector,
                                           matrix4x4=bind_to_parent_translation_matrix4x4)
