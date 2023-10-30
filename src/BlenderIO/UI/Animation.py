import bpy
from ..Globals import NAMESPACE
from .HelpWindows import defineHelpWindow
from .GFSProperties import makeCustomPropertiesPanel


class GenerateMesh(bpy.types.Operator):
    bl_idname = "gfstools.genanimboundingbox"
    bl_label  = "Show"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        action = context.active_nla_strip.action
        props = action.GFSTOOLS_AnimationProperties
        
        if props.is_bounding_box_alive():
            props.remove_bounding_box()
        else:
            props.generate_bounding_box()
        return {'FINISHED'}


class AnimCopyBoundingBox(bpy.types.Operator):
    bl_label   = "Copy Box"
    bl_idname  = f"{NAMESPACE}.animcopyboundingbox"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return (context.scene is not None) and (context.active_nla_strip is not None)
    
    def execute(self, context):
        scene = context.scene
        action = context.active_nla_strip.action
        clipboard = scene.GFSTOOLS_SceneProperties.clipboard
        aprops    = action.GFSTOOLS_AnimationProperties
        clipboard.bounding_box_min_dims = aprops.bounding_box.min_dims
        clipboard.bounding_box_max_dims = aprops.bounding_box.max_dims
        return {'FINISHED'}


class AnimPasteBoundingBox(bpy.types.Operator):
    bl_label   = "Paste Box"
    bl_idname  = f"{NAMESPACE}.animpasteboundingbox"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return (context.scene is not None) and (context.active_nla_strip is not None)
    
    def execute(self, context):
        scene = context.scene
        action = context.active_nla_strip.action
        clipboard = scene.GFSTOOLS_SceneProperties.clipboard
        aprops    = action.GFSTOOLS_AnimationProperties
        aprops.bounding_box.min_dims = clipboard.bounding_box_min_dims
        aprops.bounding_box.max_dims = clipboard.bounding_box_max_dims
        return {'FINISHED'}


class OBJECT_PT_GFSToolsAnimationPanel(bpy.types.Panel):
    bl_label       = "GFS Animation"
    bl_idname      = "OBJECT_PT_GFSToolsAnimationPanel"
    bl_space_type  = 'NLA_EDITOR'
    bl_region_type = 'UI'
    bl_category    = "Strip"
    
    
    @classmethod
    def poll(cls, context):
        if context.active_nla_strip is None:
            return False
        elif context.active_nla_strip.action is None:
            return False
        
        return True

    def draw(self, context):
        # node = context.active_node
        layout = self.layout
        
        active_action = context.active_nla_strip.action
        props = active_action.GFSTOOLS_AnimationProperties
        
        layout.operator(self.AnimationHelpWindow.bl_idname)
        
        layout.prop(props, "autocorrect_action")
        layout.prop(props, "category")
        props.bounding_box.draw(layout)
        if props.bounding_box.export_policy == "MANUAL":
            row = layout.row()
            row.operator(AnimCopyBoundingBox.bl_idname)
            row.operator(AnimPasteBoundingBox.bl_idname)
        
        layout.prop(props, "flag_0")
        layout.prop(props, "flag_1")
        layout.prop(props, "flag_2")
        layout.prop(props, "flag_3")
        layout.prop(props, "flag_4")
        layout.prop(props, "flag_5")
        layout.prop(props, "flag_6")
        layout.prop(props, "flag_7")
        layout.prop(props, "flag_8")
        layout.prop(props, "flag_9")
        layout.prop(props, "flag_10")
        layout.prop(props, "flag_11")
        layout.prop(props, "flag_12")
        layout.prop(props, "flag_13")
        layout.prop(props, "flag_14")
        layout.prop(props, "flag_15")
        layout.prop(props, "flag_16")
        layout.prop(props, "flag_17")
        layout.prop(props, "flag_18")
        layout.prop(props, "flag_19")
        layout.prop(props, "flag_20")
        layout.prop(props, "flag_21")
        layout.prop(props, "flag_22")
        layout.prop(props, "flag_24")
        layout.prop(props, "flag_26")
        layout.prop(props, "flag_27")
        
        if props.category == "NORMAL":
            layout.prop(props, "has_lookat_anims")
            col = layout.column()
            col.prop(props, "lookat_up")
            col.prop(props, "lookat_up_factor")
            col.prop(props, "lookat_down")
            col.prop(props, "lookat_down_factor")
            col.prop(props, "lookat_left")
            col.prop(props, "lookat_left_factor")
            col.prop(props, "lookat_right")
            col.prop(props, "lookat_right_factor")
            col.enabled = props.has_lookat_anims
            
        if props.category == "BLEND" or props.category == "LOOKAT":
            layout.prop(props, "has_scale_action")
            
            col = layout.column()
            col.prop(props, "blend_scale_action")
            col.enabled = props.has_scale_action

    AnimationHelpWindow = defineHelpWindow("Animation",
        "- 'Autocorrect Action' will autoamtically set the keyframe interpolation and strip blending method to those appropriate for whichever Animation category you switch to.\n"\
        "- 'Category' is the animation category.\n"\
        "- 'Unknown Flags' are unknown. Flags 0-3 may represent the presence of bone, material, camera, and morph animations respectively.\n"\
        "- 'LookAt Anims' are shown if the animation is a Normal Animation. Each animation is a direction the character looks in.\n"\
        "- 'Blend Scale' is shown if the animation is a Blend or LookAt Animation. This is a separate action for the bone scale channels animation.\n"\
        "- GFS Properties of specific data types can be added, removed, and re-ordered with the Properties listbox. Properties that may be recognised and what they may do have not yet been enumerated."
    )
    
    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.AnimationHelpWindow)
        bpy.utils.register_class(GenerateMesh)
        bpy.utils.register_class(AnimCopyBoundingBox)
        bpy.utils.register_class(AnimPasteBoundingBox)
        
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.AnimationHelpWindow)
        bpy.utils.unregister_class(GenerateMesh)
        bpy.utils.unregister_class(AnimCopyBoundingBox)
        bpy.utils.unregister_class(AnimPasteBoundingBox)


OBJECT_PT_GFSToolsAnimationGenericPropertyPanel = makeCustomPropertiesPanel(
    "OBJECT_PT_GFSToolsAnimationPanel",
    "Anim",
    "NLA_EDITOR",
    "UI",
    "Strip",
    lambda context: context.active_nla_strip.action.GFSTOOLS_AnimationProperties,
    lambda cls, context: True
)
