import bpy
from .GFSProperties import GFSToolsGenericProperty


class GFSToolsNodeProperties(bpy.types.PropertyGroup):
    unknown_float:       bpy.props.FloatProperty(name="Unknown Float", default=1.0)
    properties:          bpy.props.CollectionProperty(name="Properties", type=GFSToolsGenericProperty)
    active_property_idx: bpy.props.IntProperty(options={'HIDDEN'})
