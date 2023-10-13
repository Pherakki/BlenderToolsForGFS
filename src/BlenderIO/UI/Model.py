import bpy

from .Node import makeNodePropertiesPanel
from .Physics import OBJECT_PT_GFSToolsPhysicsDataPanel
from ..modelUtilsTest.UI.UIList import UIListBase


def _draw_on_node(context, layout):
    armature = context.armature
    layout = layout
    
    layout.prop(armature.GFSTOOLS_ModelProperties, "root_node_name")


class OBJECT_UL_GFSToolsAnimationPackUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item, "name", text="", emboss=False)


_uilist = UIListBase(
    "gfstools",
    "AnimPacks", 
    OBJECT_UL_GFSToolsAnimationPackUIList, 
    "animation_packs", 
    "animation_pack_idx",
    lambda ctx: ctx.armature.GFSTOOLS_ModelProperties
)


class SwapActiveAnimationPack(bpy.types.Operator):
    bl_label   = "Swap Active GAP"
    bl_idname  = "gfstools.swapactivegap"
    bl_options = {'UNDO', 'REGISTER'}
    
    def execute(self, context):
        raise NotImplementedError


class OBJECT_PT_GFSToolsModelDataPanel(bpy.types.Panel):
    bl_label       = "GFS Model"
    bl_idname      = "OBJECT_PT_GFSToolsModelDataPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    PACK_LIST = _uilist()
    
    @classmethod
    def poll(self, context):
        return context.armature is not None

    def draw(self, context):
        armature = context.armature
        layout = self.layout
        aprops = armature.GFSTOOLS_ModelProperties
        
        ctr = layout.column()
        
        ctr.prop(aprops, "has_external_emt")
        ctr.prop(aprops, "flag_3")
        
        aprops.bounding_box.draw(ctr)
        aprops.bounding_sphere.draw(ctr)
        
        self.PACK_LIST.draw(layout, context)
        
    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.NodePropertiesPanel)
        bpy.utils.register_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        bpy.utils.register_class(OBJECT_UL_GFSToolsAnimationPackUIList)
        _uilist.register()
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.NodePropertiesPanel)
        bpy.utils.unregister_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsAnimationPackUIList)
        _uilist.unregister()
    
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
