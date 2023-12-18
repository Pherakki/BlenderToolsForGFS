import bpy

from .Node import makeNodePropertiesPanel
from .Physics import OBJECT_PT_GFSToolsPhysicsDataPanel
from ..modelUtilsTest.API.Icon import icon_lookup
from ..modelUtilsTest.UI.UIList import UIListBase
from ..Globals import NAMESPACE
from ..Preferences import get_preferences
from ..Utils.Animation import gapnames_to_nlatrack, is_anim_restpose


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


class SwitchAnimation(bpy.types.Operator):
    index: bpy.props.IntProperty()

    bl_label   = ""
    bl_idname = f"{NAMESPACE}.switchanimation"
    bl_options = {"UNDO", "REGISTER"}

    @classmethod
    def poll(cls, context):
        bpy_armature_object = context.active_object
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        return mprops.is_selected_gap_active()

    def execute(self, context):
        bpy_armature_object = context.active_object
        anim_data           = bpy_armature_object.animation_data
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        gap = mprops.get_selected_gap()

        anim = gap.test_anims[self.index]
        name = gapnames_to_nlatrack(gap.name, "NORMAL", anim.name)

        # Reset armature pose, deactivate tracks
        for nla_track in anim_data.nla_tracks:
            nla_track.mute = True
        for bone in bpy_armature_object.pose.bones:
            bone.location            = (0., 0., 0.)
            bone.rotation_quaternion = (1., 0., 0., 0.)
            bone.rotation_euler      = (0., 0., 0.)
            bone.scale               = (1., 1., 1.)

        # Reactivate any necessary animations, set index
        if gap.active_anim_idx == self.index:
            gap.active_anim_idx = -1
        else:
            gap.active_anim_idx = self.index
            for nla_track in anim_data.nla_tracks:
                if nla_track.name == name or is_anim_restpose(nla_track):
                    nla_track.mute = False

        return {'FINISHED'}


class ToggleBlendAnimation(bpy.types.Operator):
    index: bpy.props.IntProperty()

    bl_label   = ""
    bl_idname = f"{NAMESPACE}.toggleblendanimation"
    bl_options = {"UNDO", "REGISTER"}

    @classmethod
    def poll(cls, context):
        bpy_armature_object = context.active_object
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        return mprops.is_selected_gap_active()

    def execute(self, context):
        bpy_armature_object = context.active_object
        anim_data           = bpy_armature_object.animation_data
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        gap = mprops.get_selected_gap()

        anim = gap.test_blend_anims[self.index]
        anim.is_active = not anim.is_active
        name = gapnames_to_nlatrack(gap.name, "BLEND", anim.name)
        name2 = gapnames_to_nlatrack(gap.name, "BLENDSCALE", anim.name)

        names = set((name, name2))

        for nla_track in anim_data.nla_tracks:
            if nla_track.name in names:
                nla_track.mute = not anim.is_active

        return {'FINISHED'}


class ToggleLookAtAnimation(bpy.types.Operator):
    index: bpy.props.IntProperty()

    bl_label = ""
    bl_idname = f"{NAMESPACE}.togglelookatanimation"
    bl_options = {"UNDO", "REGISTER"}

    @classmethod
    def poll(cls, context):
        bpy_armature_object = context.active_object
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        return mprops.is_selected_gap_active()

    def execute(self, context):
        bpy_armature_object = context.active_object
        anim_data = bpy_armature_object.animation_data
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        gap = mprops.get_selected_gap()

        anim = gap.test_lookat_anims[self.index]
        anim.is_active = not anim.is_active
        name = gapnames_to_nlatrack(gap.name, "LOOKAT", anim.name)
        name2 = gapnames_to_nlatrack(gap.name, "LOOKATSCALE", anim.name)
        names = set((name, name2))

        for nla_track in anim_data.nla_tracks:
            if nla_track.name in names:
                nla_track.mute = not anim.is_active

        return {'FINISHED'}


