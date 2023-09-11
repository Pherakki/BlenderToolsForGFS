import functools

import bpy


def safe_active_object_switch(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        prev_obj = get_active_obj()
        out = func(*args, **kwargs)
        set_active_obj(prev_obj)
        return out
    return wrapped


def set_active_obj(obj):
    bpy.context.view_layer.objects.active = obj


def get_active_obj():
    return bpy.context.view_layer.objects.active


def set_mode(mode):
    bpy.ops.object.mode_set(mode=mode)
