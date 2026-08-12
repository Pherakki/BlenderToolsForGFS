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
    
    
    LIST_ITEMS = (
        (bpy.types.TOPBAR_MT_file_import, menu_func_import),
        (bpy.types.TOPBAR_MT_file_export, menu_func_export)
    )
    
    MODULES = (
        ErrorLogger,
    )
    
    return CLASSES, PROP_GROUPS, LIST_ITEMS, MODULES



def register():
    import bpy
    import traceback
    from .src.BlenderIO.Preferences import get_preferences
    
    def create_welcome_message():
        prefs = get_preferences()
        if not prefs.initialized:
            prefs.initialized = True
            try:
                bpy.ops.gfstools.registerwindow('INVOKE_DEFAULT')
            except Exception:
                # Fallback: ignore if operator isn't available yet
                traceback.print_exc()
    
    CLASSES, PROP_GROUPS, LIST_ITEMS, MODULES = init_bpy()
    
   # Note for later: multi-language support can be implemented by checking
   #     - bpy.context.preferences.view.language
   #     - bpy.context.preferences.view.use_translate_interface
   #     - bpy.context.preferences.view.use_translate_new_dataname
   #     - bpy.context.preferences.view.use_translate_tooltips
    for classtype in CLASSES:
        try:
            bpy.utils.register_class(classtype)
        except Exception:
            # Continue if already registered or if there's a specific ordering issue
            traceback.print_exc()
    
    for obj, name, prop_type in PROP_GROUPS:
        try:
            bpy.utils.register_class(prop_type)
        except Exception:
            # Already registered or registration error; continue
            traceback.print_exc()
        try:
            setattr(obj, name, bpy.props.PointerProperty(type=prop_type))
        except Exception:
            traceback.print_exc()
        
    for obj, elem in LIST_ITEMS:
        try:
            obj.append(elem)
        except Exception:
            traceback.print_exc()
        
    for mod in MODULES:
        try:
            mod.register()
        except Exception:
            traceback.print_exc()
    
    # Fire off the welcome message
    try:
        bpy.app.timers.register(create_welcome_message, first_interval=.01)
    except Exception:
        traceback.print_exc()


def unregister():
    import bpy
    import traceback
    
    CLASSES, PROP_GROUPS, LIST_ITEMS, MODULES = init_bpy()
    
    for classtype in CLASSES[::-1]:
        try:
            bpy.utils.unregister_class(classtype)
        except Exception:
            traceback.print_exc()

    for obj, name, prop_type in PROP_GROUPS[::-1]:
        try:
            delattr(obj, name)
        except Exception:
            traceback.print_exc()
        try:
            bpy.utils.unregister_class(prop_type)
        except Exception:
            traceback.print_exc()
        
    for obj, elem in LIST_ITEMS:
        try:
            obj.remove(elem)
        except Exception:
            traceback.print_exc()
        
    for mod in MODULES:
        try:
            mod.unregister()
        except Exception:
            traceback.print_exc()
        