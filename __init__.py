# Check if we're running a Blender instance
try:
    import bpy
except:
    pass

from .src.FileFormats.GFS.GFSBinary import GFS0Binary
    
bl_info = {
        "name": "GFS Import/Export (.GMD)",
        "description": "Imports GFS files.",
        "author": "Pherakki",
        "version": (0, 2),
        "blender": (2, 80, 0),
        "location": "File > Import, File > Export",
        "warning": "",
        #"wiki_url": "https://github.com/Pherakki/Blender-Tools-for-DSCS",
        #"tracker_url": "https://github.com/Pherakki/Blender-Tools-for-DSCS/issues",
        "category": "Import-Export",
        }
    
# Disable bpy setup if we're running the tools outside of Blender
if "bpy" in locals():
    from .src.BlenderIO.Import import ImportGFS
    from .src.BlenderIO.Utils.ErrorPopup import MessagePopup

    
    
    class GFSImportSubmenu(bpy.types.Menu):
        bl_idname = "OBJECT_MT_GFSImportExport_import_submenu"
        bl_label = "GFS"
    
        def draw(self, context):
            layout = self.layout
            layout.operator(ImportGFS.bl_idname, text="GFS Model (.GMD)")
    
    
    # class GFSExportSubmenu(bpy.types.Menu):
    #     bl_idname = "OBJECT_MT_GFSImportExport_export_submenu"
    #     bl_label = "GFS"
    
    #     def draw(self, context):
    #         layout = self.layout
    #         layout.operator(ExportDSCS.bl_idname, text="GFS Model (.GMD)")
    
    
    def menu_func_import(self, context):
        self.layout.menu(GFSImportSubmenu.bl_idname)
    
    
    # def menu_func_export(self, context):
    #     self.layout.menu(GFSExportSubmenu.bl_idname)
    
    
    def register():
        blender_version = bpy.app.version_string  # Can use this string to switch version-dependent Blender API codes
       
        bpy.utils.register_class(ImportGFS)
        bpy.utils.register_class(GFSImportSubmenu)
        bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
        
        # bpy.utils.register_class(ExportGFS)
        # bpy.utils.register_class(GFSExportSubmenu)
        # bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
        
        bpy.utils.register_class(MessagePopup)
    
    
    def unregister():
        bpy.utils.unregister_class(ImportGFS)
        bpy.utils.unregister_class(GFSImportSubmenu)
        bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
        
        # bpy.utils.unregister_class(ExportGFS)
        # bpy.utils.unregister_class(GFSExportSubmenu)
        # bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
        
        bpy.utils.unregister_class(MessagePopup)
