import bpy

from ....Globals import NAMESPACE
from ....modelUtilsTest.API.Icon import icon_lookup
from ....modelUtilsTest.UI.UIList import UIListBase
from .BaseAnimationSubPanel import OBJECT_UL_GFSToolsActivateAnimationUIList, SwitchAnimation, ToggleLookAtAnimation
from .BlendAnimationSubPanel import OBJECT_UL_GFSToolsActivateBlendAnimationUIList, ToggleBlendAnimation
from .PropertiesSubPanel import OBJECT_PT_GFSToolsAnimationPackDataPanel

BLANK_ID = icon_lookup["BLANK1"]
INTRL_ID = icon_lookup["GROUP"]
ACTIV_ID = icon_lookup["SOLO_ON"]
TOGON_ID  = icon_lookup["CHECKBOX_HLT"]
TOGOFF_ID = icon_lookup["CHECKBOX_DEHLT"]


class ToggleActiveAnimationPack(bpy.types.Operator):
    bl_label = "Activate GAP"
    bl_idname = f"{NAMESPACE}.toggleactivegap"
    bl_options = {'UNDO', 'REGISTER'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        bpy_armature_object = context.active_object
        bpy_armature = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        
        selected_gap = mprops.animation_packs[self.index]

        if selected_gap.is_active:
            # Deactivate
            if not selected_gap.update_from_nla(bpy_armature_object):
                return {'CANCELLED'}
            selected_gap.remove_from_nla(bpy_armature_object)
            selected_gap.is_active = False
        else:
            # Activate
            selected_gap.add_to_nla(bpy_armature_object)
            selected_gap.is_active = True

        return {'FINISHED'}

    @staticmethod
    def getText(context):
        bpy_armature_object = context.active_object
        bpy_armature = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        selected_gap = mprops.get_selected_gap()

        if selected_gap is None:
            return "No GAPs"
        
        if selected_gap.is_active:
            return "Deactivate GAP"
        else:
            return "Activate GAP"


class OBJECT_UL_GFSToolsAnimationPackUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        bpy_armature_object = context.active_object
        bpy_armature        = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties

        anim = mprops.animation_packs[index]
        active_icon = TOGON_ID if anim.is_active else TOGOFF_ID
        op = layout.operator(ToggleActiveAnimationPack.bl_idname, text="", icon_value=active_icon, emboss=False)
        op.index = index

        if mprops.has_internal_gap():
            internal_icon = INTRL_ID if index == mprops.internal_animation_pack_idx else BLANK_ID
            layout.prop(item, "name", text="", emboss=False, icon_value=internal_icon, icon_only=True)
        layout.prop(item, "name", text="", emboss=False)

def add_callback(context, event, old_idx, new_idx):
    bpy_armature_object = context.active_object
    bpy_armature = bpy_armature_object.data
    mprops = bpy_armature.GFSTOOLS_ModelProperties
    if len(mprops.animation_packs) == 1:
        mprops.animation_packs[0].store_animation_pack(bpy_armature_object)
        mprops.active_animation_pack_idx = 0


def delete_callback(context, event, old_idx, new_idx):
    bpy_armature = context.armature
    mprops = bpy_armature.GFSTOOLS_ModelProperties

    if old_idx <= mprops.active_animation_pack_idx:
        mprops.active_animation_pack_idx -= 1

    if old_idx < mprops.internal_animation_pack_idx:
        mprops.internal_animation_pack_idx -= 1
    elif old_idx == mprops.internal_animation_pack_idx:
        mprops.internal_animation_pack_idx = -1

    if len(mprops.animation_packs) == 0:
        mprops.internal_animation_pack_idx = -1
        mprops.active_animation_pack_idx = -1


def moveup_callback(context, event, old_idx, new_idx):
    if old_idx == new_idx:
        return

    bpy_armature = context.armature
    mprops = bpy_armature.GFSTOOLS_ModelProperties

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
    mprops = bpy_armature.GFSTOOLS_ModelProperties

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
    bl_label = "Set Internal GAP"
    bl_idname = f"{NAMESPACE}.setinternalgap"
    bl_options = {'UNDO', 'REGISTER'}

    @classmethod
    def poll(cls, context):
        bpy_armature_object = context.active_object
        bpy_armature = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties

        return len(mprops.animation_packs) > 0

    @staticmethod
    def getText(context):
        bpy_armature_object = context.active_object
        bpy_armature = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        return "Remove Internal GAP" if mprops.is_internal_gap_selected() and len(
            mprops.animation_packs) else "Set Internal GAP"

    def execute(self, context):
        bpy_armature_object = context.active_object
        bpy_armature = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties

        if mprops.is_internal_gap_selected():
            new_idx = -1
        else:
            new_idx = mprops.animation_pack_idx
        mprops.internal_animation_pack_idx = new_idx

        return {'FINISHED'}


class SetActiveAnimationPack(bpy.types.Operator):
    bl_label = "Set Active GAP"
    bl_idname = f"{NAMESPACE}.setactivegap"
    bl_options = {'UNDO', 'REGISTER'}

    @classmethod
    def poll(cls, context):
        bpy_armature_object = context.active_object
        bpy_armature = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties

        return mprops.active_animation_pack_idx != mprops.animation_pack_idx and len(mprops.animation_packs)

    def execute(self, context):
        bpy_armature_object = context.active_object
        bpy_armature = bpy_armature_object.data
        mprops = bpy_armature.GFSTOOLS_ModelProperties

        active_gap = mprops.get_active_gap()
        if active_gap is not None:
            active_gap.store_animation_pack(bpy_armature_object)
            # TODO: Need some error-handling stuff in here!!!
        selected_gap = mprops.get_selected_gap()
        selected_gap.restore_animation_pack(bpy_armature_object)

        mprops.active_animation_pack_idx = mprops.animation_pack_idx

        return {'FINISHED'}


class OBJECT_PT_GFSToolsAnimationDataPanel(bpy.types.Panel):
    bl_label       = "GFS Animation Packs"
    bl_idname      = "OBJECT_PT_GFSToolsAnimationDataPanel"
    bl_parent_id   = "OBJECT_PT_GFSToolsModelDataPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = set()

    PACK_LIST = _uilist()

    @classmethod
    def poll(cls, context):
        return context.armature is not None

    def _draw_lookat(self, layout, gap, lookat_lookup, anim_name, icon_name):
        row = layout.row()
        row.scale_x = 0.6
        row.label(icon=icon_name)

        lookat_idx = lookat_lookup.get(anim_name, -1)
        if lookat_idx > -1:
            icon_name = "CHECKBOX_HLT" if gap.test_lookat_anims[lookat_idx].is_active else "CHECKBOX_DEHLT"
            op = layout.operator(ToggleLookAtAnimation.bl_idname, icon=icon_name, emboss=False)
            op.index = lookat_idx
        else:
            row.label(icon="CHECKBOX_DEHLT")

    def draw(self, context):
        armature = context.armature
        layout = self.layout
        aprops = armature.GFSTOOLS_ModelProperties

        ctr = layout.column()

        self.PACK_LIST.draw(ctr, context)

        op_row = ctr.row()
        op = op_row.operator(ToggleActiveAnimationPack.bl_idname, text=ToggleActiveAnimationPack.getText(context))
        op.index = aprops.animation_pack_idx
        op_row.operator(SetInternalAnimationPack.bl_idname, text=SetInternalAnimationPack.getText(context))

        gap = aprops.get_selected_gap()

        if gap is None:
            return
        
        ctr.separator(factor=1.0)

        lookat_row = ctr.row()
        lookat_row.label(text="Root LookAts:")
        lookat_lookup = gap.lookat_anims_as_dict()

        self._draw_lookat(lookat_row, gap, lookat_lookup, gap.test_lookat_left, "TRIA_LEFT")
        self._draw_lookat(lookat_row, gap, lookat_lookup, gap.test_lookat_up, "TRIA_UP")
        self._draw_lookat(lookat_row, gap, lookat_lookup, gap.test_lookat_right, "TRIA_RIGHT")
        self._draw_lookat(lookat_row, gap, lookat_lookup, gap.test_lookat_down, "TRIA_DOWN")

        ctr.label(text="Base Animations")
        ctr.template_list(OBJECT_UL_GFSToolsActivateAnimationUIList.__name__, "", gap, "test_anims", gap,
                          "test_anims_idx")

        ctr.label(text="Blend Animations")
        ctr.template_list(OBJECT_UL_GFSToolsActivateBlendAnimationUIList.__name__, "", gap, "test_blend_anims", gap,
                          "test_blend_anims_idx")

    @classmethod
    def register(cls):
        bpy.utils.register_class(SwitchAnimation)
        bpy.utils.register_class(ToggleBlendAnimation)
        bpy.utils.register_class(ToggleLookAtAnimation)
        bpy.utils.register_class(OBJECT_UL_GFSToolsAnimationPackUIList)
        bpy.utils.register_class(ToggleActiveAnimationPack)
        bpy.utils.register_class(SetActiveAnimationPack)
        bpy.utils.register_class(SetInternalAnimationPack)
        bpy.utils.register_class(OBJECT_UL_GFSToolsActivateAnimationUIList)
        bpy.utils.register_class(OBJECT_UL_GFSToolsActivateBlendAnimationUIList)
        bpy.utils.register_class(OBJECT_PT_GFSToolsAnimationPackDataPanel)
        _uilist.register()

    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(SwitchAnimation)
        bpy.utils.unregister_class(ToggleBlendAnimation)
        bpy.utils.unregister_class(ToggleLookAtAnimation)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsAnimationPackUIList)
        bpy.utils.unregister_class(ToggleActiveAnimationPack)
        bpy.utils.unregister_class(SetActiveAnimationPack)
        bpy.utils.unregister_class(SetInternalAnimationPack)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsActivateAnimationUIList)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsActivateBlendAnimationUIList)
        bpy.utils.unregister_class(OBJECT_PT_GFSToolsAnimationPackDataPanel)
        _uilist.unregister()
