import bpy


def UIListBase(module_name, identifier, ui_list, collection_name, collection_idx_name, props_getter,
               add_callback=None, delete_callback=None, moveup_callback=None, movedown_callback=None,
               extra_collection_indices=None):
    if extra_collection_indices is None:
        extra_collection_indices = []

    class UIList:
        def draw(self, layout, context):
            self.draw_collection(layout, context)
            
        def draw_collection(self, layout, context):
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
                new_idx = len(collection) - 1
                setattr(props, collection_idx_name, new_idx)
                
                if add_callback is not None:
                    add_callback(context, event, collection_idx, new_idx)
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
                new_idx = collection_idx - 1
                setattr(props, collection_idx_name, new_idx)

                for idx_name in extra_collection_indices:
                    old_idx = getattr(props, idx_name)
                    if old_idx == collection_idx:
                        setattr(props, idx_name, -1)

                if delete_callback is not None:
                    delete_callback(context, event, collection_idx, new_idx)
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
                else:
                    new_idx = collection_idx

                for idx_name in extra_collection_indices:
                    idx = getattr(props, idx_name)
                    if collection_idx == idx:
                        setattr(props, idx_name, idx-1)
                    elif collection_idx == idx+ 1:
                        setattr(props, idx_name, idx+1)
                    
                if moveup_callback is not None:
                    moveup_callback(context, event, collection_idx, new_idx)
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
                else:
                    new_idx = collection_idx

                for idx_name in extra_collection_indices:
                    idx = getattr(props, idx_name)
                    if collection_idx == idx:
                        setattr(props, idx_name, idx + 1)
                    elif collection_idx == idx - 1:
                        setattr(props, idx_name, idx - 1)

                if movedown_callback is not None:
                    movedown_callback(context, event, collection_idx, new_idx)
                return {'FINISHED'}
    
    UIList.__name__                  = "UIList"
    UIList.AddOperator.__name__      = UIList.AddOperator.bl_idname
    UIList.DelOperator.__name__      = UIList.DelOperator.bl_idname
    UIList.MoveUpOperator.__name__   = UIList.MoveUpOperator.bl_idname
    UIList.MoveDownOperator.__name__ = UIList.MoveDownOperator.bl_idname
    
    return UIList
