import bpy
from .Node import makeNodePropertiesPanel
    
OBJECT_PT_GFSToolsBonePropertiesPanel = makeNodePropertiesPanel(
    "BoneNode", 
    "PROPERTIES", 
    "WINDOW",
    "bone", 
    lambda context: context.active_bone.GFSTOOLS_NodeProperties,
    lambda cls, context: type(context.active_bone) is bpy.types.Bone
)
