import bpy

class GFSToolsImageProperties(bpy.types.PropertyGroup):
    unknown_1: bpy.props.IntProperty(name="Unknown 1", default=1, min=0, max=255)
    unknown_2: bpy.props.IntProperty(name="Unknown 2", default=1, min=0, max=255)
    unknown_3: bpy.props.IntProperty(name="Unknown 3", default=0, min=0, max=255)
    unknown_4: bpy.props.IntProperty(name="Unknown 4", default=0, min=0, max=255)
