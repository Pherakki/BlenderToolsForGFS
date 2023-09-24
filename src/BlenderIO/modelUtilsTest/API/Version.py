import bpy


def bpy_at_least(major, minor, patch):
    return all([v1 >= v2 for v1, v2 in zip((major, minor, patch), bpy.app.version)])
