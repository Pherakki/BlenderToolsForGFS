import bpy


class OBJECT_PT_GFSToolsAnimationPanel(bpy.types.Panel):
    bl_label       = "GFS Animation"
    bl_idname      = "OBJECT_PT_GFSToolsAnimationPanel"
    bl_space_type  = 'NLA_EDITOR'
    bl_region_type = 'UI'
    bl_category    = "Strip"
    
    @classmethod
    def poll(self, context):
        if context.active_nla_strip is None:
            return False
        elif context.active_nla_strip.action is None:
            return False
        return True

    def draw(self, context):
        # node = context.active_node
        layout = self.layout
        
        layout.label("I AM A TEST")
        
        active_action = context.active_nla_strip.action
        props = active_action.GFSTOOLS_AnimationProperties
        
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x04")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x08")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "has_texture_filtering")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x0A")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x0B")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x0C")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x10")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x14")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x18")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x1C")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x20")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x24")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x28")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x2C")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x30")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x34")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x38")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x3C")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x40")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x44")
        # layout.prop(node.GFSTOOLS_TextureRefPanelProperties, "unknown_0x48")
