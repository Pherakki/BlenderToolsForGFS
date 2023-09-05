import numpy as np
from mathutils import Matrix, Quaternion


basis_vector_lookup_table = {
    'X': np.array([1, 0, 0]),
    '-X': np.array([1, 0, 0]),
    'Y': np.array([0, 1, 0]),
    '-Y': np.array([0, -1, 0]),
    'Z': np.array([0, 0, 1]),
    '-Z': np.array([0, 0, -1])
}


_valid_axis_set = set(('X', 'Y', 'Z'))


def construct_rotation_matrix(initializer):
    if initializer is None:
        return Matrix.Identity(4)
    elif hasattr(initializer, "__iter__") and hasattr(initializer, '__len__'):
        if all(isinstance(e, str) for e in initializer):
            if len(initializer) == 3:
                return create_axis_permutation(*initializer)
            else:
                raise ValueError(f"Received an axis permutation string of length {len(initializer)}, expected length 3")
        else:
            return Matrix(initializer)
    else:
        return Matrix(initializer)


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

def freeze(transforms):
    transforms.matrix4x4.freeze()
    transforms.matrix4x4_inv.freeze()
    transforms.matrix3x3.freeze()
    transforms.matrix3x3_inv.freeze()
    transforms.matrix3x3Sq.freeze()
    transforms.matrix3x3Sq_inv.freeze()
    transforms.quat.freeze()
    transforms.quat_inv.freeze()


class RotationTransforms:
    """
    A class containing multiple pre-computed representations of a rotation to 
    prevent unnecessary work.
    """
    
    __slots__ = ("matrix3x3",   "matrix3x3_inv",
                 "matrix3x3Sq", "matrix3x3Sq_inv",
                 "matrix4x4",   "matrix4x4_inv",
                 "quat",        "quat_inv")
    
    def __init__(self, matrix4x4=None, quat=None):
        if matrix4x4 is not None:
            self.set_from_matrix4x4(construct_rotation_matrix(matrix4x4))
        elif quat is not None:
            self.set_from_quat(quat)
        else:
            self.set_from_matrix4x4(Matrix.Identity(4))
    
    def set_from_quat(self, quat):
        self.quat            = Quaternion(quat)
        self.quat_inv        = self.quat.inverted()
        self.matrix3x3       = self.quat.to_matrix()
        self.matrix3x3_inv   = self.matrix3x3.transposed()
        self.matrix3x3Sq     = Matrix(np.array(self.matrix3x3)**2)
        self.matrix3x3Sq_inv = self.matrix3x3Sq.transposed()
        self.matrix4x4       = self.matrix3x3.to_4x4()
        self.matrix4x4_inv   = self.matrix4x4.transposed()
        freeze(self)
    
    def set_from_matrix4x4(self, matrix4x4):
        self.matrix4x4     = Matrix(matrix4x4)
        self.matrix4x4_inv = self.matrix4x4.transposed()
        self.matrix3x3     = self.matrix4x4.to_3x3()
        self.matrix3x3_inv = self.matrix3x3.transposed()
        self.matrix3x3Sq     = Matrix(np.array(self.matrix3x3)**2)
        self.matrix3x3Sq_inv = self.matrix3x3Sq.transposed()
        self.quat          = self.matrix3x3.to_quaternion()
        self.quat_inv      = self.quat.inverted()
        freeze(self)
