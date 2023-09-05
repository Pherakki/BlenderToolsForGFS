import numpy as np
from mathutils import Matrix

from .RotationTransforms import RotationTransforms


class ModelTransforms:
    __slots__ = ("_world_axis_rotation",
                 "_bone_axis_permutation")
    
    def __init__(self, world_axis=None, bone_axis=None):
        self._world_axis_rotation   = RotationTransforms(world_axis)
        self._bone_axis_permutation = RotationTransforms(bone_axis)

    @property
    def world_axis_rotation(self):
        return self._world_axis_rotation
    
    @world_axis_rotation.setter
    def world_axis_rotation(self, value):
        self._world_axis_rotation.set_from_matrix4x4(value)
    
    @property
    def bone_axis_permutation(self):
        return self._bone_axis_permutation
    
    @bone_axis_permutation.setter
    def bone_axis_permutation(self, value):
        self._bone_axis_permutation.set_from_matrix4x4(value)

