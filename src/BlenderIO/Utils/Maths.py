import mathutils


def decomposableToTRS(matrix, tol=0.001):
    shear_factor = abs(matrix.col[1].dot(matrix.col[2]))
    return shear_factor <= tol
