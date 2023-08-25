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
    __slots__ = ("_world_rotation", "_world_rotation_inverse",
                 "_bone_axis_permutation", "_bone_axis_permutation_inverse")
    
    def __init__(self, world_axis=None, bone_axis=None):
        self.world_axis_rotation   = self._construct_rotation_matrix(world_axis)
        self.bone_axis_permutation = self._construct_rotation_matrix(bone_axis)

    def _construct_rotation_matrix(self, initializer):
        if initializer is None:
            return Matrix.Identity(4)
        elif hasattr(initializer, "__iter__") and hasattr(initializer, '__len__'):
            if all(isinstance(e, str) for e in initializer):
                if len(initializer) == 3:
                    return self.create_axis_permutation(*initializer)
                else:
                    raise ValueError(f"Received an axis permutation string of length {len(initializer)}, expected length 3")
            else:
                return Matrix(initializer)
        else:
            return Matrix(initializer)

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
