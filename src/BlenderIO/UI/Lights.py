import bpy


class OBJECT_PT_GFSToolsLightAttributesPanel(bpy.types.Panel):
    bl_label       = "GFS Light"
    bl_idname      = "OBJECT_PT_GFSToolsLightAttributesPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return context.light is not None

    def draw(self, context):
        light = context.light
        layout = self.layout
        
        
        ctr = layout.column()
        
        ctr.prop(light.GFSTOOLS_LightProperties, "color_1")
        ctr.prop(light.GFSTOOLS_LightProperties, "color_2")
        ctr.prop(light.GFSTOOLS_LightProperties, "color_3")
        
        ctr.prop(light.GFSTOOLS_LightProperties, "dtype")
        if light.GFSTOOLS_LightProperties.dtype == "TYPE1":
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x28")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x2C")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x30")
        elif light.GFSTOOLS_LightProperties.dtype == "SPHERE":
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x34")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x38")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x3C")
            ctr.prop(light.GFSTOOLS_LightProperties, "unk_setting")
            if light.GFSTOOLS_LightProperties.unk_setting:
                ctr.prop(light.GFSTOOLS_LightProperties, "blur_radius")
                ctr.prop(light.GFSTOOLS_LightProperties, "lum_radius")
            else:
                ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x48")
                ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x4C")
                ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x50")
        elif light.GFSTOOLS_LightProperties.dtype == "HEMISPHERE":
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x54")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x58")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x5C")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x60")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x64")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x68")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x6C")
            ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x70")
            ctr.prop(light.GFSTOOLS_LightProperties, "unk_setting")
            if light.GFSTOOLS_LightProperties.unk_setting:
                ctr.prop(light.GFSTOOLS_LightProperties, "blur_radius")
                ctr.prop(light.GFSTOOLS_LightProperties, "lum_radius")
            else:
                ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x7C")
                ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x80")
                ctr.prop(light.GFSTOOLS_LightProperties, "unknown_0x84")
        
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_0")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_2")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_3")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_4")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_5")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_6")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_7")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_8")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_9")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_10")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_11")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_12")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_13")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_14")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_15")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_16")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_17")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_18")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_19")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_20")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_21")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_22")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_23")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_24")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_25")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_26")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_27")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_28")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_29")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_30")
        ctr.prop(light.GFSTOOLS_LightProperties, "flag_31")
        