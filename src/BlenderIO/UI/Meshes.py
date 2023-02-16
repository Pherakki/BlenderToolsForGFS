import bpy
from .Node import makeNodePropertiesPanel

class OBJECT_PT_GFSToolsMeshAttributesPanel(bpy.types.Panel):
    bl_label       = "GFS Mesh"
    bl_idname      = "OBJECT_PT_GFSToolsMeshAttributesPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return context.mesh is not None

    def draw(self, context):
        mesh = context.mesh
        layout = self.layout
        
        ctr = layout.column()
        
        # Bounding volumes
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "export_bounding_box")
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "export_bounding_sphere")
        
        # Vertex properties
        # Normals
        ctr.prop(mesh.GFSTOOLS_MeshProperties, "export_normals")
        has_uv_maps = (len(mesh.uv_layers) > 0)
        # Tangents
        row_tangent = ctr.row()
        row_tangent.prop(mesh.GFSTOOLS_MeshProperties, "export_tangents")
        row_tangent.active = has_uv_maps
        # Binormals
        row_binormal = ctr.row()
        row_binormal.prop(mesh.GFSTOOLS_MeshProperties, "export_binormals")
        row_binormal.active = has_uv_maps
        
        # Flags
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

    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.NodePropertiesPanel)
        bpy.utils.register_class(cls.OBJECT_PT_GFSToolsMeshUnknownFloatsPanel)
        
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.NodePropertiesPanel)
        bpy.utils.unregister_class(cls.OBJECT_PT_GFSToolsMeshUnknownFloatsPanel)
    
    class DummyType:
        type = None
    
    NodePropertiesPanel = makeNodePropertiesPanel(
        "MeshNode", 
        "PROPERTIES",
        "WINDOW",
        "data", 
        lambda context: context.mesh.GFSTOOLS_NodeProperties,
        lambda cls, context: context.mesh is not None and getattr(context.active_object, "parent", OBJECT_PT_GFSToolsMeshAttributesPanel.DummyType).type != "MESH",
        parent_id="OBJECT_PT_GFSToolsMeshAttributesPanel"
    )        

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
            