import bpy

from .Operator import ImportGFS, ImportGAP, ImportEPL


class GFSImportSubmenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_GFSImportExport_import_submenu"
    bl_label = "GFS (.GMD, .GFS, .GAP)"

    def draw(self, context):
        layout = self.layout
        layout.operator(ImportGFS.bl_idname, text="GFS Model (.GMD, .GFS)")
        layout.operator(ImportGAP.bl_idname, text="GAP Animations (.GAP)")
        layout.operator(ImportEPL.bl_idname, text="EPLs (.EPL)")
    

def menu_func_import(self, context):
    self.layout.menu(GFSImportSubmenu.bl_idname)
