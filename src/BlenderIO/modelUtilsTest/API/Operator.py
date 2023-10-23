import bpy


def get_op(cls):
    op = bpy.ops
    for subitem in cls.bl_idname.split('.'):
        op = getattr(op, subitem)
    return op


def get_op_idname(cls):
    return get_op(cls).idname()
