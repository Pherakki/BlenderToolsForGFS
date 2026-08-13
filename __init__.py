from .src.FileFormats.GFS import GFSBinary, GFSInterface
from .src.FileFormats.GFS import EPLFileBinary
    
bl_info = {
        "name": "GFS Import/Export (.GMD/.GAP/.GFS)",
        "description": "Imports GFS files.",
        "author": "Pherakki",
        "version": (0, 3, 1),
        "blender": (5, 2, 0),
        "location": "File > Import, File > Export",
        "warning": "",
        #"wiki_url": "https://github.com/Pherakki/BlenderToolsforGFS",
        #"tracker_url": "https://github.com/Pherakki/BlenderToolsforGFS/issues",
        "category": "Import-Export",
        }

def init_bpy():
    import bpy
    
    from .src.BlenderIO.Preferences import AddonPreferences
    from .src.BlenderIO.Import      import ImportGFS, ImportGAP, ImportEPL, ImportPolicies
    from .src.BlenderIO.Import.Menu import GFSImportSubmenu, menu_func_import
    from .src.BlenderIO.Export      import ExportGFS, ExportGAP, ExportPolicies
    from .src.BlenderIO.Export.Menu import GFSExportSubmenu, menu_func_export
    from .src.BlenderIO.Properties.AnimationPack  import BaseAnimBoundingBox
    from .src.BlenderIO.Properties.AnimationPack  import BaseAnimBoundingBoxProps
    from .src.BlenderIO.Properties.AnimationPack  import BlendAnimBoundingBox
    from .src.BlenderIO.Properties.AnimationPack  import BlendAnimBoundingBoxProps
    from .src.BlenderIO.Properties.AnimationPack  import LookAtAnimBoundingBox
    from .src.BlenderIO.Properties.AnimationPack  import LookAtAnimBoundingBoxProps
    from .src.BlenderIO.Properties.AnimationPack import GFSToolsAnimationPackProperties, NLAStripWrapper, NLATrackWrapper
    from .src.BlenderIO.Properties.AnimationPack import AnimationProperties
    from .src.BlenderIO.Properties.AnimationPack import BlendAnimationProperties
    from .src.BlenderIO.Properties.AnimationPack import LookAtAnimationProperties
    from .src.BlenderIO.Properties.AnimationPack import NodeAnimationProperties
    from .src.BlenderIO.Properties.AnimationPack import MaterialAnimationProperties
    from .src.BlenderIO.Properties.AnimationPack import CameraAnimationProperties
    from .src.BlenderIO.Properties.AnimationPack import Type4AnimationProperties
    from .src.BlenderIO.Properties.AnimationPack import MorphAnimationProperties
    from .src.BlenderIO.Properties.Bones         import GFSToolsBoneNodeProperties
    from .src.BlenderIO.Properties.Cameras       import GFSToolsCameraProperties
    from .src.BlenderIO.Properties.Clipboard     import GFSToolsClipboard
    from .src.BlenderIO.Properties.GFSProperties import GFSToolsGenericProperty
    from .src.BlenderIO.Properties.Lights        import GFSToolsLightProperties
    from .src.BlenderIO.Properties.Materials     import GFSToolsTextureRefPanelProperties
    from .src.BlenderIO.Properties.Materials     import GFSToolsMaterialProperties
    from .src.BlenderIO.Properties.MaterialShader import GFSToolsMaterialShaderPropsProperties
    from .src.BlenderIO.Properties.MaterialShader import Type0Flags
    from .src.BlenderIO.Properties.MaterialShader import Type2Flags
    from .src.BlenderIO.Properties.MaterialShader import Type4Flags
    from .src.BlenderIO.Properties.MaterialShader import WaterFlags
    from .src.BlenderIO.Properties.MaterialShader import Type6Flags
    from .src.BlenderIO.Properties.MaterialShader import Type7Flags
    from .src.BlenderIO.Properties.MaterialShader import Type9Flags
    from .src.BlenderIO.Properties.MaterialShader import Type10Flags
    from .src.BlenderIO.Properties.MaterialShader import Type12Flags
    from .src.BlenderIO.Properties.MaterialShader import Type15Flags
    from .src.BlenderIO.Properties.MaterialShader.V2Type15 import V2Type15Layer
    from .src.BlenderIO.Properties.Meshes        import MeshBoundingBox
    from .src.BlenderIO.Properties.Meshes        import MeshBoundingSphere
    from .src.BlenderIO.Properties.Meshes        import MeshBoundingBoxProps
    from .src.BlenderIO.Properties.Meshes        import MeshBoundingSphereProps
    from .src.BlenderIO.Properties.Meshes        import GFSToolsMeshProperties, GFSToolsMeshNodeProperties
    from .src.BlenderIO.Properties.Model         import GFSToolsModelProperties
    from .src.BlenderIO.Properties.Model         import GFSToolsModelNodeProperties
    from .src.BlenderIO.Properties.Model         import ModelBoundingBox
    from .src.BlenderIO.Properties.Model         import ModelBoundingSphere
    from .src.BlenderIO.Properties.Model         import ModelBoundingBoxProps
    from .src.BlenderIO.Properties.Model         import ModelBoundingSphereProps
    from .src.BlenderIO.Properties.Model         import UnusedTexture
    from .src.BlenderIO.Properties.Nodes         import BlobProperty
    from .src.BlenderIO.Properties.Object        import GFSToolsObjectProperties
    from .src.BlenderIO.Properties.Physics       import GFSToolsPhysicsProperties
    from .src.BlenderIO.Properties.Physics       import GFSToolsPhysicsBoneProperties
    from .src.BlenderIO.Properties.Physics       import GFSToolsBackendColliderProperties
    from .src.BlenderIO.Properties.Physics       import GFSToolsColliderProperties
    from .src.BlenderIO.Properties.Physics       import GFSToolsPhysicsLinkProperties
    from .src.BlenderIO.Properties.Scene         import GFSToolsSceneProperties
    from .src.BlenderIO.Properties.Textures      import GFSToolsImageProperties
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
    from .src.BlenderIO.UI.Model.PhysicsSubPanel import OBJECT_PT_GFSToolsColliderPanel
    from .src.BlenderIO.UI.RegisterWindow import RegisterWindow
    from .src.BlenderIO.UI.ShaderNodes   import OBJECT_PT_GFSToolsTextureRefPanel, OBJECT_PT_GFSToolsImagePanel
    from .src.BlenderIO.Globals          import ErrorLogger

    CLASSES = (
        AddonPreferences,
        ImportPolicies,
        ImportGFS,
        ImportGAP,
        ImportEPL,
        GFSImportSubmenu,
        ExportPolicies,
        ExportGFS,
        ExportGAP,
        GFSExportSubmenu,
        NLAStripWrapper,
        NLATrackWrapper,
        V2Type15Layer,
        Type15Flags,
        Type12Flags,
        Type10Flags,
        Type9Flags,
        Type7Flags,
        Type6Flags,
        WaterFlags,
        Type4Flags,
        Type2Flags,
        Type0Flags,
        GFSToolsMaterialShaderPropsProperties,
        NodeAnimationProperties,
        MaterialAnimationProperties,
        CameraAnimationProperties,
        Type4AnimationProperties,
        MorphAnimationProperties,
        BlobProperty,
        GFSToolsGenericProperty,
        RegisterWindow,
        OpenDocumentation,
        BaseAnimBoundingBox,
        BaseAnimBoundingBoxProps,
        BlendAnimBoundingBox,
        BlendAnimBoundingBoxProps,
        LookAtAnimBoundingBox,
        LookAtAnimBoundingBoxProps,
        UnusedTexture,
        ModelBoundingBox,
        ModelBoundingBoxProps,
        ModelBoundingSphere,
        ModelBoundingSphereProps,
        MeshBoundingBox,
        MeshBoundingBoxProps,
        MeshBoundingSphere,
        MeshBoundingSphereProps,
        AnimationProperties,
        BlendAnimationProperties,
        LookAtAnimationProperties,
        GFSToolsAnimationPackProperties,
        GFSToolsBackendColliderProperties,
        GFSToolsPhysicsBoneProperties,
        GFSToolsPhysicsLinkProperties,
        GFSToolsPhysicsProperties,
        GFSToolsClipboard,
        OBJECT_PT_GFSToolsBonePropertiesPanel,
        OBJECT_PT_GFSToolsCameraAttributesPanel,
        OBJECT_PT_GFSToolsColliderPanel,
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
    )
    
    PROP_GROUPS = (
        (bpy.types.Armature, "GFSTOOLS_ModelProperties",           GFSToolsModelProperties          ),
        (bpy.types.Armature, "GFSTOOLS_NodeProperties",            GFSToolsModelNodeProperties      ),
        (bpy.types.Bone,     "GFSTOOLS_NodeProperties",            GFSToolsBoneNodeProperties       ),
        (bpy.types.Camera,   "GFSTOOLS_CameraProperties",          GFSToolsCameraProperties         ),
        (bpy.types.Image,    "GFSTOOLS_ImageProperties",           GFSToolsImageProperties          ),
        (bpy.types.Light,    "GFSTOOLS_LightProperties",           GFSToolsLightProperties          ),
        (bpy.types.Material, "GFSTOOLS_MaterialProperties",        GFSToolsMaterialProperties       ),
        (bpy.types.Mesh,     "GFSTOOLS_ColliderProperties",        GFSToolsColliderProperties       ),
        (bpy.types.Mesh,     "GFSTOOLS_MeshProperties",            GFSToolsMeshProperties           ),
        (bpy.types.Mesh,     "GFSTOOLS_NodeProperties",            GFSToolsMeshNodeProperties       ),
        (bpy.types.Node,     "GFSTOOLS_TextureRefPanelProperties", GFSToolsTextureRefPanelProperties),
        (bpy.types.Object,   "GFSTOOLS_ObjectProperties",          GFSToolsObjectProperties         ),
        (bpy.types.Scene,    "GFSTOOLS_SceneProperties",           GFSToolsSceneProperties          )
    )
    
    # Blender 5.2 removed INFO_MT_file_import/export menus; only use TOPBAR menus
    LIST_ITEMS = (
        (bpy.types.TOPBAR_MT_file_import, menu_func_import),
        (bpy.types.TOPBAR_MT_file_export, menu_func_export),
    )
    
    MODULES = (
        ErrorLogger,
    )
    
    return CLASSES, PROP_GROUPS, LIST_ITEMS, MODULES



