import bpy
from .HelpWindows import defineHelpWindow
from .Model import OBJECT_PT_GFSToolsModelDataPanel


class OBJECT_PT_GFSToolsAnimationPackDataPanel(bpy.types.Panel):
    bl_label       = "GFS Animation Pack"
    bl_parent_id   = OBJECT_PT_GFSToolsModelDataPanel.bl_idname
    bl_idname      = "OBJECT_PT_GFSToolsAnimationPackDataPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        if context.armature is None:
            return False
        
        bpy_armature = context.armature
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        if mprops.get_active_gap() is None:
            return False
        
        return True

    def draw(self, context):
        bpy_armature = context.armature
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        
        layout = self.layout
        
        layout.operator(self.AnimationPackHelpWindow.bl_idname)
        
        props = mprops.get_active_gap()
        
        layout.prop(props, 'version')
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
        flag_col.prop(props, "flag_23")
        flag_col.prop(props, "flag_24")
        flag_col.prop(props, "flag_25")
        flag_col.prop(props, "flag_26")
        flag_col.prop(props, "flag_27")
        flag_col.prop(props, "flag_28")
        flag_col.prop(props, "flag_29")
        flag_col.prop(props, "flag_30")
        flag_col.prop(props, "flag_31")
        
        # LookAts
        flag_col.prop(props, "has_lookat_anims")
        lookat_col = layout.column()
        lookat_col.prop(props, "lookat_up")
        lookat_col.prop(props, "lookat_up_factor")
        lookat_col.prop(props, "lookat_down")
        lookat_col.prop(props, "lookat_down_factor")
        lookat_col.prop(props, "lookat_left")
        lookat_col.prop(props, "lookat_left_factor")
        lookat_col.prop(props, "lookat_right")
        lookat_col.prop(props, "lookat_right_factor")
        
        lookat_col.enabled = props.has_lookat_anims

    AnimationPackHelpWindow = defineHelpWindow("AnimationPack",
        "- 'Unknown Flags' are unknown. Only Flag 3 appears to be used and may do something.\n"\
        "- 'LookAt Anims' are a set of animations for the four directions the character can look in.\n"\
    )
            
    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.AnimationPackHelpWindow)
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.AnimationPackHelpWindow)
