import bpy


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
        
        ctr = layout.column()
        
        ctr.prop(light.GFSTOOLS_CameraProperties, "aspect_ratio")
        ctr.prop(light.GFSTOOLS_CameraProperties, "unknown_0x50")
