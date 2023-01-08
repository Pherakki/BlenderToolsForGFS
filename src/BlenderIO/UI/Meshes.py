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
        
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_5")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_7")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_8")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_9")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_10")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_11")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_13")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_14")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_15")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_16")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_17")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_18")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_19")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_20")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_21")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_22")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_23")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_24")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_25")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_26")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_27")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_28")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_29")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_30")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "flag_31")

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
        