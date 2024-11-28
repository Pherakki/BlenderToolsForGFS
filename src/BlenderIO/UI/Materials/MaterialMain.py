import bpy

from ..HelpWindows import defineHelpWindow


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
        
        layout.operator(self.MaterialHelpWindow.bl_idname)
        
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
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_18")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "disable_bloom")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "extra_distortion")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_31")
        
        layout.prop(mat.GFSTOOLS_MaterialProperties, "enable_specular")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "enable_emissive")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "shader_type")
        mat.GFSTOOLS_MaterialProperties.shader_params.draw(layout, mat.GFSTOOLS_MaterialProperties)
        layout.prop(mat.GFSTOOLS_MaterialProperties, "draw_method")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x51")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x52")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x53")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x54")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x55")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x56")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x58")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x5A")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x5C")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x5E")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x6A")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "unknown_0x6C")
        
        props = mat.GFSTOOLS_MaterialProperties
        
        uvs_row = layout.row()
        label_col = uvs_row.column()
        in_uv_col = uvs_row.column()
        out_uv_col = uvs_row.column()
        label_col.label(text="")
        label_col.label(text="Diffuse")
        label_col.label(text="Normal")
        label_col.label(text="Specular")
        label_col.label(text="Reflection")
        label_col.label(text="Highlight")
        label_col.label(text="Glow")
        label_col.label(text="Night")
        label_col.label(text="Detail")
        label_col.label(text="Shadow")
        label_col.label(text="Texture 10")
        in_uv_col.label(text="In UV")
        in_uv_col.prop(props,  "diffuse_uv_in")
        in_uv_col.prop(props,  "normal_uv_in")
        in_uv_col.prop(props,  "specular_uv_in")
        in_uv_col.prop(props,  "reflection_uv_in")
        in_uv_col.prop(props,  "highlight_uv_in")
        in_uv_col.prop(props,  "glow_uv_in")
        in_uv_col.prop(props,  "night_uv_in")
        in_uv_col.prop(props,  "detail_uv_in")
        in_uv_col.prop(props,  "shadow_uv_in")
        in_uv_col.prop(props,  "tex10_uv_in")
        out_uv_col.label(text="Out UV")
        out_uv_col.prop(props, "diffuse_uv_out")
        out_uv_col.prop(props, "normal_uv_out")
        out_uv_col.prop(props, "specular_uv_out")
        out_uv_col.prop(props, "reflection_uv_out")
        out_uv_col.prop(props, "highlight_uv_out")
        out_uv_col.prop(props, "glow_uv_out")
        out_uv_col.prop(props, "night_uv_out")
        out_uv_col.prop(props, "detail_uv_out")
        out_uv_col.prop(props, "shadow_uv_out")
        out_uv_col.prop(props, "tex10_uv_out")
    
    MaterialHelpWindow = defineHelpWindow("Material", 
        "Materials are very complicated and are better described by the documentation rather than a tooltip."
    )

    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.MaterialHelpWindow)
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.MaterialHelpWindow)
    