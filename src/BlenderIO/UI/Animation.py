import bpy
from .GFSProperties import makeCustomPropertiesPanel


class OBJECT_PT_GFSToolsAnimationPanel(bpy.types.Panel):
    bl_label       = "GFS Animation"
    bl_idname      = "OBJECT_PT_GFSToolsAnimationPanel"
    bl_space_type  = 'NLA_EDITOR'
    bl_region_type = 'UI'
    bl_category    = "Strip"
    
    @classmethod
    def poll(self, context):
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
        
        layout.prop(props, "autocorrect_action")
        layout.prop(props, "category")
        
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


OBJECT_PT_GFSToolsAnimationGenericPropertyPanel = makeCustomPropertiesPanel(
    "OBJECT_PT_GFSToolsAnimationPanel",
    "Anim",
    "NLA_EDITOR",
    "UI",
    "Strip",
    lambda context: context.active_nla_strip.action.GFSTOOLS_AnimationProperties,
    lambda cls, context: True
    )
