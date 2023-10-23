import bpy

from ..modelUtilsTest.Utils.TextWrapping import wrapText

class BasicErrorBox(bpy.types.Operator):
    bl_idname = "gfstools.basicerrorbox"
    bl_label = "GFS Blender Tools: Errors Detected"
    bl_options = {'REGISTER'}
    
    message: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=512)

    def check(self, context):
        """Allows the dialog to redraw"""
        return True

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        msg_lines = wrapText(self.message, 80)
        for line in msg_lines:
            col.label(text=line)
        
class BasicWarningBox(bpy.types.Operator):
    bl_idname = "gfstools.basicwarningbox"
    bl_label = "GFS Blender Tools: Warnings Detected"
    bl_options = {'REGISTER'}
    
    message: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=512)

    def check(self, context):
        """Allows the dialog to redraw"""
        return True

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        msg_lines = wrapText(self.message, 80)
        for line in msg_lines:
            col.label(text=line)
        
class UnhandledErrorBox(bpy.types.Operator):
    bl_idname = "gfstools.unhandlederrorbox"
    bl_label = "GFS Blender Tools: Unhandled Error Detected"
    bl_options = {'REGISTER'}
    
    exception_msg: bpy.props.StringProperty()
    context_msg:   bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=512)

    def check(self, context):
        """Allows the dialog to redraw"""
        return True

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        msg = f"BlenderToolsForGFS has encountered an unhandled error. The exception is:\n\n"         \
        f"{self.exception_msg}\n\n"                                                                   \
        f"A full stacktrace has been printed to the console.\n"                                       \
        f"Since all exceptions should be handled by the internal error-reporting system, "            \
        f"this is a bug. Please report this at https://github.com/Pherakki/BlenderToolsForGFS/issues" \
        f" with the following information:\n"                                                         \
        f"1) {self.context_msg}\n"                                                                    \
        f"2) The stacktrace that has been printed to the console.\n"                                  \
        f"3) Any further information that you think may be relevant."
        
        msg_lines = wrapText(msg, 80)
        for line in msg_lines:
            col.label(text=line)
        

# This is going to be prohibitively complex to set up due to Blender's restrictions
# on initialising variables on a class
# It's going to run into race conditions and all sorts of terrible things
class ErrorPopup(bpy.types.Operator):
    bl_idname = "gfstools.testerrorpopup"
    bl_label = "GFS Blender Tools: Error Detected"
    bl_options = {'REGISTER'}
    active_instance = None

    error_idx:     bpy.props.IntProperty(min=-1, default=-1)
    should_remove: bpy.props.BoolProperty(default=False)
    
    __slots__ = ("errors",)

    @classmethod
    def update_instance_error_idx(cls, idx):
        cls.active_instance.error_idx += idx

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.should_remove = True
        self.error_idx = -1
        return {'FINISHED'}

    # This worked at one point, dunno why not now
    # def __del__(self):
    #     if hasattr(self, "should_remove"):
    #         print("DELETING - SHOULD REMOVE?", self.should_remove)
    #         if not self.should_remove:
    #             print("NO DELETE!")
    #             bpy.ops.gfsblendertools.testerrorpopup('INVOKE_DEFAULT', message="I am a test 2", error_idx=self.error_idx)
    #         else:
    #             print("DELETED!")
    #             ErrorPopup.active_instance = None

    def invoke(self, context, event):
        self.errors = []
        ErrorPopup.active_instance = self
        return context.window_manager.invoke_props_dialog(self, width=512)

    def check(self, context):
        """Allows the dialog to redraw"""
        return True

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        
        if self.error_idx == -1:
            text = f"{len(self.errors)} errors were found when trying to export. Click 'Next' to view the first error."
        else:
            text = self.errors[self.error_idx].message
            
        for line in wrapText(text, 80):
            col.label(text=line)
            
        col.label(text=str(self.error_idx))
            
        row = col.row()
        if self.error_idx > -1:
            row.operator(PreviousErrorOperator.bl_idname)
        if self.error_idx < (len(self.errors) - 1):
            row.operator(NextErrorOperator.bl_idname)


class PreviousErrorOperator(bpy.types.Operator):
    bl_idname = "gfsblendertools.testerrorpopup_prev"
    bl_label = "Previous"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ErrorPopup.update_instance_error_idx(-1)
        return {'FINISHED'}

class NextErrorOperator(bpy.types.Operator):
    bl_idname = "gfsblendertools.testerrorpopup_next"
    bl_label = "Next"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ErrorPopup.update_instance_error_idx(1)
        return {'FINISHED'}
    