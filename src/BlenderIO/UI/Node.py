import bpy
from .HelpWindows import defineHelpWindow
from .GFSProperties import makeCustomPropertiesPanel


def makeNodePropertiesPanel(identifier, space_type, region_type, context, props_getter, poll_func, parent_id=None, predraw=None, extra_register=None):
    def make_idname():
        return f"OBJECT_PT_GFSTools{identifier}PropertiesPanel"
    
    class NodePropertiesPanel(bpy.types.Panel):
        bl_label       = "GFS Node"
        if parent_id is not None:
            bl_parent_id = parent_id
            bl_options   = {'DEFAULT_CLOSED'}

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
            
            layout.operator(self.NodeHelpWindow.bl_idname)
            
            if predraw is not None:
                predraw(context, layout)
            layout.prop(props, "unknown_float")
    
        @classmethod
        def register(cls):
            bpy.utils.register_class(cls.CustomPropertyPanel)
            bpy.utils.register_class(cls.NodeHelpWindow)
            if extra_register is not None:
                for elem in extra_register:
                    bpy.utils.register_class(elem)
            
        @classmethod
        def unregister(cls):
            bpy.utils.unregister_class(cls.CustomPropertyPanel)
            bpy.utils.unregister_class(cls.NodeHelpWindow)
            if extra_register is not None:
                for elem in extra_register:
                    bpy.utils.unregister_class(elem)


        NodeHelpWindow = defineHelpWindow(identifier,
            "- The purpose of 'Unknown Float' is unknown.\n"\
            "- GFS Properties of specific data types can be added, removed, and re-ordered with the Properties listbox. Properties that may be recognised and what they may do have not yet been enumerated."
        )

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
