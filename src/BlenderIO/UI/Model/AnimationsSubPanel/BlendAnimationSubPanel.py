import bpy

from ....Globals import NAMESPACE, BLEND_ANIM_TYPE, BLENDSCALE_ANIM_TYPE
from ....Utils.Animation import gapnames_to_nlatrack


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
        name = gapnames_to_nlatrack(gap.name, BLEND_ANIM_TYPE, anim.name)
        name2 = gapnames_to_nlatrack(gap.name, BLENDSCALE_ANIM_TYPE, anim.name)

        names = set((name, name2))

        for nla_track in anim_data.nla_tracks:
            if nla_track.name in names:
                nla_track.mute = not anim.is_active

        return {'FINISHED'}


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
