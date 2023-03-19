from .src.FileFormats.GFS import GFSBinary, GFSInterface
    
bl_info = {
        "name": "GFS Import/Export (.GMD/.GAP/.GFS)",
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

def init_bpy():
    import bpy
    
    from .src.BlenderIO.Preferences import AddonPreferences
    from .src.BlenderIO.Import      import ImportGFS, ImportGAP
    from .src.BlenderIO.Import.Menu import GFSImportSubmenu, menu_func_import
    from .src.BlenderIO.Export      import ExportGFS, ExportGAP
    from .src.BlenderIO.Export.Menu import GFSExportSubmenu, menu_func_export
    from .src.BlenderIO.Properties.Animations    import GFSToolsAnimationProperties
    from .src.BlenderIO.Properties.AnimationPack import GFSToolsAnimationPackProperties
    from .src.BlenderIO.Properties.Bones         import GFSToolsBoneNodeProperties
    from .src.BlenderIO.Properties.Cameras       import GFSToolsCameraProperties
    from .src.BlenderIO.Properties.GFSProperties import GFSToolsGenericProperty
    from .src.BlenderIO.Properties.Lights        import GFSToolsLightProperties
    from .src.BlenderIO.Properties.Materials     import GFSToolsTextureRefPanelProperties
    from .src.BlenderIO.Properties.Materials     import GFSToolsMaterialProperties
    from .src.BlenderIO.Properties.Meshes        import GFSToolsMeshProperties, GFSToolsMeshNodeProperties
    from .src.BlenderIO.Properties.Model         import GFSToolsModelProperties, GFSToolsModelNodeProperties
    from .src.BlenderIO.Properties.Nodes         import BlobProperty
    from .src.BlenderIO.Properties.Textures      import GFSToolsImageProperties
    from .src.BlenderIO.UI.Animation             import OBJECT_PT_GFSToolsAnimationPanel
    from .src.BlenderIO.UI.Animation             import OBJECT_PT_GFSToolsAnimationGenericPropertyPanel
    from .src.BlenderIO.UI.AnimationPack         import OBJECT_PT_GFSToolsAnimationPackDataPanel
    from .src.BlenderIO.UI.Bones         import OBJECT_PT_GFSToolsBonePropertiesPanel
    from .src.BlenderIO.UI.Cameras       import OBJECT_PT_GFSToolsCameraAttributesPanel
    from .src.BlenderIO.UI.GFSProperties import OBJECT_UL_GFSToolsGenericPropertyUIList
    from .src.BlenderIO.UI.HelpWindows   import OpenDocumentation
    from .src.BlenderIO.UI.Lights        import OBJECT_PT_GFSToolsLightAttributesPanel
    from .src.BlenderIO.UI.Materials     import OBJECT_PT_GFSToolsMaterialPanel
    from .src.BlenderIO.UI.Materials     import OBJECT_PT_GFSToolsMaterialToonShadingAttributePanel
    from .src.BlenderIO.UI.Materials     import OBJECT_PT_GFSToolsMaterialAttributeType1Panel
    from .src.BlenderIO.UI.Materials     import OBJECT_PT_GFSToolsMaterialOutlineAttributePanel
    from .src.BlenderIO.UI.Materials     import OBJECT_PT_GFSToolsMaterialAttributeType3Panel
    from .src.BlenderIO.UI.Materials     import OBJECT_PT_GFSToolsMaterialAttributeType4Panel
    from .src.BlenderIO.UI.Materials     import OBJECT_PT_GFSToolsMaterialAttributeType5Panel
    from .src.BlenderIO.UI.Materials     import OBJECT_PT_GFSToolsMaterialAttributeType6Panel
    from .src.BlenderIO.UI.Materials     import OBJECT_PT_GFSToolsMaterialAttributeType7Panel
    from .src.BlenderIO.UI.Materials     import OBJECT_PT_GFSToolsMaterialVertexAttributePanel
    from .src.BlenderIO.UI.Meshes        import OBJECT_PT_GFSToolsMeshAttributesPanel
    from .src.BlenderIO.UI.Model         import OBJECT_PT_GFSToolsModelDataPanel
    from .src.BlenderIO.UI.RegisterWindow import RegisterWindow
    from .src.BlenderIO.UI.ShaderNodes   import OBJECT_PT_GFSToolsTextureRefPanel, OBJECT_PT_GFSToolsImagePanel
    from .src.BlenderIO.WarningSystem.UI import BasicErrorBox, BasicWarningBox, UnhandledErrorBox
    
    
    CLASSES = (
        AddonPreferences,
        ImportGFS,
        ImportGAP,
        GFSImportSubmenu,
        ExportGFS,
        ExportGAP,
        GFSExportSubmenu,
        BlobProperty,
        GFSToolsGenericProperty,
        RegisterWindow,
        OpenDocumentation,
        OBJECT_PT_GFSToolsAnimationPanel,
        OBJECT_PT_GFSToolsAnimationGenericPropertyPanel,
        OBJECT_PT_GFSToolsAnimationPackDataPanel,
        OBJECT_PT_GFSToolsBonePropertiesPanel,
        OBJECT_PT_GFSToolsCameraAttributesPanel,
        OBJECT_UL_GFSToolsGenericPropertyUIList,
        OBJECT_PT_GFSToolsLightAttributesPanel,
        OBJECT_PT_GFSToolsMaterialPanel,
        OBJECT_PT_GFSToolsMaterialToonShadingAttributePanel,
        OBJECT_PT_GFSToolsMaterialAttributeType1Panel,
        OBJECT_PT_GFSToolsMaterialOutlineAttributePanel,
        OBJECT_PT_GFSToolsMaterialAttributeType3Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType4Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType5Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType6Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType7Panel,
        OBJECT_PT_GFSToolsMaterialVertexAttributePanel,
        OBJECT_PT_GFSToolsMeshAttributesPanel,
        OBJECT_PT_GFSToolsModelDataPanel,
        OBJECT_PT_GFSToolsTextureRefPanel,
        OBJECT_PT_GFSToolsImagePanel,
        BasicErrorBox,
        BasicWarningBox,
        UnhandledErrorBox
    )
    
    PROP_GROUPS = (
        (bpy.types.Action,   "GFSTOOLS_AnimationProperties",       GFSToolsAnimationProperties      ),
        (bpy.types.Armature, "GFSTOOLS_AnimationPackProperties",   GFSToolsAnimationPackProperties  ),
        (bpy.types.Armature, "GFSTOOLS_ModelProperties",           GFSToolsModelProperties          ),
        (bpy.types.Armature, "GFSTOOLS_NodeProperties",            GFSToolsModelNodeProperties      ),
        (bpy.types.Bone,     "GFSTOOLS_NodeProperties",            GFSToolsBoneNodeProperties       ),
        (bpy.types.Camera,   "GFSTOOLS_CameraProperties",          GFSToolsCameraProperties         ),
        (bpy.types.Image,    "GFSTOOLS_ImageProperties",           GFSToolsImageProperties          ),
        (bpy.types.Light,    "GFSTOOLS_LightProperties",           GFSToolsLightProperties          ),
        (bpy.types.Material, "GFSTOOLS_MaterialProperties",        GFSToolsMaterialProperties       ),
        (bpy.types.Mesh,     "GFSTOOLS_MeshProperties",            GFSToolsMeshProperties           ),
        (bpy.types.Mesh,     "GFSTOOLS_NodeProperties",            GFSToolsMeshNodeProperties       ),
        (bpy.types.Node,     "GFSTOOLS_TextureRefPanelProperties", GFSToolsTextureRefPanelProperties)
    )
    
    
    LIST_ITEMS = (
        (bpy.types.TOPBAR_MT_file_import, menu_func_import),
        (bpy.types.TOPBAR_MT_file_export, menu_func_export)
    )
    
    return CLASSES, PROP_GROUPS, LIST_ITEMS


def register():
    import bpy
    
    CLASSES, PROP_GROUPS, LIST_ITEMS = init_bpy()
    
    blender_version = bpy.app.version_string  # Can use this string to switch version-dependent Blender API codes
   # Note for later: multi-language support can be implemented by checking
   #     - bpy.context.preferences.view.language
   #     - bpy.context.preferences.view.use_translate_interface
   #     - bpy.context.preferences.view.use_translate_new_dataname
   #     - bpy.context.preferences.view.use_translate_tooltips
    for classtype in CLASSES:
        bpy.utils.register_class(classtype)
    
    for obj, name, prop_type in PROP_GROUPS:
        bpy.utils.register_class(prop_type)
        setattr(obj, name, bpy.props.PointerProperty(type=prop_type))
        
    for obj, elem in LIST_ITEMS:
        obj.append(elem)
     
    # Apparently not allowed to do this. Would be handy though to direct users...  
    # bpy.ops.gfstools.registerwindow('INVOKE_DEFAULT')


def unregister():
    import bpy
    
    CLASSES, PROP_GROUPS, LIST_ITEMS = init_bpy()
    
    for classtype in CLASSES[::-1]:
        bpy.utils.unregister_class(classtype)

    for obj, name, prop_type in PROP_GROUPS[::-1]:
        delattr(obj, name)
        bpy.utils.unregister_class(prop_type)
        
    for obj, elem in LIST_ITEMS:
        obj.remove(elem)
        