class OBJECT_UL_GFSToolsActivateAnimationUIList(bpy.types.UIList):
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

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        bpy_armature_object = context.active_object
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        gap = mprops.get_selected_gap()

        icon_name = "SOLO_ON" if index == gap.active_anim_idx else "SOLO_OFF"
        op = layout.operator(SwitchAnimation.bl_idname, icon=icon_name, emboss=False)
        op.index = index
        if gap.is_active:
            layout.label(text=item.name)
        else:
            layout.prop(item, "name", text="", emboss=False)

        if item.has_lookat_anims:
            lookat_lookup = gap.lookat_anims_as_dict()

            self._draw_lookat(layout, gap, lookat_lookup, item.test_lookat_left , "TRIA_LEFT")
            self._draw_lookat(layout, gap, lookat_lookup, item.test_lookat_up   , "TRIA_UP")
            self._draw_lookat(layout, gap, lookat_lookup, item.test_lookat_right, "TRIA_RIGHT")
            self._draw_lookat(layout, gap, lookat_lookup, item.test_lookat_down , "TRIA_DOWN")


class OBJECT_UL_GFSToolsActivateBlendAnimationUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        bpy_armature_object = context.active_object
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        gap = mprops.get_selected_gap()

        icon_name = "CHECKBOX_HLT" if gap.test_blend_anims[index].is_active else "CHECKBOX_DEHLT"
        op = layout.operator(ToggleBlendAnimation.bl_idname, icon=icon_name, emboss=False)
        op.index = index
        if gap.is_active:
            layout.label(text=item.name)
        else:
            layout.prop(item, "name", text="", emboss=False)


class OBJECT_PT_GFSToolsAnimationDataPanel(bpy.types.Panel):
    bl_label       = "Animation Packs"
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

    def draw(self, context):
        armature = context.armature
        layout = self.layout
        aprops = armature.GFSTOOLS_ModelProperties

        ctr = layout.column()

        self.PACK_LIST.draw(ctr, context)

        op_row = ctr.row()
        if get_preferences().wip_animation_import and get_preferences().developer_mode:
            op = op_row.operator(ToggleActiveAnimationPack.bl_idname, text=ToggleActiveAnimationPack.getText(context))
            op.index = aprops.animation_pack_idx
        else:
            op_row.operator(SetActiveAnimationPack.bl_idname)
        op_row.operator(SetInternalAnimationPack.bl_idname, text=SetInternalAnimationPack.getText(context))

        if get_preferences().wip_animation_import and get_preferences().developer_mode:
            gap = aprops.get_selected_gap()
            ctr.label(text="Base Animations")
            ctr.template_list(OBJECT_UL_GFSToolsActivateAnimationUIList.__name__, "", gap, "test_anims", gap,
                              "test_anims_idx")

            ctr.label(text="Blend Animations")
            ctr.template_list(OBJECT_UL_GFSToolsActivateBlendAnimationUIList.__name__, "", gap, "test_blend_anims", gap,
                              "test_blend_anims_idx")

    @classmethod
    def register(cls):
        bpy.utils.register_class(OBJECT_UL_GFSToolsAnimationPackUIList)
        bpy.utils.register_class(ToggleActiveAnimationPack)
        bpy.utils.register_class(SetActiveAnimationPack)
        bpy.utils.register_class(SetInternalAnimationPack)
        bpy.utils.register_class(OBJECT_UL_GFSToolsActivateAnimationUIList)
        bpy.utils.register_class(OBJECT_UL_GFSToolsActivateBlendAnimationUIList)
        _uilist.register()

    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsAnimationPackUIList)
        bpy.utils.unregister_class(ToggleActiveAnimationPack)
        bpy.utils.unregister_class(SetActiveAnimationPack)
        bpy.utils.unregister_class(SetInternalAnimationPack)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsActivateAnimationUIList)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsActivateBlendAnimationUIList)
        _uilist.unregister()


def _draw_on_node(context, layout):
    armature = context.armature
    layout = layout
    
    layout.prop(armature.GFSTOOLS_ModelProperties, "root_node_name")


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

    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.NodePropertiesPanel)
        bpy.utils.register_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        bpy.utils.register_class(AutonameMeshUVs)
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.NodePropertiesPanel)
        bpy.utils.unregister_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        bpy.utils.unregister_class(AutonameMeshUVs)

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
