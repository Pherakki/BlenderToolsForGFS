import math

from mathutils import Quaternion


def decomposableToTRS(matrix, tol=0.001):
    shear_factor = abs(matrix.col[1].dot(matrix.col[2]))
    return shear_factor <= tol


def convert_rotation_to_quaternion(rotation_quat, rotation_euler, rotation_mode):
    if rotation_mode == "QUATERNION":
        # pull out quaternion data, normalise
        q = rotation_quat
        mag = sum(e**2 for e in q)
        return Quaternion([e/mag for e in q])
    else:
        x = rotation_euler[0]/2
        y = rotation_euler[1]/2
        z = rotation_euler[2]/2
        
        x_rotation = Quaternion([math.cos(x), math.sin(x),          0.,          0.])
        y_rotation = Quaternion([math.cos(y),          0., math.sin(y),          0.])
        z_rotation = Quaternion([math.cos(z),          0.,          0., math.sin(z)])
        
        # Check which Euler convention to use
        if   rotation_mode == 'XYZ':
            q = x_rotation @ y_rotation @ z_rotation
        elif rotation_mode == 'XZY':
            q = x_rotation @ z_rotation @ y_rotation
        elif rotation_mode == 'YXZ':
            q = y_rotation @ x_rotation @ z_rotation
        elif rotation_mode == 'YZX':
            q = y_rotation @ z_rotation @ x_rotation
        elif rotation_mode == 'ZXY':
            q = z_rotation @ x_rotation @ y_rotation
        elif rotation_mode == 'ZYX':
            q = z_rotation @ y_rotation @ x_rotation
        else:
            raise NotImplementedError("Failed to find rotation mode: THIS SHOULD NEVER HAPPEN")
            
        return q
