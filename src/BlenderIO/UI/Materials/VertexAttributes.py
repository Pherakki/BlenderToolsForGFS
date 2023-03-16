import bpy


class OBJECT_PT_GFSToolsMaterialVertexAttributePanel(bpy.types.Panel):
    bl_label       = "Vertex Attributes"
    bl_parent_id   = "OBJECT_PT_GFSToolsMaterialPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "material"
    bl_options     = set()
    
    @classmethod
    def poll(self, context):
        return context.material is not None

    def draw(self, context):
        mat = context.material
        layout = self.layout
        
        ctr = layout.column()
        
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "requires_normals")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "requires_tangents")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "requires_binormals")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "requires_color0s")
        ctr.prop(mat.GFSTOOLS_MaterialProperties, "requires_color1s")
