import bpy


def UIListBase(module_name, identifier, ui_list, collection_name, collection_idx_name, props_getter):
    class PropertyPanel(bpy.types.Panel):
        def draw(self, context):
            self.draw_collection(context)
            
        def draw_collection(self, context):
            layout = self.layout
    
            props = props_getter(context)
            row = layout.row()
            row.template_list(ui_list.__name__, "", props, collection_name, props, collection_idx_name)

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
            bl_idname = f"{module_name}.OBJECT_OT_{identifier}PanelAdd".lower()
            
            bl_label       = "Add Item"
            bl_description = "Adds a new item to the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                props          = props_getter(context)
                collection     = getattr(props, collection_name)
                collection_idx = getattr(props, collection_idx_name)
                
                collection.add()
                setattr(props, collection_idx_name, len(collection) - 1)
                return {'FINISHED'}
        
        
        class DelOperator(bpy.types.Operator):
            bl_idname = f"{module_name}.OBJECT_OT_{identifier}PanelDel".lower()
            
            bl_label       = "Delete Item"
            bl_description = "Removes the selected item from the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                props          = props_getter(context)
                collection     = getattr(props, collection_name)
                collection_idx = getattr(props, collection_idx_name)
                
                collection.remove(collection_idx)
                setattr(props, collection_idx_name, collection_idx - 1)
                
                return {'FINISHED'}
        
        
        class MoveUpOperator(bpy.types.Operator):
            bl_idname = f"{module_name}.OBJECT_OT_{identifier}PanelMoveUp".lower()
            
            bl_label       = "Move Item Up"
            bl_description = "Moves the selected item up in the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                props          = props_getter(context)
                collection     = getattr(props, collection_name)
                collection_idx = getattr(props, collection_idx_name)
                
                if collection_idx > 0:
                    new_idx = collection_idx - 1
                    collection.move(collection_idx, new_idx)
                    setattr(props, collection_idx_name, new_idx)
                return {'FINISHED'}
        
        
        class MoveDownOperator(bpy.types.Operator):
            bl_idname = f"{module_name}.OBJECT_OT_{identifier}PanelMoveDown".lower()
            
            bl_label       = "Move Item Down"
            bl_description = "Moves the selected item down in the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                props          = props_getter(context)
                collection     = getattr(props, collection_name)
                collection_idx = getattr(props, collection_idx_name)
                
                if collection_idx < (len(collection) - 1):
                    new_idx = collection_idx + 1
                    collection.move(collection_idx, new_idx)
                    setattr(props, collection_idx_name, new_idx)
                return {'FINISHED'}
    
    PropertyPanel.__name__                  = f"{module_name}.OBJECT_PT_{identifier}Panel"
    PropertyPanel.AddOperator.__name__      = PropertyPanel.AddOperator.bl_idname
    PropertyPanel.DelOperator.__name__      = PropertyPanel.DelOperator.bl_idname
    PropertyPanel.MoveUpOperator.__name__   = PropertyPanel.MoveUpOperator.bl_idname
    PropertyPanel.MoveDownOperator.__name__ = PropertyPanel.MoveDownOperator.bl_idname
    
    return PropertyPanel
