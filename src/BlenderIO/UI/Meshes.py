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
        bpy_armature_object = context.active_object.get_armature()
        bones = bpy_armature_object.data.bones
        if oprops.is_root_unrigged():
            return bpy_armature_object.GFSTOOLS_NodeProperties
        else:
            if    oprops.is_rigged(): bone_name = oprops.node
            else:                     bone_name = bpy_object.vertex_groups[0].name
            return bones[bone_name].GFSTOOLS_NodeProperties


def get_armature_bones(self, context):
    return [b.name for b in context.active_object.GFSTOOLS_ObjectProperties.get_armature().data.bones]


def get_armature_enum(self, context):
    return [(name, name, "") for name in get_armature_bones(self, context)]


class ConvertToUnriggedMesh(bpy.types.Operator):
    bl_idname = "gfstools.converttounrigged"
    bl_label = "Convert To Unrigged"
    bl_property = "bone_name"
    bl_options = {'REGISTER', 'UNDO'}

    bone_name: bpy.props.EnumProperty(items=get_armature_enum)
    
    @classmethod
    def poll(cls, context):
        if context is None:
            return False
        if context.active_object is None:
            return False
        if context.active_object.type != "MESH":
            return False
        if not context.active_object.GFSTOOLS_ObjectProperties.is_valid_mesh():
            return False
        
        return context.active_object.GFSTOOLS_ObjectProperties.is_mesh()
        
    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}

    def execute(self, context):
        bpy_mesh_object = context.active_object
        if self.bone_name not in set(get_armature_bones(self, context)):
            bpy_armature_object = bpy_mesh_object.GFSTOOLS_ObjectProperties.get_armature()
            self.report({'ERROR'}, f"'{self.bone_name}' is not a bone in '{bpy_armature_object.name}'")
            return {'CANCELLED'}
        for vg in list(bpy_mesh_object.vertex_groups):
            bpy_mesh_object.vertex_groups.remove(vg)
        vg = bpy_mesh_object.vertex_groups.new(name=self.bone_name)
        vg.add(list(range(len(bpy_mesh_object.data.vertices))), 1, 'REPLACE')
        bpy_mesh_object.data.GFSTOOLS_MeshProperties.permit_unrigged_export = True
        self.report({'INFO'}, f"Made '{bpy_mesh_object.name}' a GFS Unrigged Mesh on bone '{self.bone_name}'")
        return {'FINISHED'}



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
        
        # Rigging data
        row = ctr.row()
        row.prop(oprops, "attach_mode_label")
        if not oprops.is_valid_mesh():
            return
        
        if oprops.is_rigged():
            label = oprops.attach_mode_label
            if label == oprops.RIGGED_NEW_NODE_INVALID:
                row.alert = True
            
            bpy_armature_object = bpy_mesh_object.parent
            
            #ctr.prop(oprops, "attach_mode")
            attach_mode = oprops.attach_mode
            if attach_mode == "NODE":
                row = ctr.row()
                row.prop_search(oprops, "node", bpy_armature_object.data, "bones")
                
            elif attach_mode == "MESH":
                ctr.prop(oprops, "merged_node")
        ctr.operator(ConvertToUnriggedMesh.bl_idname)
        
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
        bpy.utils.register_class(ConvertToUnriggedMesh)
        bpy.utils.register_class(cls.NodePropertiesPanel)
        bpy.utils.register_class(cls.MeshHelpWindow)
        bpy.utils.register_class(cls.OBJECT_PT_GFSToolsMeshUnknownFloatsPanel)
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(ConvertToUnriggedMesh)
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
        get_node_props,
        lambda cls, context: (context.active_object.GFSTOOLS_ObjectProperties.is_valid_mesh() and context.mesh.GFSTOOLS_MeshProperties.is_mesh() and getattr(getattr(context.active_object, "parent", OBJECT_PT_GFSToolsMeshAttributesPanel.DummyType), "type", None) != "MESH") 
                             if context.active_object is not None
                             else False,
        parent_id="OBJECT_PT_GFSToolsMeshAttributesPanel",
        #predraw=_draw_on_node
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
            