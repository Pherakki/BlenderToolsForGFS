# Check if we're running a Blender instance
try:
    import bpy
except:
    pass

from .src.FileFormats.GFS import GFSBinary
    
bl_info = {
        "name": "GFS Import/Export (.GMD)",
        "description": "Imports GFS files.",
        "author": "Pherakki",
        "version": (0, 0, 1),
        "blender": (2, 81, 0),
        "location": "File > Import, File > Export",
        "warning": "",
        #"wiki_url": "https://github.com/Pherakki/BlenderToolsforGFS",
        #"tracker_url": "https://github.com/Pherakki/BlenderToolsforGFS/issues",
        "category": "Import-Export",
        }
    
# Disable bpy setup if we're running the tools outside of Blender
if "bpy" in locals():
    from .src.BlenderIO.Import import ImportGFS
    from .src.BlenderIO.Properties.Bones import GFSToolsBoneProperties
    from .src.BlenderIO.Properties.GFSProperties import GFSToolsGenericProperty
    from .src.BlenderIO.Properties.Materials import GFSToolsTextureRefPanelProperties
    from .src.BlenderIO.Properties.Materials import GFSToolsMaterialProperties
    from .src.BlenderIO.Properties.Meshes import GFSToolsMeshProperties
    from .src.BlenderIO.Tools import GFSToolsPinnedArmatureToolsPanel
    from .src.BlenderIO.UI.Bones import OBJECT_PT_GFSToolsBonePropertiesPanel
    from .src.BlenderIO.UI.Bones import OBJECT_PT_GFSToolsBoneGenericPropertyPanel
    from .src.BlenderIO.UI.Bones import OBJECT_OT_GFSToolsBoneGenericPropertyPanelAdd
    from .src.BlenderIO.UI.Bones import OBJECT_OT_GFSToolsBoneGenericPropertyPanelDel
    from .src.BlenderIO.UI.Bones import OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveUp
    from .src.BlenderIO.UI.Bones import OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveDown
    from .src.BlenderIO.UI.GFSProperties import OBJECT_UL_GFSToolsGenericPropertyUIList
    from .src.BlenderIO.UI.Materials import OBJECT_PT_GFSToolsMaterialPanel
    from .src.BlenderIO.UI.Materials import OBJECT_PT_GFSToolsMaterialToonShadingAttributePanel
    from .src.BlenderIO.UI.Materials import OBJECT_PT_GFSToolsMaterialAttributeType1Panel
    from .src.BlenderIO.UI.Materials import OBJECT_PT_GFSToolsMaterialOutlineAttributePanel
    from .src.BlenderIO.UI.Materials import OBJECT_PT_GFSToolsMaterialAttributeType3Panel
    from .src.BlenderIO.UI.Materials import OBJECT_PT_GFSToolsMaterialAttributeType4Panel
    from .src.BlenderIO.UI.Materials import OBJECT_PT_GFSToolsMaterialAttributeType5Panel
    from .src.BlenderIO.UI.Materials import OBJECT_PT_GFSToolsMaterialAttributeType6Panel
    from .src.BlenderIO.UI.Materials import OBJECT_PT_GFSToolsMaterialAttributeType7Panel
    from .src.BlenderIO.UI.Meshes import OBJECT_PT_GFSToolsMeshAttributesPanel
    from .src.BlenderIO.UI.Meshes import OBJECT_PT_GFSToolsMeshUnknownFloatsPanel
    from .src.BlenderIO.UI.ShaderNodes import OBJECT_PT_GFSToolsTextureRefPanel
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
    
    CLASSES = (
        ImportGFS,
        GFSImportSubmenu,
        #ExportGFS,
        #GFSExportSubmenu
        MessagePopup,
        GFSToolsGenericProperty,
        GFSToolsPinnedArmatureToolsPanel,
        OBJECT_PT_GFSToolsTextureRefPanel,
        OBJECT_PT_GFSToolsMaterialPanel,
        OBJECT_PT_GFSToolsMaterialToonShadingAttributePanel,
        OBJECT_PT_GFSToolsMaterialAttributeType1Panel,
        OBJECT_PT_GFSToolsMaterialOutlineAttributePanel,
        OBJECT_PT_GFSToolsMaterialAttributeType3Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType4Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType5Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType6Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType7Panel
        OBJECT_PT_GFSToolsMaterialAttributeType7Panel,
        OBJECT_PT_GFSToolsMeshAttributesPanel,
        OBJECT_PT_GFSToolsMeshUnknownFloatsPanel,
        OBJECT_PT_GFSToolsBonePropertiesPanel,
        OBJECT_PT_GFSToolsBoneGenericPropertyPanel,
        OBJECT_OT_GFSToolsBoneGenericPropertyPanelAdd,
        OBJECT_OT_GFSToolsBoneGenericPropertyPanelDel,
        OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveUp,
        OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveDown,
        OBJECT_UL_GFSToolsGenericPropertyUIList
    )
    
    PROP_GROUPS = (
        (bpy.types.Node,     "GFSTOOLS_TextureRefPanelProperties", GFSToolsTextureRefPanelProperties),
        (bpy.types.Material, "GFSTOOLS_MaterialProperties",        GFSToolsMaterialProperties       ),
        (bpy.types.Mesh,     "GFSTOOLS_MeshProperties",            GFSToolsMeshProperties           ),
        (bpy.types.Bone,     "GFSTOOLS_BoneProperties",            GFSToolsBoneProperties           ),
    )
    
    LIST_ITEMS = (
        (bpy.types.TOPBAR_MT_file_import, menu_func_import),
        #(bpy.types.TOPBAR_MT_file_export, menu_func_export)
    )
    
    def register():
        blender_version = bpy.app.version_string  # Can use this string to switch version-dependent Blender API codes
       
        for classtype in CLASSES:
            bpy.utils.register_class(classtype)
        
        for obj, name, prop_type in PROP_GROUPS:
            bpy.utils.register_class(prop_type)
            setattr(obj, name, bpy.props.PointerProperty(type=prop_type))
            
        for obj, elem in LIST_ITEMS:
            obj.append(elem)
    

    def unregister():
        for classtype in CLASSES[::-1]:
            bpy.utils.unregister_class(classtype)

        for obj, name, prop_type in PROP_GROUPS[::-1]:
            delattr(obj, name)
            bpy.utils.unregister_class(prop_type)
            
        for obj, elem in LIST_ITEMS:
            obj.remove(elem)
        