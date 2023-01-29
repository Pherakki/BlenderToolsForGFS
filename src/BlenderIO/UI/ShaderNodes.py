import bpy


class OBJECT_PT_GFSToolsTextureRefPanel(bpy.types.Panel):
    bl_label       = "GFS Texture"
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
        
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "enable_anims")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x08")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "has_texture_filtering")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x0A")
        layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x0B")
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
