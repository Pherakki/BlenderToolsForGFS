from mathutils import Quaternion, Euler, Vector


EULER_MODES = set(('XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'))


def is_euler(rotation_mode):
    return rotation_mode in EULER_MODES


def decompose_axisangle(rotation_axis_angle):
    angle = rotation_axis_angle[0]
    axis = Vector(rotation_axis_angle[1:4])
    return axis, angle


def quat_to_euler(rotation_quat, rotation_mode):
    return Quaternion(rotation_quat).to_euler(rotation_mode)


def quat_to_axisangle(rotation_quat):
    return rotation_quat.to_axis_angle()


def euler_to_quat(rotation_euler, rotation_mode):
    return Euler(rotation_euler, rotation_mode).to_quaternion()


def euler_to_axisangle(rotation_euler, rotation_mode):
    return quat_to_axisangle(euler_to_quat(rotation_euler, rotation_mode))


def axisangle_to_quat(axis, angle):
    return Quaternion(axis, angle)


def axisangle_to_euler(axis, angle, rotation_mode):
    return quat_to_euler(Quaternion(axis, angle), rotation_mode)


def convert_rotation_to_quaternion(rotation_quat, rotation_euler, rotation_mode):
    """
    Should be deprecated in favour of 'convert_rotation'
    """
    if rotation_mode == "QUATERNION":
        # pull out quaternion data, normalise
        return rotation_quat.normalized()
    else:
        return euler_to_quat(rotation_euler, rotation_mode)


def convert_rotation(obj, rotation_mode):
    if rotation_mode == "QUATERNION":
        if obj.rotation_mode == "QUATERNION":   return obj.rotation_quaternion.normalized()
        elif is_euler(obj.rotation_mode):       return euler_to_quat(obj.rotation_euler, obj.rotation_mode)
        elif obj.rotation_mode == "AXIS_ANGLE": return axisangle_to_quat(*decompose_axisangle(obj.rotation_axis_angle))
        else:                                   raise NotImplementedError(f"Object has unknown rotation mode '{obj.rotation_mode}'")
    elif is_euler(rotation_mode):
        if   obj.rotation_mode == "QUATERNION": return quat_to_euler(obj.rotation_quaternion, rotation_mode)
        elif is_euler(obj.rotation_mode):       return Euler(obj.rotation_euler, rotation_mode)
        elif obj.rotation_mode == "AXIS_ANGLE": return axisangle_to_euler(*decompose_axisangle(obj.rotation_axis_angle), rotation_mode)
        else:                                   raise NotImplementedError(f"Object has unknown rotation mode '{obj.rotation_mode}'")
    elif rotation_mode == "AXIS_ANGLE":
        if   obj.rotation_mode == "QUATERNION": return quat_to_axisangle(obj.rotation_quaternion)
        elif is_euler(obj.rotation_mode):       return euler_to_axisangle()
        elif obj.rotation_mode == "AXIS_ANGLE": return decompose_axisangle(obj.rotation_axis_angle)
        else:                                   raise NotImplementedError(f"Object has unknown rotation mode '{obj.rotation_mode}'")
    else:
        raise NotImplementedError(f"Unknown output rotation mode '{rotation_mode}'")
