import numpy as np

from .Utils import empty_attr, round_to_sigfigs


def get_binormals(bpy_mesh_obj, use_binormals, sigfigs, transform=None):
    bpy_mesh = bpy_mesh_obj.data
    loops = bpy_mesh.loops
    nloops = len(loops)
    if use_binormals:
        data  = [(round_to_sigfigs(l.bitangent_sign * np.cross(l.normal, l.tangent), sigfigs)) for l in loops]
        if transform is None: return data
        else:                 return [transform(d, l) for d, l in zip(data, loops)]
    else:
        return empty_attr(nloops)
