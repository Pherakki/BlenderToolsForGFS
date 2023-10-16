import bpy

from .Node import makeNodePropertiesPanel
from .Physics import OBJECT_PT_GFSToolsPhysicsDataPanel
from ..modelUtilsTest.API.Icon import icon_lookup
from ..modelUtilsTest.UI.UIList import UIListBase


def _draw_on_node(context, layout):
    armature = context.armature
    layout = layout
    
    layout.prop(armature.GFSTOOLS_ModelProperties, "root_node_name")

BLANK_ID = icon_lookup["BLANK1"]
INTRL_ID = icon_lookup["GROUP"]
ACTIV_ID = icon_lookup["SOLO_ON"]


class OBJECT_UL_GFSToolsAnimationPackUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties

        active_icon   = ACTIV_ID if index == mprops.active_animation_pack_idx   else BLANK_ID
        layout.prop(item, "name", text="", emboss=False, icon_value=active_icon, icon_only=True)
        if mprops.has_internal_gap():
            internal_icon = INTRL_ID if index == mprops.internal_animation_pack_idx else BLANK_ID
            layout.prop(item, "name", text="", emboss=False, icon_value=internal_icon, icon_only=True)
        layout.prop(item, "name", text="", emboss=False)


def add_callback(context, event, old_idx, new_idx):
    pass


def delete_callback(context, event, old_idx, new_idx):
    bpy_armature = context.armature
    mprops       = bpy_armature.GFSTOOLS_ModelProperties
    
    if old_idx <= mprops.active_animation_pack_idx:
        mprops.active_animation_pack_idx -= 1
    
    if old_idx < mprops.internal_animation_pack_idx:
        mprops.internal_animation_pack_idx -= 1
    elif old_idx == mprops.internal_animation_pack_idx:
        mprops.internal_animation_pack_idx = -1


def moveup_callback(context, event, old_idx, new_idx):
    if old_idx == new_idx:
        return
    
    bpy_armature = context.armature
    mprops       = bpy_armature.GFSTOOLS_ModelProperties
    
    if old_idx == mprops.active_animation_pack_idx:
        mprops.active_animation_pack_idx -= 1
    elif old_idx == mprops.active_animation_pack_idx + 1:
        mprops.active_animation_pack_idx += 1
    
    if old_idx == mprops.internal_animation_pack_idx:
        mprops.internal_animation_pack_idx -= 1
    elif old_idx == mprops.internal_animation_pack_idx + 1:
        mprops.internal_animation_pack_idx += 1


def movedown_callback(context, event, old_idx, new_idx):
    if old_idx == new_idx:
        return
    
    bpy_armature = context.armature
    mprops       = bpy_armature.GFSTOOLS_ModelProperties
    
    if old_idx == mprops.active_animation_pack_idx:
        mprops.active_animation_pack_idx += 1
    elif old_idx == mprops.active_animation_pack_idx - 1:
        mprops.active_animation_pack_idx -= 1
    
    if old_idx == mprops.internal_animation_pack_idx:
        mprops.internal_animation_pack_idx += 1
    elif old_idx == mprops.internal_animation_pack_idx - 1:
        mprops.internal_animation_pack_idx -= 1


_uilist = UIListBase(
    "gfstools",
    "AnimPacks", 
    OBJECT_UL_GFSToolsAnimationPackUIList, 
    "animation_packs", 
    "animation_pack_idx",
    lambda ctx: ctx.armature.GFSTOOLS_ModelProperties,
    add_callback=add_callback,
    delete_callback=delete_callback,
    moveup_callback=moveup_callback,
    movedown_callback=movedown_callback
)


class SetInternalAnimationPack(bpy.types.Operator):
    bl_label   = "Set Internal GAP"
    bl_idname  = "gfstools.setinternalgap"
    bl_options = {'UNDO', 'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return True
    
    @staticmethod
    def getText(context):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        return "Remove Internal GAP" if mprops.is_internal_gap_selected() else "Set Internal GAP"
        
    
    def execute(self, context):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        
        if mprops.is_internal_gap_selected():
            new_idx = -1
        else:
            new_idx = mprops.animation_pack_idx
        mprops.internal_animation_pack_idx = new_idx
        
        return {'FINISHED'}


class SetActiveAnimationPack(bpy.types.Operator):
    bl_label   = "Set Active GAP"
    bl_idname  = "gfstools.setactivegap"
    bl_options = {'UNDO', 'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        
        return mprops.active_animation_pack_idx != mprops.animation_pack_idx
    
    def execute(self, context):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        
        mprops.active_animation_pack_idx = mprops.animation_pack_idx
        
        return {'FINISHED'}


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
        
        op_row = ctr.row()
        op_row.operator(SetActiveAnimationPack.bl_idname)
        op_row.operator(SetInternalAnimationPack.bl_idname, text=SetInternalAnimationPack.getText(context))
        
    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.NodePropertiesPanel)
        bpy.utils.register_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        bpy.utils.register_class(OBJECT_UL_GFSToolsAnimationPackUIList)
        bpy.utils.register_class(SetActiveAnimationPack)
        bpy.utils.register_class(SetInternalAnimationPack)
        _uilist.register()
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.NodePropertiesPanel)
        bpy.utils.unregister_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsAnimationPackUIList)
        bpy.utils.unregister_class(SetActiveAnimationPack)
        bpy.utils.unregister_class(SetInternalAnimationPack)
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
