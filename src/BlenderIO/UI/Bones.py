import bpy
from .GFSProperties import OBJECT_PT_GFSToolsGenericPropertyPanel
from .GFSProperties import OBJECT_OT_GFSToolsGenericPropertyPanelAdd
from .GFSProperties import OBJECT_OT_GFSToolsGenericPropertyPanelDel
from .GFSProperties import OBJECT_OT_GFSToolsGenericPropertyPanelMoveUp
from .GFSProperties import OBJECT_OT_GFSToolsGenericPropertyPanelMoveDown


class OBJECT_PT_GFSToolsBonePropertiesPanel(bpy.types.Panel):
    bl_label       = "GFS Node"
    bl_idname      = "OBJECT_PT_GFSToolsBonePropertiesPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "bone"


    @classmethod
    def poll(self, context):
        return type(context.active_bone) is bpy.types.Bone

    def draw(self, context):
        layout = self.layout
        
        obj = context.active_bone
        
        layout.prop(obj.GFSTOOLS_BoneProperties, "unknown_float")


class OBJECT_PT_GFSToolsBoneGenericPropertyPanel(OBJECT_PT_GFSToolsGenericPropertyPanel):
    bl_parent_id   = "OBJECT_PT_GFSToolsBonePropertiesPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "bone"
    
    @property
    def GFSTOOLS_addoperator(self):
        return OBJECT_OT_GFSToolsBoneGenericPropertyPanelAdd.bl_idname
    
    @property
    def GFSTOOLS_deloperator(self):
        return OBJECT_OT_GFSToolsBoneGenericPropertyPanelDel.bl_idname
    
    @property
    def GFSTOOLS_moveupoperator(self):
        return OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveUp.bl_idname
    
    @property
    def GFSTOOLS_movedownoperator(self):
        return OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveDown.bl_idname
    
    def GFSTOOLS_get_obj(self, context):
        return context.active_bone.GFSTOOLS_BoneProperties
    

class OBJECT_OT_GFSToolsBoneGenericPropertyPanelAdd(OBJECT_OT_GFSToolsGenericPropertyPanelAdd):
    bl_idname = "GFSTOOLS.OBJECT_OT_GFSToolsBoneGenericPropertyPanelAdd".lower()
    
    def GFSTOOLS_get_obj(self, context):
        return context.active_bone.GFSTOOLS_BoneProperties


class OBJECT_OT_GFSToolsBoneGenericPropertyPanelDel(OBJECT_OT_GFSToolsGenericPropertyPanelDel):
    bl_idname = "GFSTOOLS.OBJECT_OT_GFSToolsBoneGenericPropertyPanelDel".lower()
    
    def GFSTOOLS_get_obj(self, context):
        return context.active_bone.GFSTOOLS_BoneProperties


class OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveUp(OBJECT_OT_GFSToolsGenericPropertyPanelMoveUp):
    bl_idname = "GFSTOOLS.OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveUp".lower()
    
    def GFSTOOLS_get_obj(self, context):
        return context.active_bone.GFSTOOLS_BoneProperties


class OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveDown(OBJECT_OT_GFSToolsGenericPropertyPanelMoveDown):
    bl_idname = "GFSTOOLS.OBJECT_OT_GFSToolsBoneGenericPropertyPanelMoveDown".lower()
    
    def GFSTOOLS_get_obj(self, context):
        return context.active_bone.GFSTOOLS_BoneProperties
