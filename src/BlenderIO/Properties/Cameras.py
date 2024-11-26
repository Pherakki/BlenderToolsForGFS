import bpy


class GFSToolsCameraProperties(bpy.types.PropertyGroup):
    aspect_ratio : bpy.props.FloatProperty(name="Aspect Ratio", default=16/9)
    unknown_0x50 : bpy.props.FloatProperty(name="Unknown 0x50", default=0.)
    unknown_0x54 : bpy.props.IntProperty(name="Unknown 0x54", default=0, min=0, max=255)
    unknown_0x55 : bpy.props.FloatProperty(name="Unknown 0x55", default=0.)
    unknown_0x59 : bpy.props.FloatProperty(name="Unknown 0x59", default=0.)
