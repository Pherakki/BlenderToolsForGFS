import bpy

from ....Globals import NAMESPACE, BASE_ANIM_TYPE, LOOKAT_ANIM_TYPE, LOOKATSCALE_ANIM_TYPE
from ....Utils.Animation import gapnames_to_nlatrack, is_anim_restpose


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
        name = gapnames_to_nlatrack(gap.name, BASE_ANIM_TYPE, anim.name)

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
        name = gapnames_to_nlatrack(gap.name, LOOKAT_ANIM_TYPE, anim.name)
        name2 = gapnames_to_nlatrack(gap.name, LOOKATSCALE_ANIM_TYPE, anim.name)
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
