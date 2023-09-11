import os

import bpy

from .Data import get_package_name
from .Data import available_versions_property
from .Data import bone_pose_enum_options
from .Data import too_many_vertices_policy_options
from .Data import multiple_materials_policy_options
from .Data import missing_uv_maps_policy_options

    
def get_preferences():
    return bpy.context.preferences.addons[get_package_name()].preferences


class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = get_package_name()

    merge_vertices : bpy.props.BoolProperty(
        name="Merge Vertices",
        description="Default setting for 'Merge Vertices' on import",
        default=True
    )
    
    set_fps: bpy.props.BoolProperty(
        name="Set FPS to 30",
        description="Default setting for 'Set FPS to 30' on import",
        default=False
    )
    
    bone_pose: bpy.props.EnumProperty(
        name="Bind Pose",
        description="Default setting for 'Bind Pose' on import",
        items=bone_pose_enum_options(),
        default="bindpose"
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
    
    version: available_versions_property()

    
    def draw(self, context):
        layout = self.layout
        
        io_row = layout.row()
        import_col = io_row.column()
        import_col.label(text='Default Import settings:')
        import_col.prop(self, 'merge_vertices')
        import_col.prop(self, 'set_fps')
        import_col.prop(self, 'bone_pose')
        
        export_col = io_row.column()
        export_col.label(text='Default Export settings:')
        export_col.prop(self, 'strip_missing_vertex_groups')
        export_col.prop(self, 'recalculate_tangents')
        export_col.prop(self, 'throw_missing_weight_errors')
        export_col.prop(self, 'too_many_vertices_policy')
        export_col.prop(self, 'multiple_materials_policy')
        export_col.prop(self, 'missing_uv_maps_policy')
        export_col.prop(self, 'version')
