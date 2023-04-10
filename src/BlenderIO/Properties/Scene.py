import bpy

from .Physics import GFSToolsPhysicsProperties

class GFSToolsSceneProperties(bpy.types.PropertyGroup):
    physics_clipboard: bpy.props.PointerProperty(type=GFSToolsPhysicsProperties, name="Physics Clipboard")
