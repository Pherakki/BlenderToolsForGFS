import bpy
from .GFSProperties import OBJECT_PT_GFSToolsGenericPropertyPanel
from .GFSProperties import OBJECT_OT_GFSToolsGenericPropertyPanelAdd
from .GFSProperties import OBJECT_OT_GFSToolsGenericPropertyPanelDel
from .GFSProperties import OBJECT_OT_GFSToolsGenericPropertyPanelMoveUp
from .GFSProperties import OBJECT_OT_GFSToolsGenericPropertyPanelMoveDown


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
    

class OBJECT_PT_GFSToolsAnimationGenericPropertyPanel(OBJECT_PT_GFSToolsGenericPropertyPanel):
    bl_parent_id   = "OBJECT_PT_GFSToolsAnimationPanel"
    bl_space_type  = 'NLA_EDITOR'
    bl_region_type = 'UI'
    bl_context     = "Strip"
    
    @property
    def GFSTOOLS_addoperator(self):
        return OBJECT_OT_GFSToolsAnimationGenericPropertyPanelAdd.bl_idname
    
    @property
    def GFSTOOLS_deloperator(self):
        return OBJECT_OT_GFSToolsAnimationGenericPropertyPanelDel.bl_idname
    
    @property
    def GFSTOOLS_moveupoperator(self):
        return OBJECT_OT_GFSToolsAnimationGenericPropertyPanelMoveUp.bl_idname
    
    @property
    def GFSTOOLS_movedownoperator(self):
        return OBJECT_OT_GFSToolsAnimationGenericPropertyPanelMoveDown.bl_idname
    
    def GFSTOOLS_get_obj(self, context):
        return context.active_nla_strip.action.GFSTOOLS_AnimationProperties
    

class OBJECT_OT_GFSToolsAnimationGenericPropertyPanelAdd(OBJECT_OT_GFSToolsGenericPropertyPanelAdd):
    bl_idname = "GFSTOOLS.OBJECT_OT_GFSToolsAnimGenericPropertyPanelAdd".lower()
    
    def GFSTOOLS_get_obj(self, context):
        return context.active_nla_strip.action.GFSTOOLS_AnimationProperties


class OBJECT_OT_GFSToolsAnimationGenericPropertyPanelDel(OBJECT_OT_GFSToolsGenericPropertyPanelDel):
    bl_idname = "GFSTOOLS.OBJECT_OT_GFSToolsAnimGenericPropertyPanelDel".lower()
    
    def GFSTOOLS_get_obj(self, context):
        return context.active_nla_strip.action.GFSTOOLS_AnimationProperties


class OBJECT_OT_GFSToolsAnimationGenericPropertyPanelMoveUp(OBJECT_OT_GFSToolsGenericPropertyPanelMoveUp):
    bl_idname = "GFSTOOLS.OBJECT_OT_GFSToolsAnimGenericPropertyPanelMoveUp".lower()
    
    def GFSTOOLS_get_obj(self, context):
        return context.active_nla_strip.action.GFSTOOLS_AnimationProperties


class OBJECT_OT_GFSToolsAnimationGenericPropertyPanelMoveDown(OBJECT_OT_GFSToolsGenericPropertyPanelMoveDown):
    bl_idname = "GFSTOOLS.OBJECT_OT_GFSToolsAnimGenericPropertyPanelMoveDown".lower()
    
    def GFSTOOLS_get_obj(self, context):
        return context.active_nla_strip.action.GFSTOOLS_AnimationProperties
