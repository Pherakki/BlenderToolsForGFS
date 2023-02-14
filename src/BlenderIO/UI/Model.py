import bpy

from .Node import makeNodePropertiesPanel

    
def _draw_on_node(context, layout):
    armature = context.armature
    layout = layout
    
    layout.prop(armature.GFSTOOLS_ModelProperties, "root_node_name")
    
class OBJECT_PT_GFSToolsModelDataPanel(bpy.types.Panel):
    bl_label       = "GFS Model"
    bl_idname      = "OBJECT_PT_GFSToolsModelDataPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return context.armature is not None

    def draw(self, context):
        armature = context.armature
        layout = self.layout
        
        ctr = layout.column()
        
        ctr.prop(armature.GFSTOOLS_ModelProperties, "has_external_emt")
        ctr.prop(armature.GFSTOOLS_ModelProperties, "export_bounding_box")
        ctr.prop(armature.GFSTOOLS_ModelProperties, "export_bounding_sphere")
        ctr.prop(armature.GFSTOOLS_ModelProperties, "flag_3")
    
    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.NodePropertiesPanel)
        
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.NodePropertiesPanel)
    
    NodePropertiesPanel = makeNodePropertiesPanel(
        "ArmatureNode", 
        "PROPERTIES", 
        "WINDOW",
        "data", 
        lambda context: context.armature.data.GFSTOOLS_NodeProperties,
        lambda cls, context: context.armature is not None,
        parent_id="OBJECT_PT_GFSToolsModelDataPanel",
        predraw=_draw_on_node
    )
