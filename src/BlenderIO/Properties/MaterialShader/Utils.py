import bpy


def copy_list(out, src, size):
    for i in range(size):
        out[i] = src[i]
