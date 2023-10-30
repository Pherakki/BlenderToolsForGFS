import bpy

from .Clipboard import GFSToolsClipboard
from .Physics import GFSToolsPhysicsProperties

class GFSToolsSceneProperties(bpy.types.PropertyGroup):
    physics_clipboard: bpy.props.PointerProperty(type=GFSToolsPhysicsProperties, name="Physics Clipboard")
    clipboard:         bpy.props.PointerProperty(type=GFSToolsClipboard)

