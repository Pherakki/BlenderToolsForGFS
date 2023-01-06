import bpy


class OBJECT_PT_GFSToolsMaterialAttributeType4Panel(bpy.types.Panel):
    bl_label       = "Attribute 4"
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
        layout.prop(mat.GFSTOOLS_MaterialProperties, "has_a4", text="")

    def draw(self, context):
        mat = context.material
        layout = self.layout
        
        ctr = layout.column()
        
        # Could remove boxes by changing this to an if statement
        ctr.active = mat.GFSTOOLS_MaterialProperties.has_a4
    
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x00")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x04")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x08")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x0C")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x10")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x14")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x18")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x1C")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x20")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x24")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x28")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x2C")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x30")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x34")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x38")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x3C")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x40")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x44")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x45")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_unknown_0x49")
        
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_0")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_1")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_2")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_3")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_4")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_5")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_6")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_7")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_8")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_9")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_10")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_11")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_12")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_13")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_14")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_ctr_flag_15")
        
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_0")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_1")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_2")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_3")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_4")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_5")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_6")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_7")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_8")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_9")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_10")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_11")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_12")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_13")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_14")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_15")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_16")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_17")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_18")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_19")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_20")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_21")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_22")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_23")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_24")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_25")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_26")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_27")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_28")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_29")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_30")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "a4_flag_31")
