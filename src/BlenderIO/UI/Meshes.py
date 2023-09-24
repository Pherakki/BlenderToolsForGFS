import bpy
from .HelpWindows import defineHelpWindow
from .Node import makeNodePropertiesPanel


def _draw_on_node(context, layout):
    mesh = context.mesh
    layout = layout
    
    layout.prop(mesh.GFSTOOLS_NodeProperties, "override_name")


def get_node_props(context):
    bpy_object = context.active_object
    oprops = bpy_object.GFSTOOLS_ObjectProperties
    if oprops.requires_new_node():
        return context.mesh.GFSTOOLS_NodeProperties
    else:
        bone_name = bpy_object.vertex_groups[0].name
        bpy_armature_object = context.active_object.parent
        bones = bpy_armature_object.data.bones
        if    oprops.is_rigged(): bone_name = oprops.node
        else:                     bone_name = bpy_object.vertex_groups[0].name
        return bones[bone_name].GFSTOOLS_NodeProperties


class OBJECT_PT_GFSToolsMeshAttributesPanel(bpy.types.Panel):
    bl_label       = "GFS Mesh"
    bl_idname      = "OBJECT_PT_GFSToolsMeshAttributesPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        if context.mesh is not None:
            return context.mesh.GFSTOOLS_MeshProperties.is_mesh()
        
        return False

    def draw(self, context):
        bpy_mesh_object = context.active_object
        bpy_mesh        = context.mesh
        oprops          = bpy_mesh_object.GFSTOOLS_ObjectProperties
        mprops          = bpy_mesh.GFSTOOLS_MeshProperties
        
        layout = self.layout
        
        ctr = layout.column()
        
        # Help window
        ctr.operator(self.MeshHelpWindow.bl_idname)
        
        # Bounding volumes
        ctr.prop(mprops, "permit_unrigged_export") # Needs to go
        mprops.bounding_box.draw(ctr)
        mprops.bounding_sphere.draw(ctr)
        
        # Flags
        ctr.prop(mprops, "flag_5")
        ctr.prop(mprops, "flag_7")
        ctr.prop(mprops, "flag_8")
        ctr.prop(mprops, "flag_9")
        ctr.prop(mprops, "flag_10")
        ctr.prop(mprops, "flag_11")
        ctr.prop(mprops, "flag_13")
        ctr.prop(mprops, "flag_14")
        ctr.prop(mprops, "flag_15")
        ctr.prop(mprops, "flag_16")
        ctr.prop(mprops, "flag_17")
        ctr.prop(mprops, "flag_18")
        ctr.prop(mprops, "flag_19")
        ctr.prop(mprops, "flag_20")
        ctr.prop(mprops, "flag_21")
        ctr.prop(mprops, "flag_22")
        ctr.prop(mprops, "flag_23")
        ctr.prop(mprops, "flag_24")
        ctr.prop(mprops, "flag_25")
        ctr.prop(mprops, "flag_26")
        ctr.prop(mprops, "flag_27")
        ctr.prop(mprops, "flag_28")
        ctr.prop(mprops, "flag_29")
        ctr.prop(mprops, "flag_30")
        ctr.prop(mprops, "flag_31")

        ctr.prop(mprops, "unknown_0x12")

    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.NodePropertiesPanel)
        bpy.utils.register_class(cls.MeshHelpWindow)
        bpy.utils.register_class(cls.OBJECT_PT_GFSToolsMeshUnknownFloatsPanel)
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.NodePropertiesPanel)
        bpy.utils.unregister_class(cls.MeshHelpWindow)
        bpy.utils.unregister_class(cls.OBJECT_PT_GFSToolsMeshUnknownFloatsPanel)
    
    class DummyType:
        type = None
    
    NodePropertiesPanel = makeNodePropertiesPanel(
        "MeshNode", 
        "PROPERTIES",
        "WINDOW",
        "data", 
        lambda context: context.mesh.GFSTOOLS_NodeProperties,
        lambda cls, context: (context.mesh.GFSTOOLS_MeshProperties.is_mesh() and getattr(context.active_object, "parent", OBJECT_PT_GFSToolsMeshAttributesPanel.DummyType).type != "MESH") 
                             if context.mesh is not None
                             else False,
        parent_id="OBJECT_PT_GFSToolsMeshAttributesPanel",
        predraw=_draw_on_node
    )        
    
    MeshHelpWindow = defineHelpWindow("Mesh", 
        "- Export Bounding Mesh/Sphere will create a bounding volume on export.\n"\
        "- Export Normals / Tangents / Binormals will export these vertex attributes.\n"\
        "- The purpose of Unknown Flags is not known. Checking and unchecking these may cause or fix crashes.\n"\
        "- The purpose of unknown_0x12 is not known.\n"\
        "- The GFS Node sub-panel will appear if the Mesh is not parented under another Mesh."
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
            if context.mesh is not None:
                return context.mesh.GFSTOOLS_MeshProperties.is_mesh()
            return False
    
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
            