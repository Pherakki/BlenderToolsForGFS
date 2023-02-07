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
    
    from .src.BlenderIO.Import import ImportGFS, ImportGAP
    from .src.BlenderIO.Import.Menu import GFSImportSubmenu, menu_func_import
    from .src.BlenderIO.Export import ExportGFS
    from .src.BlenderIO.Export.Menu import GFSExportSubmenu, menu_func_export
    from .src.BlenderIO.Properties.Animations import GFSToolsAnimationProperties
    from .src.BlenderIO.Properties.Bones import GFSToolsBoneProperties
    from .src.BlenderIO.Properties.GFSProperties import GFSToolsGenericProperty
    from .src.BlenderIO.Properties.Lights import GFSToolsLightProperties
    from .src.BlenderIO.Properties.Materials import GFSToolsTextureRefPanelProperties
    from .src.BlenderIO.Properties.Materials import GFSToolsMaterialProperties
    from .src.BlenderIO.Properties.Meshes import GFSToolsMeshProperties
    from .src.BlenderIO.Properties.Model import GFSToolsModelProperties
    from .src.BlenderIO.UI.Animation import OBJECT_PT_GFSToolsAnimationPanel
    from .src.BlenderIO.UI.Bones import OBJECT_PT_GFSToolsBonePropertiesPanel
    from .src.BlenderIO.UI.Bones import OBJECT_PT_GFSToolsBoneGenericPropertyPanel
    from .src.BlenderIO.UI.Bones import OBJECT_OT_GFSToolsBoneGenericPropertyPanelAdd
    from .src.BlenderIO.UI.Bones import OBJECT_OT_GFSToolsBoneGenericPropertyPanelDel
    from .src.BlenderIO.UI.Bones import OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveUp
    from .src.BlenderIO.UI.Bones import OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveDown
    from .src.BlenderIO.UI.GFSProperties import OBJECT_UL_GFSToolsGenericPropertyUIList
    from .src.BlenderIO.UI.Lights import OBJECT_PT_GFSToolsLightAttributesPanel
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
    from .src.BlenderIO.UI.Model import OBJECT_PT_GFSToolsModelDataPanel
    from .src.BlenderIO.UI.PinnedArmature import OBJECT_PT_GFSToolsPinnedArmatureToolsPanel
    from .src.BlenderIO.UI.ShaderNodes import OBJECT_PT_GFSToolsTextureRefPanel
    from .src.BlenderIO.Utils.ErrorPopup import MessagePopup
    from .src.BlenderIO.WarningSystem.StateMachine import ErrorPopup, PreviousErrorOperator, NextErrorOperator
    
    
    CLASSES = (
        ImportGFS,
        ImportGAP,
        GFSImportSubmenu,
        ExportGFS,
        GFSExportSubmenu,
        MessagePopup,
        GFSToolsGenericProperty,
        OBJECT_PT_GFSToolsPinnedArmatureToolsPanel,
        OBJECT_PT_GFSToolsAnimationPanel,
        OBJECT_PT_GFSToolsTextureRefPanel,
        OBJECT_PT_GFSToolsMaterialPanel,
        OBJECT_PT_GFSToolsMaterialToonShadingAttributePanel,
        OBJECT_PT_GFSToolsMaterialAttributeType1Panel,
        OBJECT_PT_GFSToolsMaterialOutlineAttributePanel,
        OBJECT_PT_GFSToolsMaterialAttributeType3Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType4Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType5Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType6Panel,
        OBJECT_PT_GFSToolsMaterialAttributeType7Panel,
        OBJECT_PT_GFSToolsMeshAttributesPanel,
        OBJECT_PT_GFSToolsMeshUnknownFloatsPanel,
        OBJECT_PT_GFSToolsModelDataPanel,
        OBJECT_PT_GFSToolsBonePropertiesPanel,
        OBJECT_PT_GFSToolsBoneGenericPropertyPanel,
        OBJECT_OT_GFSToolsBoneGenericPropertyPanelAdd,
        OBJECT_OT_GFSToolsBoneGenericPropertyPanelDel,
        OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveUp,
        OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveDown,
        OBJECT_PT_GFSToolsLightAttributesPanel,
        OBJECT_UL_GFSToolsGenericPropertyUIList
        # ErrorPopup,
        # PreviousErrorOperator,
        # NextErrorOperator
    )
    
    PROP_GROUPS = (
        (bpy.types.Action,   "GFSTOOLS_AnimationProperties",       GFSToolsAnimationProperties      )
        (bpy.types.Node,     "GFSTOOLS_TextureRefPanelProperties", GFSToolsTextureRefPanelProperties),
        (bpy.types.Material, "GFSTOOLS_MaterialProperties",        GFSToolsMaterialProperties       ),
        (bpy.types.Mesh,     "GFSTOOLS_MeshProperties",            GFSToolsMeshProperties           ),
        (bpy.types.Bone,     "GFSTOOLS_BoneProperties",            GFSToolsBoneProperties           ),
        (bpy.types.Light,    "GFSTOOLS_LightProperties",           GFSToolsLightProperties          ),
        (bpy.types.Armature, "GFSTOOLS_ModelProperties",           GFSToolsModelProperties          )
    )
    
    
    LIST_ITEMS = (
        (bpy.types.TOPBAR_MT_file_import, menu_func_import),
        #(bpy.types.TOPBAR_MT_file_export, menu_func_export)
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
        