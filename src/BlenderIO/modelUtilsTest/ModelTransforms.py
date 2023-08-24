import numpy as np
from mathutils import Matrix

basis_vector_lookup_table = {
    'X': np.array([1, 0, 0]),
    '-X': np.array([1, 0, 0]),
    'Y': np.array([0, 1, 0]),
    '-Y': np.array([0, -1, 0]),
    'Z': np.array([0, 0, 1]),
    '-Z': np.array([0, 0, -1])
}

_valid_axis_set = set(('X', 'Y', 'Z'))

class ModelTransforms:
    def __init__(self):
        self._world_rotation                = Matrix.Identity(4)
        self._bone_axis_permutation         = Matrix.Identity(4)
        self._world_rotation_inverse        = Matrix.Identity(4)
        self._bone_axis_permutation_inverse = Matrix.Identity(4)

    @staticmethod
    def create_axis_permutation(right, up, forwards):
        # Validate inputs
        for varname, var in [("right", right), ("up", up), ("forwards", forwards)]:
            if var not in basis_vector_lookup_table:
                valid_keys = list(basis_vector_lookup_table.keys())
                raise ValueError(f"Invalid {varname}-axis '{var}', expected a string in {valid_keys}")
        if set((v[-1] for v in (right, up, forwards))) != _valid_axis_set:
            raise ValueError(f"Cannot construct matrix from degenerate axes '{right}', '{up}', '{forwards}' - inputs must be a (signed) permutation of 'X', 'Y', and 'Z'")
        
        # Create rotation matrix
        out = np.empty((3, 3), dtype=np.float64)
        out[:, 0] = basis_vector_lookup_table[right]
        out[:, 1] = basis_vector_lookup_table[up]
        out[:, 2] = basis_vector_lookup_table[forwards]
        return Matrix(out).to_4x4()

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
