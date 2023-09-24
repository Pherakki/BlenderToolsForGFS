from .Utils import get_loop_attribute


def get_normals(bpy_mesh_object, use_normals, sigfigs, transform=None):
    return get_loop_attribute(bpy_mesh_object, use_normals, "normal", sigfigs)