def register():
    import bpy
    import traceback
    from .src.BlenderIO.Preferences import get_preferences
    
    print("[GFSTools] === REGISTRATION START ===")
    
    def create_welcome_message():
        prefs = get_preferences()
        if not prefs.initialized:
            prefs.initialized = True
            try:
                bpy.ops.gfstools.registerwindow('INVOKE_DEFAULT')
            except Exception:
                traceback.print_exc()
    
    CLASSES, PROP_GROUPS, LIST_ITEMS, MODULES = init_bpy()
    print(f"[GFSTools] init_bpy() returned {len(CLASSES)} classes, {len(PROP_GROUPS)} prop groups, {len(LIST_ITEMS)} menu items")
    
    # Note for later: multi-language support can be implemented by checking
    #     - bpy.context.preferences.view.language
    #     - bpy.context.preferences.view.use_translate_interface
    #     - bpy.context.preferences.view.use_translate_new_dataname
    #     - bpy.context.preferences.view.use_translate_tooltips
    
    # Register classes
    print("[GFSTools] Registering classes...")
    for i, classtype in enumerate(CLASSES):
        try:
            bpy.utils.register_class(classtype)
            if 'Import' in classtype.__name__ or 'Export' in classtype.__name__:
                print(f"[GFSTools]   + {classtype.__name__} registered")
        except Exception as e:
            print(f"[GFSTools]   ERROR registering {classtype.__name__}: {e}")
            traceback.print_exc()
    
    # Register property groups
    print("[GFSTools] Registering property groups...")
    for obj, name, prop_type in PROP_GROUPS:
        try:
            bpy.utils.register_class(prop_type)
        except Exception as e:
            print(f"[GFSTools]   ERROR registering prop group {prop_type.__name__}: {e}")
            traceback.print_exc()
        try:
            setattr(obj, name, bpy.props.PointerProperty(type=prop_type))
        except Exception as e:
            print(f"[GFSTools]   ERROR setting property {name} on {obj}: {e}")
            traceback.print_exc()
    
    # Append menu items
    print("[GFSTools] Appending menu items...")
    for obj, elem in LIST_ITEMS:
        try:
            obj.append(elem)
            print(f"[GFSTools]   + Appended menu to {obj.__name__}")
        except Exception as e:
            print(f"[GFSTools]   ERROR appending menu to {obj}: {e}")
            traceback.print_exc()
    
    # Register modules
    print("[GFSTools] Registering modules...")
    for mod in MODULES:
        try:
            mod.register()
        except Exception as e:
            print(f"[GFSTools]   ERROR registering module {mod}: {e}")
            traceback.print_exc()
    
    # Check operator registration
    print("[GFSTools] Checking operator registration...")
    print(f"[GFSTools]   hasattr(bpy.ops.import_file, 'import_gfs') = {hasattr(bpy.ops.import_file, 'import_gfs')}")
    print(f"[GFSTools]   hasattr(bpy.ops.import_file, 'import_gap') = {hasattr(bpy.ops.import_file, 'import_gap')}")
    print(f"[GFSTools]   hasattr(bpy.ops.export_file, 'export_gfs') = {hasattr(bpy.ops.export_file, 'export_gfs')}")
    
    # Fire off the welcome message
    print("[GFSTools] Registering timer for welcome message...")
    try:
        bpy.app.timers.register(create_welcome_message, first_interval=.01)
        print("[GFSTools] Timer registered successfully")
    except Exception as e:
        print(f"[GFSTools] ERROR registering timer: {e}")
        traceback.print_exc()
    
    print("[GFSTools] === REGISTRATION COMPLETE ===\n")


