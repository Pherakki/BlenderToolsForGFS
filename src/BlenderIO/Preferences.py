import os

import bpy

from .Data import get_package_name, available_versions_property

    
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
    
    version: available_versions_property()

    
    def draw(self, context):
        layout = self.layout
        
        io_row = layout.row()
        import_col = io_row.column()
        import_col.label(text='Default Import settings:')
        import_col.prop(self, 'merge_vertices')
        import_col.prop(self, 'set_fps')
        
        export_col = io_row.column()
        export_col.label(text='Default Export settings:')
        export_col.prop(self, 'strip_missing_vertex_groups')
        export_col.prop(self, 'recalculate_tangents')
        export_col.prop(self, 'version')
