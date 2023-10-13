import bpy


def bpy_at_least(major, minor, patch):
    return (major, minor, patch) <= bpy.app.version