def unregister():
    import bpy
    import traceback
    
    print("[GFSTools] === UNREGISTRATION START ===")
    
    CLASSES, PROP_GROUPS, LIST_ITEMS, MODULES = init_bpy()
    
    # Unregister classes (reverse order)
    print("[GFSTools] Unregistering classes...")
    for classtype in CLASSES[::-1]:
        try:
            bpy.utils.unregister_class(classtype)
            if 'Import' in classtype.__name__ or 'Export' in classtype.__name__:
                print(f"[GFSTools]   - {classtype.__name__} unregistered")
        except Exception as e:
            print(f"[GFSTools]   ERROR unregistering {classtype.__name__}: {e}")
            traceback.print_exc()

    # Unregister property groups
    print("[GFSTools] Unregistering property groups...")
    for obj, name, prop_type in PROP_GROUPS[::-1]:
        try:
            delattr(obj, name)
        except Exception as e:
            print(f"[GFSTools]   ERROR delattr {name}: {e}")
            traceback.print_exc()
        try:
            bpy.utils.unregister_class(prop_type)
        except Exception as e:
            print(f"[GFSTools]   ERROR unregistering prop {prop_type.__name__}: {e}")
            traceback.print_exc()
    
    # Remove menu items
    print("[GFSTools] Removing menu items...")
    for obj, elem in LIST_ITEMS:
        try:
            obj.remove(elem)
            print(f"[GFSTools]   - Removed menu from {obj.__name__}")
        except Exception as e:
            print(f"[GFSTools]   ERROR removing menu from {obj}: {e}")
            traceback.print_exc()
    
    # Unregister modules
    print("[GFSTools] Unregistering modules...")
    for mod in MODULES:
        try:
            mod.unregister()
        except Exception as e:
            print(f"[GFSTools]   ERROR unregistering module {mod}: {e}")
            traceback.print_exc()
    
    print("[GFSTools] === UNREGISTRATION COMPLETE ===\n")
