import bpy


class OBJECT_UL_GFSToolsGenericPropertyUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        split = layout.split(factor=0.1)
        split.separator()
        split.prop(item, "dname")
        split.prop(item, "dtype")
        if item.dtype == "UINT32":
            split.prop(item, "uint32_data")
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


class OBJECT_PT_GFSToolsGenericPropertyPanel(bpy.types.Panel):
    bl_label = "Properties"
    
    @property
    def GFSTOOLS_addoperator(self):
        raise NotImplementedError()
        
    @property
    def GFSTOOLS_deloperator(self):
        raise NotImplementedError()
        
    @property
    def GFSTOOLS_moveupoperator(self):
        raise NotImplementedError()
        
    @property
    def GFSTOOLS_movedownoperator(self):
        raise NotImplementedError()
    
    def GFSTOOLS_get_obj(self, context):
        raise NotImplementedError()

    def draw(self, context):
        layout = self.layout

        obj = self.GFSTOOLS_get_obj(context)
        row = layout.row()
        row.template_list("OBJECT_UL_GFSToolsGenericPropertyUIList", "", obj, "properties", obj, "active_property_idx")

        col = row.column(align=True)
        col.operator(self.GFSTOOLS_addoperator, icon='ADD',    text="")
        col.operator(self.GFSTOOLS_deloperator, icon='REMOVE', text="")
        col.separator()
        col.operator(self.GFSTOOLS_moveupoperator,   icon='TRIA_UP',   text="")
        col.operator(self.GFSTOOLS_movedownoperator, icon='TRIA_DOWN', text="")


class OBJECT_OT_GFSToolsGenericPropertyPanelAdd(bpy.types.Operator):
    bl_label       = "Add Item"
    bl_description = "Adds a new GFSProperty to the Property List."
    bl_options     = {'REGISTER'}   
      
    def GFSTOOLS_get_obj(self, context):
        raise NotImplementedError()
        
    def invoke(self, context, event):
        obj = self.GFSTOOLS_get_obj(context)
        obj.properties.add()
        obj.active_property_idx = len(obj.properties) - 1
        return {'FINISHED'}


class OBJECT_OT_GFSToolsGenericPropertyPanelDel(bpy.types.Operator):
    bl_label       = "Delete Item"
    bl_description = "Removes the selected GFSProperty from the Property List."
    bl_options     = {'REGISTER'}   
      
    def GFSTOOLS_get_obj(self, context):
        raise NotImplementedError()
        
    def invoke(self, context, event):
        obj = self.GFSTOOLS_get_obj(context)
        obj.properties.remove(obj.active_property_idx)
        obj.active_property_idx -= 1
        return {'FINISHED'}


class OBJECT_OT_GFSToolsGenericPropertyPanelMoveUp(bpy.types.Operator):
    bl_label       = "Move Item Up"
    bl_description = "Moves the selected GFSProperty up in the Property List."
    bl_options     = {'REGISTER'}   
      
    def GFSTOOLS_get_obj(self, context):
        raise NotImplementedError()
        
    def invoke(self, context, event):
        obj = self.GFSTOOLS_get_obj(context)
        if obj.active_property_idx > 0:
            new_idx = obj.active_property_idx - 1
            obj.properties.move(obj.active_property_idx, new_idx)
            obj.active_property_idx = new_idx
        return {'FINISHED'}


class OBJECT_OT_GFSToolsGenericPropertyPanelMoveDown(bpy.types.Operator):
    bl_label       = "Move Item Down"
    bl_description = "Moves the selected GFSProperty down in the Property List."
    bl_options     = {'REGISTER'}   
      
    def GFSTOOLS_get_obj(self, context):
        raise NotImplementedError()
        
    def invoke(self, context, event):
        obj = self.GFSTOOLS_get_obj(context)
        if obj.active_property_idx < (len(obj.properties) - 1):
            new_idx = obj.active_property_idx + 1
            obj.properties.move(obj.active_property_idx, new_idx)
            obj.active_property_idx = new_idx
        return {'FINISHED'}
