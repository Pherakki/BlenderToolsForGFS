import bpy

from .HelpWindows import defineHelpWindow


class OBJECT_PT_GFSToolsTextureRefPanel(bpy.types.Panel):
    bl_label       = "GFS Texture Sampler"
    bl_idname      = "OBJECT_PT_GFSToolsTextureRefPanel"
    bl_space_type  = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category    = "GFS Texture"
    
    @classmethod
    def poll(self, context):
        if context.active_node is None:
            return False
        is_required_area      = context.area.ui_type     == "ShaderNodeTree"
        is_required_node_type = context.active_node.type == "TEX_IMAGE"
        return is_required_area and is_required_node_type

    def draw(self, context):
        node = context.active_node
        layout = self.layout
        
        layout.operator(self.TextureSamplerHelpWindow.bl_idname)
        
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "enable_anims")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x08")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "has_texture_filtering")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "wrap_mode_u")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "wrap_mode_v")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x0C")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x10")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x14")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x18")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x1C")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x20")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x24")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x28")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x2C")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x30")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x34")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x38")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x3C")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x40")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x44")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x48")
    
        TextureSamplerHelpWindow = defineHelpWindow("TextureSampler", 
            "- Animatable will allow the UV coordinates to be animated."\
            "- The purpose of unknown_0x08 is unknown."\
            "- Texture Filtering has no effect."\
            "- The purpose of the remaining attributes is unknown."
        )
    
        @classmethod
        def register(cls):
            bpy.utils.register_class(cls.TextureSamplerHelpWindow)
        
        @classmethod
        def unregister(cls):
            bpy.utils.unregister_class(cls.TextureSamplerHelpWindow)
        

class OBJECT_PT_GFSToolsImagePanel(bpy.types.Panel):
    bl_label       = "GFS Texture"
    bl_idname      = "OBJECT_PT_GFSToolsImagePanel"
    bl_parent_id   = "OBJECT_PT_GFSToolsTextureRefPanel"
    bl_space_type  = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category    = "GFS Texture"
    
    @classmethod
    def poll(self, context):
        if context.active_node is None:
            return False
        
        is_required_area = context.area.ui_type     == "ShaderNodeTree"
        is_required_node_type = context.active_node.type == "TEX_IMAGE"
        has_img = context.active_node.image is not None if is_required_node_type else False
             
        return is_required_area and is_required_node_type and has_img

    def draw(self, context):
        img = context.active_node.image
        layout = self.layout
        
        layout.operator(self.TextureHelpWindow.bl_idname)
        
        layout.prop(img.GFSTOOLS_ImageProperties, "unknown_1")
        layout.prop(img.GFSTOOLS_ImageProperties, "unknown_2")
        layout.prop(img.GFSTOOLS_ImageProperties, "unknown_3")
        layout.prop(img.GFSTOOLS_ImageProperties, "unknown_4")

    TextureHelpWindow = defineHelpWindow("Texture", 
        "- The purpose of Unknown 1 is unknown."\
        "- The purpose of Unknown 2 is unknown."\
        "- The purpose of Unknown 3 is unknown."\
        "- The purpose of Unknown 4 is unknown."\
    )

    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.TextureHelpWindow)
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.TextureHelpWindow)