import bpy
from mathutils import Matrix

from . import modelUtilsTest as blenderModelSupportUtils
from .modelUtilsTest.Misc.Errorlog import ErrorLogBase
bmu = blenderModelSupportUtils

NAMESPACE = "gfstools"
BASE_ANIM_TYPE        = "BASE"
BLEND_ANIM_TYPE       = "BLEND"
BLENDSCALE_ANIM_TYPE  = "BLENDSCALE"
LOOKAT_ANIM_TYPE      = "LOOKAT"
LOOKATSCALE_ANIM_TYPE = "LOOKATSCALE"

GFS_MODEL_TRANSFORMS = bmu.ModelTransforms(world_axis=['X', 'Z', '-Y'], 
                                           bone_axis=['-Y', 'X', 'Z'])


ErrorLogger = ErrorLogBase(NAMESPACE, "BlenderToolsForGFS", 
    "BlenderToolsForGFS has encountered an unhandled error. The exception is:\n\n"               \
    "{exception_msg}\n\n"                                                                        \
    "A full stacktrace has been printed to the console.\n"                                       \
    "Since all exceptions should be handled by the internal error-reporting system, "            \
    "this is a bug. Please report this at https://github.com/Pherakki/BlenderToolsForGFS/issues" \
    " with the following information:\n"                                                         \
    "1) {context_msg}\n"                                                                         \
    "2) The stacktrace that has been printed to the console.\n"                                  \
    "3) Any further information that you think may be relevant."
)
