import bpy


class OBJECT_UL_GFSToolsGenericPropertyUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        split = layout.split(factor=0.1)
        split.separator()
        split.prop(item, "dname")
        split.prop(item, "dtype")
        if item.dtype == "INT32":
            split.prop(item, "int32_data")
        elif item.dtype == "FLOAT32":
            split.prop(item, "float32_data")
        elif item.dtype == "UINT8":
            split.prop(item, "uint8_data")
        elif item.dtype == "STRING":
            split.prop(item, "string_data")
        elif item.dtype == "UINT8VEC3":
            split.prop(item, "uint8vec3_data")
        elif item.dtype == "UINT8VEC4":
            split.prop(item, "uint8vec4_data")
        elif item.dtype == "FLOAT32VEC3":
            split.prop(item, "float32vec3_data")
        elif item.dtype == "FLOAT32VEC4":
            split.prop(item, "float32vec4_data")
        elif item.dtype == "BYTES":
            split.prop(item, "bytes_data")


def makeCustomPropertiesPanel(parent_id, identifier, space_type, region_type, context, props_getter, poll_func):
    class PropertyPanel(bpy.types.Panel):
        bl_label       = "Properties"
        bl_parent_id   = parent_id
        bl_space_type  = space_type
        bl_region_type = region_type
        bl_context     = context

        @classmethod
        def poll(cls, context):
            return poll_func(cls, context)
    
        def draw(self, context):
            layout = self.layout
    
            obj = props_getter(context)
            row = layout.row()
            row.template_list("OBJECT_UL_GFSToolsGenericPropertyUIList", "", obj, "properties", obj, "active_property_idx")

            col = row.column(align=True)
            col.operator(type(self).AddOperator.bl_idname, icon='ADD',    text="")
            col.operator(type(self).DelOperator.bl_idname, icon='REMOVE', text="")
            col.separator()
            col.operator(type(self).MoveUpOperator.bl_idname,   icon='TRIA_UP',   text="")
            col.operator(type(self).MoveDownOperator.bl_idname, icon='TRIA_DOWN', text="")
    
        @classmethod
        def register(cls):
            bpy.utils.register_class(cls.AddOperator)
            bpy.utils.register_class(cls.DelOperator)
            bpy.utils.register_class(cls.MoveUpOperator)
            bpy.utils.register_class(cls.MoveDownOperator)
    
        @classmethod
        def unregister(cls):
            bpy.utils.unregister_class(cls.AddOperator)
            bpy.utils.unregister_class(cls.DelOperator)
            bpy.utils.unregister_class(cls.MoveUpOperator)
            bpy.utils.unregister_class(cls.MoveDownOperator)

        class AddOperator(bpy.types.Operator):
            bl_idname = f"GFSTOOLS.OBJECT_OT_{identifier}PropertyPanelAdd".lower()
            
            bl_label       = "Add Item"
            bl_description = "Adds a new GFSProperty to the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                obj = props_getter(context)
                obj.properties.add()
                obj.active_property_idx = len(obj.properties) - 1
                return {'FINISHED'}
        
        
        class DelOperator(bpy.types.Operator):
            bl_idname = f"GFSTOOLS.OBJECT_OT_{identifier}PropertyPanelDel".lower()
            
            bl_label       = "Delete Item"
            bl_description = "Removes the selected GFSProperty from the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                obj = props_getter(context)
                obj.properties.remove(obj.active_property_idx)
                obj.active_property_idx -= 1
                return {'FINISHED'}
        
        
        class MoveUpOperator(bpy.types.Operator):
            bl_idname = f"GFSTOOLS.OBJECT_OT_{identifier}PropertyPanelMoveUp".lower()
            
            bl_label       = "Move Item Up"
            bl_description = "Moves the selected GFSProperty up in the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                obj = props_getter(context)
                if obj.active_property_idx > 0:
                    new_idx = obj.active_property_idx - 1
                    obj.properties.move(obj.active_property_idx, new_idx)
                    obj.active_property_idx = new_idx
                return {'FINISHED'}
        
        
        class MoveDownOperator(bpy.types.Operator):
            bl_idname = f"GFSTOOLS.OBJECT_OT_{identifier}PropertyPanelMoveDown".lower()
            
            bl_label       = "Move Item Down"
            bl_description = "Moves the selected GFSProperty down in the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                obj = props_getter(context)
                if obj.active_property_idx < (len(obj.properties) - 1):
                    new_idx = obj.active_property_idx + 1
                    obj.properties.move(obj.active_property_idx, new_idx)
                    obj.active_property_idx = new_idx
                return {'FINISHED'}
    
    PropertyPanel.__name__                  = f"OBJECT_PT_GFSTools{identifier}GenericPropertyPanel"
    PropertyPanel.AddOperator.__name__      = PropertyPanel.AddOperator.bl_idname
    PropertyPanel.DelOperator.__name__      = PropertyPanel.DelOperator.bl_idname
    PropertyPanel.MoveUpOperator.__name__   = PropertyPanel.MoveUpOperator.bl_idname
    PropertyPanel.MoveDownOperator.__name__ = PropertyPanel.MoveDownOperator.bl_idname
    return PropertyPanel