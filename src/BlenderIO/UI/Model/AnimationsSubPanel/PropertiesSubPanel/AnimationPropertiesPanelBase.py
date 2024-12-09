import bpy

from .....modelUtilsTest.UI.UIList import UIListBase
from .....Globals import NAMESPACE
from .....Preferences import get_preferences
from ....GFSProperties import makeCustomPropertiesPanel


class OBJECT_UL_GFSToolsAnimationUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        bpy_armature_object = context.active_object
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        gap = mprops.get_selected_gap()

        if gap.is_active:
            layout.label(text=item.name)
        else:
            layout.prop(item, "name", text="", emboss=False)



def generate_panel(identifier, label, getter, collection_name, collection_idx_name, extra_collection_indices):
    OBJECT_PT_GFSToolsAnimationGenericPropertyPanel = makeCustomPropertiesPanel(
        f"OBJECT_PT_GFSTools{identifier}PropsPanel",
        identifier,
        "PROPERTIES",
        "WINDOW",
        "data",
        getter,
        lambda cls, context: getter(context) is not None
    )

    class AnimCopyBoundingBox(bpy.types.Operator):
        bl_label = "Copy Box"
        bl_idname = f"{NAMESPACE}.{identifier}copyboundingbox".lower()
        bl_options = {'REGISTER', 'UNDO'}

        @classmethod
        def poll(cls, context):
            return True

        def execute(self, context):
            scene = context.scene
            clipboard = scene.GFSTOOLS_SceneProperties.clipboard
            props = getter(context)
            clipboard.bounding_box_min_dims = props.bounding_box.min_dims
            clipboard.bounding_box_max_dims = props.bounding_box.max_dims
            return {'FINISHED'}

    class AnimPasteBoundingBox(bpy.types.Operator):
        bl_label = "Paste Box"
        bl_idname = f"{NAMESPACE}.{identifier}pasteboundingbox".lower()
        bl_options = {'REGISTER', 'UNDO'}

        @classmethod
        def poll(cls, context):
            return True

        def execute(self, context):
            scene = context.scene
            clipboard = scene.GFSTOOLS_SceneProperties.clipboard
            props = getter(context)
            props.bounding_box.min_dims = clipboard.bounding_box_min_dims
            props.bounding_box.max_dims = clipboard.bounding_box_max_dims
            return {'FINISHED'}

    _uilist = UIListBase(
        NAMESPACE,
        identifier,
        OBJECT_UL_GFSToolsAnimationUIList,
        collection_name,
        collection_idx_name,
        lambda ctx: ctx.armature.GFSTOOLS_ModelProperties.get_selected_gap(),
        extra_collection_indices=extra_collection_indices
    )
    setattr(_uilist, "poll", classmethod(lambda cls, context: get_preferences().developer_mode))

    class OBJECT_PT_GFSToolsBaseAnimationPropsPanel(bpy.types.Panel):
        bl_label = label
        bl_parent_id = "OBJECT_PT_GFSToolsAnimationPackDataPanel"
        bl_idname = f"OBJECT_PT_GFSTools{identifier}PropsPanel"
        bl_space_type = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context = "data"
        bl_options = {'DEFAULT_CLOSED'}

        ANIM_LIST = _uilist()

        def draw(self, context):
            bpy_armature = context.armature
            mprops = bpy_armature.GFSTOOLS_ModelProperties

            layout = self.layout

            self.ANIM_LIST.draw(layout, context)
            gap = mprops.get_selected_gap()
            props = getter(context)
            if props is not None:
                # Flags
                flag_col = layout.column()
                flag_col.prop(props, "flag_0")
                flag_col.prop(props, "flag_1")
                flag_col.prop(props, "flag_3")
                flag_col.prop(props, "flag_4")
                flag_col.prop(props, "flag_5")
                flag_col.prop(props, "flag_6")
                flag_col.prop(props, "flag_7")
                flag_col.prop(props, "flag_8")
                flag_col.prop(props, "flag_9")
                flag_col.prop(props, "flag_10")
                flag_col.prop(props, "flag_11")
                flag_col.prop(props, "flag_12")
                flag_col.prop(props, "flag_13")
                flag_col.prop(props, "flag_14")
                flag_col.prop(props, "flag_15")
                flag_col.prop(props, "flag_16")
                flag_col.prop(props, "flag_17")
                flag_col.prop(props, "flag_18")
                flag_col.prop(props, "flag_19")
                flag_col.prop(props, "flag_20")
                flag_col.prop(props, "flag_21")
                flag_col.prop(props, "flag_22")
                flag_col.prop(props, "flag_24")
                flag_col.prop(props, "flag_26")
                flag_col.prop(props, "flag_27")
                
                # LookAts
                flag_col.prop(props, "has_lookat_anims", text="Has LookAt Anims:")
                if props.has_lookat_anims:
                    lookat_col = flag_col.column()
                    lookat_col.prop_search(props, "test_lookat_up", gap, "test_lookat_anims")
                    lookat_col.prop(props, "lookat_up_factor")
                    lookat_col.prop_search(props, "test_lookat_down", gap, "test_lookat_anims")
                    lookat_col.prop(props, "lookat_down_factor")
                    lookat_col.prop_search(props, "test_lookat_left", gap, "test_lookat_anims")
                    lookat_col.prop(props, "lookat_left_factor")
                    lookat_col.prop_search(props, "test_lookat_right", gap, "test_lookat_anims")
                    lookat_col.prop(props, "lookat_right_factor")

                # EPLs
                layout.label(text=f"EPLs: {len(props.epls)}")

                # Bounding Box
                props.bounding_box.draw(layout)
                if props.bounding_box.export_policy == "MANUAL":
                    row = layout.row()
                    row.operator(AnimCopyBoundingBox.bl_idname)
                    row.operator(AnimPasteBoundingBox.bl_idname)


        @classmethod
        def register(cls):
            bpy.utils.register_class(AnimCopyBoundingBox)
            bpy.utils.register_class(AnimPasteBoundingBox)
            bpy.utils.register_class(OBJECT_PT_GFSToolsAnimationGenericPropertyPanel)
            _uilist.register()

        @classmethod
        def unregister(cls):
            bpy.utils.unregister_class(AnimCopyBoundingBox)
            bpy.utils.unregister_class(AnimPasteBoundingBox)
            bpy.utils.unregister_class(OBJECT_PT_GFSToolsAnimationGenericPropertyPanel)
            _uilist.unregister()

    return OBJECT_PT_GFSToolsBaseAnimationPropsPanel
