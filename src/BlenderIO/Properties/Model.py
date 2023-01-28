import bpy


class GFSToolsModelProperties(bpy.types.PropertyGroup):
    root_node_name:   bpy.props.StringProperty(name="Root Node Name", default="RootNode")
    has_external_emt: bpy.props.BoolProperty(name="External EMT", default=False)    
    physics_blob:     bpy.props.StringProperty(name="SECRET PHYSICS BLOB - DO NOT TOUCH", default='', options={'HIDDEN'})
