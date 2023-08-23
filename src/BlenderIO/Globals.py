import bpy
from mathutils import Matrix

from . import modelUtilsTest as blenderModelSupportUtils
bm = blenderModelSupportUtils


GFS_MODEL_TRANSFORMS = bm.ModelTransforms()
GFS_MODEL_TRANSFORMS.world_axis_rotation = Matrix([[ 1.,  0.,  0.,  0.],
                                                   [ 0.,  0., -1.,  0.],
                                                   [ 0.,  1.,  0.,  0.],
                                                   [ 0.,  0.,  0.,  1.]])
GFS_MODEL_TRANSFORMS.bone_axis_permutation = Matrix([[ 0.,  1.,  0.,  0.],
                                                     [-1.,  0.,  0.,  0.],
                                                     [ 0.,  0.,  1.,  0.],
                                                     [ 0.,  0.,  0.,  1.]])
