import bpy
from mathutils import Matrix

from . import modelUtilsTest as blenderModelSupportUtils
bm = blenderModelSupportUtils


GFS_MODEL_TRANSFORMS = bm.ModelTransforms(world_axis=['X', 'Z', '-Y'], 
                                          bone_axis=['-Y', 'X', 'Z'])
