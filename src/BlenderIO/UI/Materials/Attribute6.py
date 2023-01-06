import bpy


class OBJECT_PT_GFSToolsMaterialAttributeType6Panel(bpy.types.Panel):
    bl_label       = "Attribute 6"
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
        layout.prop(mat.GFSTOOLS_MaterialProperties, "has_a6", text="")

    def draw(self, context):
        mat = context.material
        layout = self.layout
        
        ctr = layout.column()
        
        # Could remove boxes by changing this to an if statement
        ctr.active = mat.GFSTOOLS_MaterialProperties.has_a6

        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_unknown_0x00")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_unknown_0x04")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_unknown_0x08")
        
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_0")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_1")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_2")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_3")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_4")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_5")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_6")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_7")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_8")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_9")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_10")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_11")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_12")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_13")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_14")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a6_ctr_flag_15")
