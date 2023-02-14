import bpy
from .GFSProperties import makeCustomPropertiesPanel
from .Node import makeNodePropertiesPanel

# class OBJECT_PT_GFSToolsBonePropertiesPanel(bpy.types.Panel):
#     bl_label       = "GFS Node"
#     bl_idname      = "OBJECT_PT_GFSToolsBonePropertiesPanel"
#     bl_space_type  = 'PROPERTIES'
#     bl_region_type = 'WINDOW'
#     bl_context     = "bone"


#     @classmethod
#     def poll(self, context):
#         return type(context.active_bone) is bpy.types.Bone

#     def draw(self, context):
#         layout = self.layout
        
#         obj = context.active_bone
        
#         layout.prop(obj.GFSTOOLS_BoneProperties, "unknown_float")


# OBJECT_PT_GFSToolsBoneGenericPropertyPanel = makeCustomPropertiesPanel(
#     "OBJECT_PT_GFSToolsBonePropertiesPanel",
#     "BoneNode",
#     "PROPERTIES",
#     "WINDOW",
#     "bone",
#     lambda context: context.active_bone.GFSTOOLS_BoneProperties,
#     lambda cls, context: type(context.active_bone) is bpy.types.Bone
#     )

OBJECT_PT_GFSToolsBonePropertiesPanel = makeNodePropertiesPanel(
    "BoneNode", 
    "PROPERTIES", 
    "WINDOW",
    "bone", 
    lambda context: context.active_bone.GFSTOOLS_NodeProperties,
    lambda cls, context: type(context.active_bone) is bpy.types.Bone
)