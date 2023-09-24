import array

import numpy as np


def round_to_sigfigs(x, p):
    """
    Credit to Scott Gigante
    Taken from https://stackoverflow.com/a/59888924
    Rounds a float x to p significant figures
    """
    x = np.asarray(x)
    x_positive = np.where(np.isfinite(x) & (x != 0), np.abs(x), 10**(p-1))
    mags = 10 ** (p - 1 - np.floor(np.log10(x_positive)))
    return np.round(x * mags) / mags


def fetch_data(obj, element, sigfigs):
    dsize = len(getattr(obj[0], element))
    data = array.array('f', [0.0] * (len(obj) * dsize))
    obj.foreach_get(element, data)
    return [tuple(round_to_sigfigs(datum, sigfigs)) for datum in zip(*(iter(data),) * dsize)]


def empty_attr(size):
    return (None for _ in range(size))


def get_loop_attribute(bpy_mesh_obj, use_attribute, attribute, sigfigs, transform=None):
    bpy_mesh = bpy_mesh_obj.data
    loops = bpy_mesh.loops
    nloops = len(loops)
    if use_attribute:
        data  = fetch_data(loops, attribute, sigfigs)
        if transform is None:
            return data
        else:
            return [transform(d, l) for d, l in zip(data, loops)]
    else:
        return empty_attr(nloops)


def make_blank(count, shape):
    elem = tuple([0.0 for _ in range(shape)])
    return [elem for _ in range(count)]
