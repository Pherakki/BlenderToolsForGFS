import bpy


class OBJECT_PT_GFSToolsMaterialPanel(bpy.types.Panel):
    bl_label       = "GFS Material"
    bl_idname      = "OBJECT_PT_GFSToolsMaterialPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "material"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return context.material is not None

    def draw(self, context):
        mat = context.material
        layout = self.layout
        
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_0")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_1")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_3")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "vertex_colors")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_5")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_6")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "enable_uv_anims")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_9")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_10")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "light_2")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "pwire")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_13")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "receive_shadow")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "cast_shadow")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_17")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_18")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "disable_bloom")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_29")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_30")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_31")
        
        # Colours
        layout.prop(mat.GFSTools.MaterialProperties, "ambient")
        layout.prop(mat.GFSTools.MaterialProperties, "diffuse")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "enable_specular")
        if mat.GFSTOOLS_MaterialProperties.enable_specular:
            layout.prop(mat.GFSTools.MaterialProperties, "specular")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "enable_emissive")
        if mat.GFSTOOLS_MaterialProperties.enable_emission:
            layout.prop(mat.GFSTools.MaterialProperties, "emissive")
            
        layout.prop(mat.GFSTools.MaterialProperties, "reflectivity")
        layout.prop(mat.GFSTools.MaterialProperties, "outline_idx")
        layout.prop(mat.GFSTools.MaterialProperties, "draw_method")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x51")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x52")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x53")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x54")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x55")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x56")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x58")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x5A")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x5C")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x5E")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x68")
        layout.prop(mat.GFSTools.MaterialProperties, "unknown_0x6A")
