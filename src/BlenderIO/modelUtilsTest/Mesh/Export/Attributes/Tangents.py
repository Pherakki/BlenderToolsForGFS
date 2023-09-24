from .Utils import get_loop_attribute


def get_tangents(bpy_mesh_object, use_tangents, sigfigs, transform=None):
    return get_loop_attribute(bpy_mesh_object, use_tangents, "tangent", sigfigs)
