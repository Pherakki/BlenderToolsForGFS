import bpy


class OBJECT_UL_GFSToolsPhysBoneUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        split = layout.split(factor=0.1)
        split.separator()
        split.prop(item, "dtype")
        split.prop(item, "unknown_0x00")
        split.prop(item, "unknown_0x04")
        split.prop(item, "unknown_0x08")
        split.prop(item, "unknown_0x0C")
        if item.dtype == "Named":
            split.prop(item, "name")
        elif item.dtype == "Unnamed":
            split.prop(item, "nameless_data")

class OBJECT_UL_GFSToolsPhysCldrUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        split = layout.split(factor=0.1)
        split.separator()
        split.prop(item, "name")
        split.prop(item, "dtype")
        split.prop(item, "radius")
        if item.dtype == "Capsule":
            split.prop(item, "height")
        split.prop(item, "matrix")

class OBJECT_UL_GFSToolsPhysLinkUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        split = layout.split(factor=0.1)
        split.separator()
        split.prop(item, "mass")
        split.prop(item, "unknown_0x04")
        split.prop(item, "radius")
        
        split.prop_search(item, "parent", data, "bones")
        split.prop_search(item, "child",  data, "bones")


def makeCollectionPanel(label, parent_id, identifier, space_type, region_type, context, list_id, props_getter, poll_func, props_id, props_idx_id):
    class PropertyPanel(bpy.types.Panel):
        bl_label       = label
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
            row.template_list(list_id, "", obj, props_id, obj, props_idx_id)

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
            bl_idname = f"GFSTOOLS.OBJECT_OT_{identifier}PanelAdd".lower()
            
            bl_label       = "Add Item"
            bl_description = "Adds a new GFSProperty to the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                obj       = props_getter(context)
                props     = getattr(obj, props_id)
                props_idx = getattr(obj, props_idx_id)
                
                props.add()
                setattr(obj, props_idx_id, len(props) - 1)
                return {'FINISHED'}
        
        
        class DelOperator(bpy.types.Operator):
            bl_idname = f"GFSTOOLS.OBJECT_OT_{identifier}PanelDel".lower()
            
            bl_label       = "Delete Item"
            bl_description = "Removes the selected GFSProperty from the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                obj       = props_getter(context)
                props     = getattr(obj, props_id)
                props_idx = getattr(obj, props_idx_id)
                
                props.remove(props_idx)
                if props_idx > 0:
                    setattr(obj, props_idx_id, props_idx-1)
                return {'FINISHED'}
        
        
        class MoveUpOperator(bpy.types.Operator):
            bl_idname = f"GFSTOOLS.OBJECT_OT_{identifier}PanelMoveUp".lower()
            
            bl_label       = "Move Item Up"
            bl_description = "Moves the selected GFSProperty up in the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                obj       = props_getter(context)
                props     = getattr(obj, props_id)
                props_idx = getattr(obj, props_idx_id)
                
                if props_idx > 0:
                    new_idx = props_idx - 1
                    props.move(props_idx, new_idx)
                    setattr(obj, props_idx_id, new_idx)
                
                return {'FINISHED'}
        
        
        class MoveDownOperator(bpy.types.Operator):
            bl_idname = f"GFSTOOLS.OBJECT_OT_{identifier}PanelMoveDown".lower()
            
            bl_label       = "Move Item Down"
            bl_description = "Moves the selected GFSProperty down in the Property List."
            bl_options     = {'REGISTER'}   
              
            def invoke(self, context, event):
                obj       = props_getter(context)
                props     = getattr(obj, props_id)
                props_idx = getattr(obj, props_idx_id)
                
                if props_idx < (len(props) - 1):
                    new_idx = props_idx + 1
                    props.move(props_idx, new_idx)
                    setattr(obj, props_idx_id, new_idx)
                
                return {'FINISHED'}
    
    PropertyPanel.__name__                  = f"OBJECT_PT_GFSTools{identifier}Panel"
    PropertyPanel.AddOperator.__name__      = PropertyPanel.AddOperator.bl_idname
    PropertyPanel.DelOperator.__name__      = PropertyPanel.DelOperator.bl_idname
    PropertyPanel.MoveUpOperator.__name__   = PropertyPanel.MoveUpOperator.bl_idname
    PropertyPanel.MoveDownOperator.__name__ = PropertyPanel.MoveDownOperator.bl_idname
    return PropertyPanel



class OBJECT_PT_GFSToolsPhysicsDataPanel(bpy.types.Panel):
    bl_label       = "GFS Physics"
    bl_idname      = "OBJECT_PT_GFSToolsPhysicsDataPanel"
    bl_parent_id   = "OBJECT_PT_GFSToolsModelDataPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}
    
    bone_list = makeCollectionPanel("Bones", 
                                    "OBJECT_PT_GFSToolsPhysicsDataPanel",
                                    "PhysBones",
                                    "PROPERTIES",
                                    "WINDOW",
                                    "data",
                                    "OBJECT_UL_GFSToolsPhysBoneUIList",
                                    lambda ctx: ctx.armature.GFSTOOLS_ModelProperties.physics,
                                    lambda cls, ctx: ctx.armature is not None,
                                    "bones",
                                    "active_bone_idx")
    
    cldr_list = makeCollectionPanel("Colliders", 
                                    "OBJECT_PT_GFSToolsPhysicsDataPanel",
                                    "PhysCldr",
                                    "PROPERTIES",
                                    "WINDOW",
                                    "data",
                                    "OBJECT_UL_GFSToolsPhysCldrUIList",
                                    lambda ctx: ctx.armature.GFSTOOLS_ModelProperties.physics,
                                    lambda cls, ctx: ctx.armature is not None,
                                    "colliders",
                                    "active_cldr_idx")
    
    link_list = makeCollectionPanel("Links", 
                                    "OBJECT_PT_GFSToolsPhysicsDataPanel",
                                    "PhysLink",
                                    "PROPERTIES",
                                    "WINDOW",
                                    "data",
                                    "OBJECT_UL_GFSToolsPhysLinkUIList",
                                    lambda ctx: ctx.armature.GFSTOOLS_ModelProperties.physics,
                                    lambda cls, ctx: ctx.armature is not None,
                                    "links",
                                    "active_link_idx")
    
    @classmethod
    def poll(cls, context):
        return context.armature is not None

    def draw(self, context):
        armature = context.armature
        layout = self.layout
        
        props = armature.GFSTOOLS_ModelProperties.physics
        
        ctr = layout.column()
        
        ctr.prop(props, "unknown_0x00")
        ctr.prop(props, "unknown_0x04")
        ctr.prop(props, "unknown_0x08")
        ctr.prop(props, "unknown_0x0C")
        ctr.prop(props, "unknown_0x10")

    @classmethod
    def register(cls):
        bpy.utils.register_class(OBJECT_UL_GFSToolsPhysBoneUIList)
        bpy.utils.register_class(OBJECT_UL_GFSToolsPhysCldrUIList)
        bpy.utils.register_class(OBJECT_UL_GFSToolsPhysLinkUIList)
        bpy.utils.register_class(cls.bone_list)
        bpy.utils.register_class(cls.cldr_list)
        bpy.utils.register_class(cls.link_list)
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsPhysBoneUIList)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsPhysCldrUIList)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsPhysLinkUIList)
        bpy.utils.unregister_class(cls.bone_list)
        bpy.utils.unregister_class(cls.cldr_list)
        bpy.utils.unregister_class(cls.link_list)