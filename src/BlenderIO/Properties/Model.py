import bpy
from .Nodes import GFSToolsNodeProperties

class GFSToolsModelNodeProperties(GFSToolsNodeProperties):
    pass


class GFSToolsModelProperties(bpy.types.PropertyGroup):
    export_bounding_box: bpy.props.BoolProperty(name="Export Bounding Box", default=True)
    export_bounding_sphere: bpy.props.BoolProperty(name="Export Bounding Sphere", default=True)
    flag_3: bpy.props.BoolProperty(name="Unknown Flag 3", default=False)
    
    root_node_name:   bpy.props.StringProperty(name="Root Node Name", default="RootNode")
    has_external_emt: bpy.props.BoolProperty(name="External EMT", default=False)    
    physics_blob:     bpy.props.StringProperty(name="SECRET PHYSICS BLOB - DO NOT TOUCH", default='', options={'HIDDEN'})
