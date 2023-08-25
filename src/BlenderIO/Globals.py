import bpy
from mathutils import Matrix

from . import modelUtilsTest as blenderModelSupportUtils
bmu = blenderModelSupportUtils


GFS_MODEL_TRANSFORMS = bmu.ModelTransforms(world_axis=['X', 'Z', '-Y'], 
                                           bone_axis=['-Y', 'X', 'Z'])
