import bpy

from ...Utils.Object import get_model_props
from ...Utils.PhysicsGen import make_collider, repair_col_material, get_col_material


class BoneEditBox(bpy.types.Operator):
    bl_idname = "GFSTOOLS.BoneEditBox".lower()
    bl_label = ""
    
    idx: bpy.props.IntProperty()
    
    def draw(self, context):
        layout = self.layout
        mdl_props = get_model_props(context)
        props = mdl_props.physics.bones[self.idx]
        
        layout.prop(props, "unknown_0x00")
        layout.prop(props, "unknown_0x04")
        layout.prop(props, "unknown_0x08")
        layout.prop(props, "unknown_0x0C")
        if not props.has_name:
            layout.prop(props, "nameless_data")
 
    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 600)


class OBJECT_UL_GFSToolsPhysBoneUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.7)
        r = split.row()
        r.prop(item, "has_name", text="")
        c = r.column()
        c.prop(item, "name")
        c.enabled = item.has_name
        
        c = split.column()
        op = c.operator(BoneEditBox.bl_idname, text="Edit")
        op.idx = index


class LinkEditBox(bpy.types.Operator):
    bl_idname = "GFSTOOLS.LinkEditBox".lower()
    bl_label = ""
    
    idx: bpy.props.IntProperty()
    
    def draw(self, context):
        layout = self.layout
        mdl_props = get_model_props(context)
        props = mdl_props.physics.links[self.idx]
        
        layout.prop(props, "mass")
        layout.prop(props, "unknown_0x04")
        layout.prop(props, "radius")
 
    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)


class OBJECT_UL_GFSToolsPhysLinkUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.7)
        s = split.split(factor=0.5)
        r = s.split(factor=0.5)
        r.label(text="Parent")
        r.prop(item, "parent", text="")
        s.prop(item, "child")
        
        c = split.column()
        op = c.operator(LinkEditBox.bl_idname, text="Edit")
        op.idx = index


