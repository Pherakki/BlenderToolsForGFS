class ReportableErrorList(Exception):
    pass

class ErrorsStateMachine:
    def __init__(self):
        self._errors   = []
        self._warnings = []
        
    @property
    def errors(self):
        return self._errors
    
    @property
    def warnings(self):
        return self._warnings
        
    def digest_errors(self):
        if len(self.errors):
            for error in self.errors:
                print("<<DEBUG - ERROR>>", error)
            self._errors = []
            #raise ReportableErrorList(self.errors)

    def log_error(self, error):
        self._errors.append(error)
        
    def digest_warnings(self):
        if len(self.warnings):
            for warning in self.warnings:
                print("<<DEBUG - WARNING>>", warning)
            self._warnings = []
            #raise ReportableWarningList(self.errors)

    def log_warning(self, warning):
        self._warning.append(warning)
    
import bpy
import functools


class ErrorPopup(bpy.types.Operator):
    bl_idname = "gfsblendertools.testerrorpopup"
    bl_label = "GFS Blender Tools: Error Detected"
    bl_options = {'REGISTER'}

    message: bpy.props.StringProperty()
    error_idx: bpy.props.IntProperty(min=-1, default=-1)
    should_remove = bpy.props.BoolProperty(default=False)

    def __init__(self):
        self.should_remove = False

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.should_remove = True
        return {'FINISHED'}

    def __del__(self):
        if not self.should_remove:
            bpy.ops.gfsblendertools.testerrorpopup('INVOKE_DEFAULT', message="I am a test 2", error_idx=self.error_idx)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=512)

    def check(self, context):
        """Allows the dialog to redraw"""
        return True

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        for substr in self.chunk_string(self.message, 80):
            col.label(text=substr)
            
        row = col.row()
        row.operator(PreviousErrorOperator.bl_idname)
        row.operator(NextErrorOperator.bl_idname)
    
    def chunk_string(self, string_, size):
        lines = []
        for marked_line in string_.split('\n'):
            current_length = 0
            current_bit = ""
            for word in marked_line.split(" "):
                current_length += len(word) + 1
                if (current_length) > size:
                    lines.append(current_bit)
                    current_length = len(word) + 1
                    current_bit = word + " "
                else:
                    current_bit += word + " "
            if len(current_bit):
                lines.append(current_bit)
        return lines

class PreviousErrorOperator(bpy.types.Operator):
    bl_idname = "gfsblendertools.testerrorpopup_prev"
    bl_label = "Previous"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print("DID PREVIOUS")
        return {'FINISHED'}

class NextErrorOperator(bpy.types.Operator):
    bl_idname = "gfsblendertools.testerrorpopup_next"
    bl_label = "Next"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print("DID NEXT")
        return {'FINISHED'}
    

def handle_warning_system(function):
    """
    The mode of operation for this function is heavily derived from the Google-forms reporter at
    https://github.com/TheDuckCow/user-report-wrapper
    """
    @functools.wraps(function)
    def handled_execute(operator, context):
        try:
            return function(operator, context)
        finally:
            bpy.ops.gfsblendertools.testerrorpopup('INVOKE_DEFAULT', message="I am a test")

    return handled_execute
