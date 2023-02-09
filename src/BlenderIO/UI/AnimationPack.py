import bpy


class OBJECT_PT_GFSToolsAnimationPackDataPanel(bpy.types.Panel):
    bl_label       = "GFS Animation Pack"
    bl_idname      = "OBJECT_PT_GFSToolsAnimationPackDataPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return context.armature is not None

    def draw(self, context):
        armature = context.armature
        layout = self.layout
        
        props = armature.GFSTOOLS_AnimationPackProperties
        
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
