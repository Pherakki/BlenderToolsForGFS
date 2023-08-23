from mathutils import Matrix


class ModelTransforms:
    def __init__(self):
        self._world_rotation                = Matrix.Identity(4)
        self._bone_axis_permutation         = Matrix.Identity(4)
        self._world_rotation_inverse        = Matrix.Identity(4)
        self._bone_axis_permutation_inverse = Matrix.Identity(4)

    @property
    def world_axis_rotation(self):
        return self._world_rotation

    @world_axis_rotation.setter
    def world_axis_rotation(self, value):
        self._world_rotation = value
        self._world_rotation_inverse = value.inverted()

    @property
    def world_axis_rotation_inverse(self):
        return self._world_rotation_inverse

    @world_axis_rotation_inverse.setter
    def world_axis_rotation_inverse(self, value):
        self._world_rotation_inverse = value
        self._world_rotation = value.inverted()

    @property
    def bone_axis_permutation(self):
        return self._bone_axis_permutation

    @bone_axis_permutation.setter
    def bone_axis_permutation(self, value):
        self._bone_axis_permutation = value
        self._bone_axis_permutation_inverse = value.inverted()

    @property
    def bone_axis_permutation_inverse(self):
        return self._bone_axis_permutation_inverse

    @bone_axis_permutation_inverse.setter
    def bone_axis_permutation_inverse(self, value):
        self._bone_axis_permutation_inverse = value
        self._bone_axis_permutation = value.inverted()
