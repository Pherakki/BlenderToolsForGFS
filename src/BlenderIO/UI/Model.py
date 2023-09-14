import bpy

from .Node import makeNodePropertiesPanel
from .Physics import OBJECT_PT_GFSToolsPhysicsDataPanel
from ..modelUtilsTest.UI.Layout import indent

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
        ctr.prop(armature.GFSTOOLS_ModelProperties, "flag_3")
        
        # Bounding box
        ctr.prop(armature.GFSTOOLS_ModelProperties, "export_bounding_box")
        if armature.GFSTOOLS_ModelProperties.export_bounding_box == "MANUAL":
            col = indent(ctr)
            
            row = col.row()
            row.prop(armature.GFSTOOLS_ModelProperties, "bounding_box_min")
            row = col.row()
            row.prop(armature.GFSTOOLS_ModelProperties, "bounding_box_max")
            armature.GFSTOOLS_ModelProperties.bounding_box_mesh.draw_operator(col)
        
        # Bounding sphere
        ctr.prop(armature.GFSTOOLS_ModelProperties, "export_bounding_sphere")
        if armature.GFSTOOLS_ModelProperties.export_bounding_sphere == "MANUAL":
            col = indent(ctr)
            
            row = col.row()
            row.prop(armature.GFSTOOLS_ModelProperties, "bounding_sphere_centre")
            row = col.row()
            row.prop(armature.GFSTOOLS_ModelProperties, "bounding_sphere_radius")
            armature.GFSTOOLS_ModelProperties.bounding_sphere_mesh.draw_operator(col)
        
    
    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.NodePropertiesPanel)
        bpy.utils.register_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.NodePropertiesPanel)
        bpy.utils.unregister_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
    
    NodePropertiesPanel = makeNodePropertiesPanel(
        "ArmatureNode", 
        "PROPERTIES", 
        "WINDOW",
        "data", 
        lambda context: context.armature.GFSTOOLS_NodeProperties,
        lambda cls, context: context.armature is not None,
        parent_id="OBJECT_PT_GFSToolsModelDataPanel",
        predraw=_draw_on_node
    )
