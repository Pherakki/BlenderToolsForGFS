import bpy


class OBJECT_PT_GFSToolsMeshAttributesPanel(bpy.types.Panel):
    bl_label       = "GFS Mesh"
    bl_idname      = "OBJECT_PT_GFSToolsMeshAttributesPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return context.mesh is not None

    def draw(self, context):
        mesh = context.mesh
        layout = self.layout
        
        ctr = layout.column()
        
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "export_bounding_box")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "export_bounding_sphere")
        
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_5", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_7", default=True)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_8", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_9", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_10", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_11", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_13", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_14", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_15", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_16", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_17", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_18", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_19", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_20", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_21", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_22", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_23", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_24", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_25", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_26", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_27", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_28", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_29", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_30", default=False)
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_31", default=True)

        ctr.prop(mesh.GFSTOOLS_MeshProperties, "unknown_0x12")
        

class OBJECT_PT_GFSToolsMeshUnknownFloatsPanel(bpy.types.Panel):
    bl_label       = "Unknown Floats"
    bl_parent_id   = "OBJECT_PT_GFSToolsMeshAttributesPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return context.mesh is not None

    def draw_header(self, context):
        mesh = context.mesh
        layout = self.layout
        layout.prop(mesh.GFSTOOLS_MeshProperties, "has_unknown_floats", text="")

    def draw(self, context):
        mesh = context.mesh
        layout = self.layout
        
        ctr = layout.column()

        ctr.active = mesh.GFSTOOLS_MeshProperties.has_unknown_floats

        ctr.prop(mesh.GFSTOOLS_MeshProperties, "unknown_float_1")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "unknown_float_2")
        