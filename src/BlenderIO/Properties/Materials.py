import bpy


class GFSToolsTextureRefPanelProperties(bpy.types.PropertyGroup):
    # def update_unknown_0x04(self, context):
    #     print("UPDATING")
    
    unknown_0x04: bpy.props.FloatProperty()#update=update_unknown_0x04)
    unknown_0x08: bpy.props.FloatProperty()
    has_texture_filtering: bpy.props.BoolProperty(name="Filter Texture")
    unknown_0x0A: bpy.props.FloatProperty()
    unknown_0x0B: bpy.props.FloatProperty()
    unknown_0x0C: bpy.props.FloatProperty()
    unknown_0x10: bpy.props.FloatProperty()
    unknown_0x14: bpy.props.FloatProperty()
    unknown_0x18: bpy.props.FloatProperty()
    unknown_0x1C: bpy.props.FloatProperty()
    unknown_0x20: bpy.props.FloatProperty()
    unknown_0x24: bpy.props.FloatProperty()
    unknown_0x28: bpy.props.FloatProperty()
    unknown_0x2C: bpy.props.FloatProperty()
    unknown_0x30: bpy.props.FloatProperty()
    unknown_0x34: bpy.props.FloatProperty()
    unknown_0x38: bpy.props.FloatProperty()
    unknown_0x3C: bpy.props.FloatProperty()
    unknown_0x40: bpy.props.FloatProperty()
    unknown_0x44: bpy.props.FloatProperty()
    unknown_0x48: bpy.props.FloatProperty()

