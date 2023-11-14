import os

import bpy

from .Data import get_package_name
from .Data import bone_pose_enum_options
from .Data import anim_boundbox_policy_options
from .Data import too_many_vertices_policy_options
from .Data import too_many_vertex_groups_policy_options
from .Data import multiple_materials_policy_options
from .Data import missing_uv_maps_policy_options
from .Data import triangulate_mesh_policy_options
from .Data import version_override_options
from .UI.HelpWindows import OpenDocumentation

    
def get_preferences():
    return bpy.context.preferences.addons[get_package_name()].preferences


class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = get_package_name()

    ##################
    ## GLOBAL STATE ##
    ##################
    initialized: bpy.props.BoolProperty(default=False)
    developer_mode: bpy.props.BoolProperty(name="Developer Mode",
                                           description="Enables Experimental and Developer features",
                                           default=False)
    ############
    ## IMPORT ##
    ############
    align_quats : bpy.props.BoolProperty(
        name="Align Animation Quaternions",
        description="Default setting for 'Align Animation Quaternions' on import",
        default=False
    )
    
    anim_boundbox_policy: bpy.props.EnumProperty(
        items=anim_boundbox_policy_options(),
        name="Animation Bounding Boxes",
        description="Default setting for 'Animation Bounding Boxes' on export",
        default="AUTO")
    
    merge_vertices : bpy.props.BoolProperty(
        name="Merge Vertices",
        description="Default setting for 'Merge Vertices' on import",
        default=True
    )
    
    set_fps: bpy.props.BoolProperty(
        name="Set FPS to 30",
        description="Default setting for 'Set FPS to 30' on import",
        default=True
    )
    
    set_clip: bpy.props.BoolProperty(
        name="Set Maximum Clip to 1000000",
        description="Default setting for 'Set P5R Screen Clip' on import",
        default=True
    )
    
    bone_pose: bpy.props.EnumProperty(
        name="Bind Pose",
        description="Default setting for 'Bind Pose' on import",
        items=bone_pose_enum_options(),
        default="bindpose"
    )
    
    connect_child_bones: bpy.props.BoolProperty(
        name="Connect Child Bones",
        description="Default setting for 'Connect Child Bones' policy",
        default=False
    )
    
    ############
    ## EXPORT ##
    ############
    combine_new_mesh_nodes: bpy.props.BoolProperty(
        name="Combine New Mesh Nodes",
        default=False
    )
    
    strip_missing_vertex_groups: bpy.props.BoolProperty(
        name="Strip Missing Vertex Groups",
        description="Default setting for 'Strip Missing Vertex Groups' on export",
        default=False
    )
    
    recalculate_tangents: bpy.props.BoolProperty(
        name="Recalculate Tangents",
        description="Default setting for 'Recalculate Tangents' on export",
        default=True
    )
    
    throw_missing_weight_errors: bpy.props.BoolProperty(
        name="Raise Error for Unrigged Vertices",
        description="Default setting for 'Raise Error for Unrigged Vertices' on export",
        default=False
    )
    
    too_many_vertices_policy: bpy.props.EnumProperty(
        items=too_many_vertices_policy_options(),
        name=">6192 Vertices",
        description="Default setting for '>6192 Vertices' on export",
        default="WARN"
    )
    
    too_many_vertex_groups_policy: bpy.props.EnumProperty(
        items=too_many_vertex_groups_policy_options(),
        name="Vertex Group Limits",
        description="Default setting for 'Vertex Group Limits' on export",
        default="ERROR"
    )
    
    multiple_materials_policy: bpy.props.EnumProperty(
        items=multiple_materials_policy_options(),
        name="Multiple Materials per Mesh",
        description="Default setting for 'Multiple Materials per Mesh' on export",
        default="WARN"
    )
        
    missing_uv_maps_policy: bpy.props.EnumProperty(
        items=missing_uv_maps_policy_options(),
        name="Missing UV Maps",
        description="Default setting for 'Missing UV Maps' on export",
        default="WARN"
    )
    
    triangulate_mesh_policy: bpy.props.EnumProperty(
        items=triangulate_mesh_policy_options(),
        name="Triangulate Meshes",
        description="Default setting for 'Triangulate Meshes' on export",
        default="ERROR")
    
    version_override: bpy.props.EnumProperty(
        items=version_override_options(),
        name="Export Version",
        description="Default setting for 'Export Version' on export",
        default="DEFAULT"
    )
    
    
    def draw(self, context):
        layout = self.layout
        
        dev_row = layout.row()
        dev_row.prop(self, 'developer_mode')

        io_row = layout.row()
        import_col = io_row.column()
        import_col.label(text='Default Import settings:')
        import_col.prop(self, 'align_quats')
        import_col.prop(self, "anim_boundbox_policy")
        import_col.prop(self, 'merge_vertices')
        import_col.prop(self, 'set_fps')
        import_col.prop(self, 'set_clip')
        import_col.prop(self, 'bone_pose')
        import_col.prop(self, 'connect_child_bones')
        
        export_col = io_row.column()
        export_col.label(text='Default Export settings:')
        export_col.prop(self, 'version_override')
        export_col.prop(self, 'strip_missing_vertex_groups')
        export_col.prop(self, 'recalculate_tangents')
        export_col.prop(self, 'throw_missing_weight_errors')
        export_col.prop(self, 'too_many_vertices_policy')
        export_col.prop(self, 'too_many_vertex_groups_policy')
        export_col.prop(self, 'multiple_materials_policy')
        export_col.prop(self, 'missing_uv_maps_policy')
        export_col.prop(self, 'triangulate_mesh_policy')
        
        docs_row = layout.row()
        docs_row.operator(OpenDocumentation.bl_idname)
        
