import bpy


class GFSToolsCameraProperties(bpy.types.PropertyGroup):
    aspect_ratio : bpy.props.FloatProperty(name="Aspect Ratio", default=16/9)
    unknown_0x50 : bpy.props.FloatProperty(name="Unknown 0x50", default=0.)
