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
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_2")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_3")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "vertex_colors")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_5")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_6")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "light_1")
        layout.prop(mat.GFSTOOLS_MaterialProperties, "flag_8")
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
        
        # Forgot to import the main material data here...
        # oops
