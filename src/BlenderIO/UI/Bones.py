import bpy
from .Node import makeNodePropertiesPanel


def _draw_on_node(context, layout):
    bone   = context.active_bone
    layout = layout
    
    layout.prop(bone.GFSTOOLS_NodeProperties, "override_name")


OBJECT_PT_GFSToolsBonePropertiesPanel = makeNodePropertiesPanel(
    "BoneNode", 
    "PROPERTIES", 
    "WINDOW",
    "bone", 
    lambda context: context.active_bone.GFSTOOLS_NodeProperties,
    lambda cls, context: type(context.active_bone) is bpy.types.Bone,
    predraw=_draw_on_node
)
