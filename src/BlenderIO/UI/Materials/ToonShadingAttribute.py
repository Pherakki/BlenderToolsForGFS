import bpy


class OBJECT_PT_GFSToolsMaterialToonShadingAttributePanel(bpy.types.Panel):
    bl_label       = "Toon Shading"
    bl_parent_id   = "OBJECT_PT_GFSToolsMaterialPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "material"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return context.material is not None

    def draw_header(self, context):
        mat = context.material
        layout = self.layout
        layout.prop(mat.GFSTOOLS_MaterialProperties, "has_toon", text="")

    def draw(self, context):
        mat = context.material
        layout = self.layout
        
        ctr = layout.column()
        
        # Could remove boxes by changing this to an if statement
        ctr.active = mat.GFSTOOLS_MaterialProperties.has_toon
        
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_colour")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_light_threshold")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_light_factor")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_light_brightness")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_shadow_threshold")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_shadow_factor")
        
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_0")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_1")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_2")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_3")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_4")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_5")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_6")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_7")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_8")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_9")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_10")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_11")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_12")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_13")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_14")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_ctr_flag_15")
        
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_0")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_1")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_2")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_3")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_4")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_5")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_6")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_7")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_8")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_9")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_10")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_11")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_12")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_13")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_14")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_15")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_16")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_17")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_18")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_19")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_20")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_21")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_22")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_23")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_24")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_25")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_26")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_27")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_28")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_29")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_30")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "toon_flag_31")
