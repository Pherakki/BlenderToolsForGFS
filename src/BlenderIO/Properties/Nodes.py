import bpy
from .GFSProperties import GFSToolsGenericProperty


class BlobProperty(bpy.types.PropertyGroup):
    blob: bpy.props.StringProperty(name="blob", default="")


def make_node_props_class(name):
    class GFSToolsNodeProperties(bpy.types.PropertyGroup):
        override_name:       bpy.props.StringProperty(name="Override Name", default="", maxlen=2**16 - 1,
                                                      description="The name the node will be written out under. "\
                                                                  "Use this to give nodes UTF-8 names that take 64 bytes."\
                                                                  "If empty, the object's identifier will be used."\
                                                                  "Do NOT use this unless you have a really good reason.")
        unknown_float:       bpy.props.FloatProperty(name="Unknown Float", default=1.0)
        properties:          bpy.props.CollectionProperty(name="Properties", type=GFSToolsGenericProperty)
        active_property_idx: bpy.props.IntProperty(options={'HIDDEN'})
    
        epls:                bpy.props.CollectionProperty(name="EPLs",
                                                          type=BlobProperty,
                                                          options={'HIDDEN'})
    GFSToolsNodeProperties.__name__ = name
    
    return GFSToolsNodeProperties
