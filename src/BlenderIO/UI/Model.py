import bpy

from .Node import makeNodePropertiesPanel
from .Physics import OBJECT_PT_GFSToolsPhysicsDataPanel
from ..modelUtilsTest.API.Icon import icon_lookup
from ..modelUtilsTest.UI.UIList import UIListBase
from ..Globals import NAMESPACE
from ..Preferences import get_preferences


def _draw_on_node(context, layout):
    armature = context.armature
    layout = layout
    
    layout.prop(armature.GFSTOOLS_ModelProperties, "root_node_name")

BLANK_ID = icon_lookup["BLANK1"]
INTRL_ID = icon_lookup["GROUP"]
ACTIV_ID = icon_lookup["SOLO_ON"]
TOGON_ID  = icon_lookup["CHECKBOX_HLT"]
TOGOFF_ID = icon_lookup["CHECKBOX_DEHLT"]


class OBJECT_UL_GFSToolsAnimationPackUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties

        if get_preferences().wip_animation_import and get_preferences().developer_mode:
            anim = mprops.animation_packs[index]
            active_icon = TOGON_ID if anim.is_active else TOGOFF_ID
            op = layout.operator(ToggleActiveAnimationPack.bl_idname, text="", icon_value=active_icon, emboss=False)
            op.index = index
        else:
            active_icon = ACTIV_ID if index == mprops.active_animation_pack_idx   else BLANK_ID
            layout.prop(item, "name", text="", emboss=False, icon_value=active_icon, icon_only=True)

        if mprops.has_internal_gap():
            internal_icon = INTRL_ID if index == mprops.internal_animation_pack_idx else BLANK_ID
            layout.prop(item, "name", text="", emboss=False, icon_value=internal_icon, icon_only=True)
        layout.prop(item, "name", text="", emboss=False)


def add_callback(context, event, old_idx, new_idx):
    bpy_armature_object = context.active_object
    bpy_armature        = bpy_armature_object.data
    mprops              = bpy_armature.GFSTOOLS_ModelProperties
    if len(mprops.animation_packs) == 1:
        mprops.animation_packs[0].store_animation_pack(bpy_armature_object)
        mprops.active_animation_pack_idx = 0


def delete_callback(context, event, old_idx, new_idx):
    bpy_armature = context.armature
    mprops       = bpy_armature.GFSTOOLS_ModelProperties
    
    if old_idx <= mprops.active_animation_pack_idx:
        mprops.active_animation_pack_idx -= 1
    
    if old_idx < mprops.internal_animation_pack_idx:
        mprops.internal_animation_pack_idx -= 1
    elif old_idx == mprops.internal_animation_pack_idx:
        mprops.internal_animation_pack_idx = -1
        
    if len(mprops.animation_packs) == 0:
        mprops.internal_animation_pack_idx = -1
        mprops.active_animation_pack_idx   = -1


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
    NAMESPACE,
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
    bl_idname  = f"{NAMESPACE}.setinternalgap"
    bl_options = {'UNDO', 'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        
        return len(mprops.animation_packs) > 0
    
    @staticmethod
    def getText(context):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        return "Remove Internal GAP" if mprops.is_internal_gap_selected() and len(mprops.animation_packs) else "Set Internal GAP"
        
    
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
    bl_idname  = f"{NAMESPACE}.setactivegap"
    bl_options = {'UNDO', 'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        
        return mprops.active_animation_pack_idx != mprops.animation_pack_idx and len(mprops.animation_packs)
    
    def execute(self, context):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        
        active_gap = mprops.get_active_gap()
        if active_gap is not None:
            active_gap.store_animation_pack(bpy_armature_object)
            # TODO: Need some error-handling stuff in here!!!
        selected_gap = mprops.get_selected_gap()
        selected_gap.restore_animation_pack(bpy_armature_object)
        
        mprops.active_animation_pack_idx = mprops.animation_pack_idx
        
        return {'FINISHED'}


class ToggleActiveAnimationPack(bpy.types.Operator):
    bl_label   = "Activate GAP"
    bl_idname  = f"{NAMESPACE}.toggleactivegap"
    bl_options = {'UNDO', 'REGISTER'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        selected_gap = mprops.animation_packs[self.index]

        if selected_gap.is_active:
            # Deactivate
            selected_gap.is_active = False
            selected_gap.update_from_nla(bpy_armature_object)
            selected_gap.remove_from_nla(bpy_armature_object)
        else:
            # Activate
            selected_gap.is_active = True
            selected_gap.add_to_nla(bpy_armature_object)

        return {'FINISHED'}

    @staticmethod
    def getText(context):
        bpy_armature_object = context.active_object
        bpy_armature = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        selected_gap = mprops.get_selected_gap()

        if selected_gap.is_active:
            return "Deactivate GAP"
        else:
            return "Activate GAP"


class AutonameMeshUVs(bpy.types.Operator):
    bl_label = "Auto-Rename Mesh UVs"
    bl_idname = f"{NAMESPACE}.autonamemeshuvs"
    
    @classmethod
    def poll(cls, context):
        if context.active_object is None:
            return False
        return context.active_object.GFSTOOLS_ObjectProperties.is_model()
    
    def execute(self, context):
        context.active_object.GFSTOOLS_ObjectProperties.autoname_mesh_uvs()
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
    def poll(cls, context):
        return context.armature is not None

    def draw(self, context):
        armature = context.armature
        layout = self.layout
        aprops = armature.GFSTOOLS_ModelProperties
        
        ctr = layout.column()
        
        ctr.prop(aprops, 'version')
        ctr.prop(aprops, "has_external_emt")
        ctr.prop(aprops, "flag_3")
        
        ctr.operator(AutonameMeshUVs.bl_idname)
        
        aprops.bounding_box.draw(ctr)
        aprops.bounding_sphere.draw(ctr)
        
        self.PACK_LIST.draw(ctr, context)
        
        op_row = ctr.row()
        if get_preferences().wip_animation_import and get_preferences().developer_mode:
            op = op_row.operator(ToggleActiveAnimationPack.bl_idname, text=ToggleActiveAnimationPack.getText(context))
            op.index = aprops.animation_pack_idx
        else:
            op_row.operator(SetActiveAnimationPack.bl_idname)
        op_row.operator(SetInternalAnimationPack.bl_idname, text=SetInternalAnimationPack.getText(context))
        
    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.NodePropertiesPanel)
        bpy.utils.register_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        bpy.utils.register_class(OBJECT_UL_GFSToolsAnimationPackUIList)
        bpy.utils.register_class(ToggleActiveAnimationPack)
        bpy.utils.register_class(SetActiveAnimationPack)
        bpy.utils.register_class(SetInternalAnimationPack)
        bpy.utils.register_class(AutonameMeshUVs)
        _uilist.register()
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.NodePropertiesPanel)
        bpy.utils.unregister_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsAnimationPackUIList)
        bpy.utils.unregister_class(ToggleActiveAnimationPack)
        bpy.utils.unregister_class(SetActiveAnimationPack)
        bpy.utils.unregister_class(SetInternalAnimationPack)
        bpy.utils.unregister_class(AutonameMeshUVs)
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