class ResetColliderMaterial(bpy.types.Operator):
    bl_label = "Reset Material to Global"
    bl_idname = "GFSTOOLS.ResetColliderObjectMaterial".lower()
    bl_options = {'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        mesh = context.mesh
        obj.active_material = get_col_material()
        
        self.report({'INFO'}, f"Set '{obj.name}' material to the GFSTools Collider material")
        return {'FINISHED'}
        
class RepairColliderMaterial(bpy.types.Operator):
    bl_label = "Repair Global Material"
    bl_idname = "GFSTOOLS.RepairColliderMaterial".lower()
    bl_options = {'UNDO'}
    
    def execute(self, context):
        repair_col_material()
        
        self.report({'INFO'}, f"Repaired global collider material")
        return {'FINISHED'}


class OBJECT_PT_GFSToolsColliderPanel(bpy.types.Panel):
    bl_label       = "GFS Collider"
    bl_idname      = "OBJECT_PT_GFSToolsColliderPanel"
    bl_space_type  = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context     = "data"

    @classmethod
    def poll(cls, context):
        if context.mesh is not None:
            return context.mesh.GFSTOOLS_MeshProperties.is_collider()
        else:
            return False

    def draw(self, context):
        layout = self.layout
        props  = context.mesh.GFSTOOLS_ColliderProperties

        col = layout.column()
        row = col.row()
        row.prop(props, "detached")
        if context.active_object.parent is not None:
            row.enabled = context.active_object.parent_type != "BONE"
        col.prop(props, "dtype")
        col.prop(props, "radius")
        if props.dtype == "Capsule":
            col.prop(props, "height")
        
        r = col.row()
        r.operator(ResetColliderMaterial.bl_idname)
        r.operator(RepairColliderMaterial.bl_idname)
        
    @classmethod
    def register(cls):
        bpy.utils.register_class(ResetColliderMaterial)
        bpy.utils.register_class(RepairColliderMaterial)
        
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(ResetColliderMaterial)
        bpy.utils.unregister_class(RepairColliderMaterial)

def makeCollectionPanel(label, parent_id, identifier, space_type, region_type, context, list_id, props_getter, poll_func, props_id, props_idx_id, manage_link_idxs):
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
                
                # Shift indices of bone links
                if manage_link_idxs:
                    for link in obj.links:
                        for mem in ["parent", "child"]:
                            bone_idx = getattr(link, mem)
                            if bone_idx == props_idx:
                                setattr(link, mem, -1)
                            elif bone_idx > props_idx:
                                setattr(link, mem, bone_idx-1)
                    
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
                
                    # Shift indices of bone links
                    if manage_link_idxs:
                        for link in obj.links:
                            for mem in ["parent", "child"]:
                                bone_idx = getattr(link, mem)
                                if bone_idx == props_idx:
                                    setattr(link, mem, new_idx)
                                elif bone_idx == new_idx:
                                    setattr(link, mem, props_idx)
                        
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
                    
                    # Shift indices of bone links
                    if manage_link_idxs:
                        for link in obj.links:
                            for mem in ["parent", "child"]:
                                bone_idx = getattr(link, mem)
                                if bone_idx == props_idx:
                                    setattr(link, mem, new_idx)
                                elif bone_idx == new_idx:
                                    setattr(link, mem, props_idx)
                
                return {'FINISHED'}
    
    PropertyPanel.__name__                  = f"OBJECT_PT_GFSTools{identifier}Panel"
    PropertyPanel.AddOperator.__name__      = PropertyPanel.AddOperator.bl_idname
    PropertyPanel.DelOperator.__name__      = PropertyPanel.DelOperator.bl_idname
    PropertyPanel.MoveUpOperator.__name__   = PropertyPanel.MoveUpOperator.bl_idname
    PropertyPanel.MoveDownOperator.__name__ = PropertyPanel.MoveDownOperator.bl_idname
    return PropertyPanel


def clone_physics(from_phys, to_phys):
    to_phys.unknown_0x00 = from_phys.unknown_0x00
    to_phys.unknown_0x04 = from_phys.unknown_0x04
    to_phys.unknown_0x08 = from_phys.unknown_0x08
    to_phys.unknown_0x0C = from_phys.unknown_0x0C
    to_phys.unknown_0x10 = from_phys.unknown_0x10
    
    to_phys.bones.clear()
    for from_bone in from_phys.bones:
        to_bone = to_phys.bones.add()
        to_bone.has_name = from_bone.has_name
        to_bone.name = from_bone.name
        to_bone.unknown_0x00 = from_bone.unknown_0x00
        to_bone.unknown_0x04 = from_bone.unknown_0x04
        to_bone.unknown_0x08 = from_bone.unknown_0x08
        to_bone.unknown_0x0C = from_bone.unknown_0x0C
        to_bone.nameless_data = from_bone.nameless_data
    
    to_phys.links.clear()
    for from_link in from_phys.links:
        to_link = to_phys.links.add()
        to_link.parent       = from_link.parent
        to_link.child        = from_link.child
        to_link.mass         = from_link.mass
        to_link.unknown_0x04 = from_link.unknown_0x04
        to_link.radius       = from_link.radius

class CopyPhysics(bpy.types.Operator):
    bl_idname = "GFSTOOLS.CopyPhysics".lower()
    bl_label = "Copy Physics"
    
    clipboard_empty: bpy.props.BoolProperty()
    
    def execute(self, context):
        props    = context.armature.GFSTOOLS_ModelProperties.physics
        sc_props = context.scene.GFSTOOLS_SceneProperties.physics_clipboard
        
        # No way to clone a property, so we have to do it manually...
        clone_physics(props, sc_props)
        
        self.report({'INFO'}, "Copied physics to clipboard")
        return {'FINISHED'}


class PastePhysics(bpy.types.Operator):
    bl_idname = "GFSTOOLS.PastePhysics".lower()
    bl_label = "Paste Physics"
    bl_options = {'UNDO'}
    
    clipboard_empty: bpy.props.BoolProperty()
    
    def execute(self, context):
        props    = context.armature.GFSTOOLS_ModelProperties.physics
        sc_props = context.scene.GFSTOOLS_SceneProperties.physics_clipboard
        
        # No way to clone a property, so we have to do it manually...
        clone_physics(sc_props, props)
        props.active_bone_idx = 0
        props.active_link_idx = 0
        
        self.report({'INFO'}, "Pasted physics from clipboard")
        return {'FINISHED'}


class ShowColliders(bpy.types.Operator):
    bl_idname = "GFSTOOLS.ShowColliders".lower()
    bl_label = "Show All Colliders"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        err = check_armature_context(self, context)
        if len(err): return err
        
        armature = context.active_object
        for obj in armature.children:
            if obj.type == "MESH":
                if obj.data.GFSTOOLS_MeshProperties.is_collider():
                    obj.hide_set(False)
        
        self.report({'INFO'}, f"Made all colliders on '{armature.name}' visible")
        return {'FINISHED'}


class HideColliders(bpy.types.Operator):
    bl_idname = "GFSTOOLS.HideColliders".lower()
    bl_label = "Hide All Colliders"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        err = check_armature_context(self, context)
        if len(err): return err
        
        armature = context.active_object
        for obj in armature.children:
            if obj.type == "MESH":
                if obj.data.GFSTOOLS_MeshProperties.is_collider():
                    obj.hide_set(True)
        
        self.report({'INFO'}, f"Hid all colliders on '{armature.name}'")
        return {'FINISHED'}
    
def check_armature_context(self, context):
    # Basic validation that should never be encountered from the UI
    if context.active_object is None:
        self.report({'ERROR'}, "Something went wrong: No active object")
        return {"CANCELLED"}
    elif context.armature is None:
        self.report({'ERROR'}, "Something went wrong: No active armature")
        return {"CANCELLED"}
    elif context.active_object.data != context.armature:
        self.report({'ERROR'}, "Something went wrong: Active object '{context.active_object.name}' does not contain the active armature '{context.armature.name}'")
        return {"CANCELLED"}
    else:
        return {}

class CreateCollider(bpy.types.Operator):
    bl_idname = "GFSTOOLS.CreateColliders".lower()
    bl_label = "Create Collider"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        err = check_armature_context(self, context)
        if len(err): return err
        
        # Now create the collider...
        armature = context.armature
        props   = armature.GFSTOOLS_ModelProperties.physics
        
        if props.attach_colliders_to_bone:
            bone_name = props.active_bone
        else:
            bone_name = ''
        c = make_collider(True, "Capsule", 10, 5, [1., 0., 0., 0.,
                                                   0., 1., 0., 0.,
                                                   0., 0., 1., 0.,
                                                   0., 0., 0., 1.], bone_name, context.active_object)
        
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = c
        c.select_set(True)
        
        self.report({'INFO'}, f"Created new collider '{c.name}'")
        return {'FINISHED'}


class ConvertColliders(bpy.types.Operator):
    bl_idname = "GFSTOOLS.ConvertColliders".lower()
    bl_label  = "<ERROR>"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        err = check_armature_context(self, context)
        if len(err): return err
        
        bpy_armature_obj = context.active_object
        bpy_armature     = bpy_armature_obj.data
        props            = bpy_armature.GFSTOOLS_ModelProperties.physics


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
                                    "active_bone_idx",
                                    manage_link_idxs=True)
    
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
                                    "active_link_idx",
                                    manage_link_idxs=False)
    
    @classmethod
    def poll(cls, context):
        return context.armature is not None

    def draw_header(self, context):
        armature = context.armature
        layout = self.layout
        props = armature.GFSTOOLS_ModelProperties.physics
        
        layout.prop(props, "has_physics", text="")

    def draw(self, context):
        armature = context.armature
        layout = self.layout
        
        props = armature.GFSTOOLS_ModelProperties.physics
        
        ctr = layout.column()
        
        # Copy / Paste
        row = ctr.row()
        rc = row.column()
        rc.operator(CopyPhysics.bl_idname)
        rc = row.column()
        rc.operator(PastePhysics.bl_idname)
        
        # Show / Hide Colliders
        row = ctr.row()
        rc = row.column()
        rc.operator(ShowColliders.bl_idname)
        rc = row.column()
        rc.operator(HideColliders.bl_idname)
        
        # Create Colliders
        row = ctr.row()
        rc = row.column()
        rc.operator(CreateCollider.bl_idname)
        rc = row.column()
        rcr = rc.row()
        rcr.prop(props, "attach_colliders_to_bone")
        rcr = rc.row()
        rcr.prop_search(props, "active_bone", armature, "bones")
        rcr.enabled = props.attach_colliders_to_bone
        
        # Repair material
        row = ctr.row()
        row.operator(RepairColliderMaterial.bl_idname)
        
        # Remaining props
        ctr.prop(props, "unknown_0x00")
        ctr.prop(props, "unknown_0x04")
        ctr.prop(props, "unknown_0x08")
        ctr.prop(props, "unknown_0x0C")
        ctr.prop(props, "unknown_0x10")

    @classmethod
    def register(cls):
        bpy.utils.register_class(CopyPhysics)
        bpy.utils.register_class(PastePhysics)
        bpy.utils.register_class(ShowColliders)
        bpy.utils.register_class(HideColliders)
        bpy.utils.register_class(CreateCollider)
        bpy.utils.register_class(BoneEditBox)
        bpy.utils.register_class(LinkEditBox)
        bpy.utils.register_class(OBJECT_UL_GFSToolsPhysBoneUIList)
        bpy.utils.register_class(OBJECT_UL_GFSToolsPhysLinkUIList)
        bpy.utils.register_class(cls.bone_list)
        bpy.utils.register_class(cls.link_list)
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(CopyPhysics)
        bpy.utils.unregister_class(PastePhysics)
        bpy.utils.unregister_class(ShowColliders)
        bpy.utils.unregister_class(HideColliders)
        bpy.utils.unregister_class(CreateCollider)
        bpy.utils.unregister_class(BoneEditBox)
        bpy.utils.unregister_class(LinkEditBox)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsPhysBoneUIList)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsPhysLinkUIList)
        bpy.utils.unregister_class(cls.bone_list)
        bpy.utils.unregister_class(cls.link_list)
