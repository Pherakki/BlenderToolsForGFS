import bpy
from .GFSProperties import makeCustomPropertiesPanel

def makeNodePropertiesPanel(identifier, space_type, region_type, context, props_getter, poll_func, parent_id=None):
    def make_idname():
        return f"OBJECT_PT_GFSTools{identifier}PropertiesPanel"
    
    class NodePropertiesPanel(bpy.types.Panel):
        bl_label       = "GFS Node"
        if parent_id is not None:
            bl_parent_id = parent_id
            
        bl_idname      = make_idname()
        bl_space_type  = space_type
        bl_region_type = region_type
        bl_context     = context
        
        
        @classmethod
        def poll(cls, context):
            return poll_func(cls, context)
    
        def draw(self, context):
            layout = self.layout
            
            props = props_getter(context)
            
            layout.prop(props, "unknown_float")
    
        @classmethod
        def register(cls):
            bpy.utils.register_class(cls.CustomPropertyPanel)
            
        @classmethod
        def unregister(cls):
            bpy.utils.unregister_class(cls.CustomPropertyPanel)

        CustomPropertyPanel = makeCustomPropertiesPanel(
            make_idname(),
            identifier,
            space_type, 
            region_type, 
            context,
            props_getter, 
            lambda cls, context: True
            )
        
    NodePropertiesPanel.__name__ = NodePropertiesPanel.bl_idname
    
    return NodePropertiesPanel
