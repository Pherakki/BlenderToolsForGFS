import bpy


class OBJECT_PT_GFSToolsPinnedArmatureToolsPanel(bpy.types.Panel):
    bl_label = "GFSTools Armature"
    bl_idname = "OBJECT_PT_GFSToolsPinnedArmatureTools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod 
    def poll(cls, context):
        return context.armature is not None
    
    def draw(self, context):
        layout = self.layout

        obj = context.object

        active_bone = [None]

        # Need to have a drop-down list of bones here
        
        row = layout.row()
        row.label(text="TODO: ADD BONE DROPDOWN")
        # Check if a pinned armature exists for the node already;
        # enable / disable the below as appropriate
        # These are supposed to be ops on the pinned armature attached to
        # the selected node
        #row.operator("operator_name", "Create")
        #row.operator("operator_name", "Delete")
        #row.operator("operator_name", "Trim") # Remove unused bones
