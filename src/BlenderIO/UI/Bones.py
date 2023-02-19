import bpy
from .Node import makeNodePropertiesPanel
from .HelpWindows import defineHelpWindow


class OBJECT_PT_GFSToolsBonePropertiesPanel(bpy.types.Panel):
    bl_label       = "GFS Bone"
    bl_idname      = "OBJECT_PT_GFSToolsBonePropertiesPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "bone"
    bl_options     = {'DEFAULT_CLOSED'}
    
    
    @classmethod
    def poll(cls, context):
        return type(context.active_bone) is bpy.types.Bone

    def draw(self, context):
        layout = self.layout
        
        ctr = layout.column()
        
        ctr.operator(self.BoneHelpWindow.bl_idname)
        
    BoneHelpWindow = defineHelpWindow("Bone", "Test String")    
    
    NodePropertiesPanel = makeNodePropertiesPanel(
        "BoneNode", 
        "PROPERTIES", 
        "WINDOW",
        "bone", 
        lambda context: context.active_bone.GFSTOOLS_NodeProperties,
        lambda cls, context: type(context.active_bone) is bpy.types.Bone,
        parent_id="OBJECT_PT_GFSToolsBonePropertiesPanel"
    )
    
    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.NodePropertiesPanel)
        bpy.utils.register_class(cls.BoneHelpWindow)
        
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.NodePropertiesPanel)
        bpy.utils.unregister_class(cls.BoneHelpWindow)
    