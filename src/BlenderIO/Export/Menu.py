import bpy

from .Operator import ExportGFS


class GFSExportSubmenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_GFSImportExport_export_submenu"
    bl_label = "GFS"

    def draw(self, context):
        layout = self.layout
        layout.operator(ExportGFS.bl_idname, text="GFS Model (.GMD, .GFS)")


def menu_func_export(self, context):
    self.layout.menu(GFSExportSubmenu.bl_idname)
