import bpy
from .HelpWindows import defineHelpWindow


class OBJECT_PT_GFSToolsCameraAttributesPanel(bpy.types.Panel):
    bl_label       = "GFS Camera"
    bl_idname      = "OBJECT_PT_GFSToolsCameraAttributesPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(self, context):
        return context.camera is not None

    def draw(self, context):
        light = context.camera
        layout = self.layout
        
        layout.operator(self.CameraHelpWindow.bl_idname)
        
        ctr = layout.column()
        
        ctr.prop(light.GFSTOOLS_CameraProperties, "aspect_ratio")
        ctr.prop(light.GFSTOOLS_CameraProperties, "unknown_0x50")

    CameraHelpWindow = defineHelpWindow("Camera",
        "- 'Lens Unit' must be set to 'Field of View'.\n"\
        "- 'Aspect Ratio' sets the camera aspect ratio. This is not reflected inside Blender.\n"\
        "- 'unknown_0x50' is unknown."\
    )
