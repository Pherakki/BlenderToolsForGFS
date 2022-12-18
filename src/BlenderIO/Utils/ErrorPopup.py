import functools
import traceback

import bpy


class ReportableException(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message


class MessagePopup(bpy.types.Operator):
    bl_idname = "gfsblendertools.errorpopup"
    bl_label = "GFS Blender Tools: Error Detected"
    bl_options = {'REGISTER'}

    message: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def check(self, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=512)

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        for substr in self.chunk_string(self.message, 80):
            col.label(text=substr)

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


def handle_errors(function):
    """
    The mode of operation for this function is heavily derived from the Google-forms reporter at
    https://github.com/TheDuckCow/user-report-wrapper
    """
    @functools.wraps(function)
    def handled_execute(operator, context):
        try:
            return function(operator, context)
        except ReportableException as e:
            operator.report({'ERROR'}, "Error popup invoked: Full details printed to console.")
            print(f'Error popup invoked. Popup message:\n{e.message}\n{traceback.format_exc()}')
            bpy.ops.gfsblendertools.errorpopup('INVOKE_DEFAULT', message=e.message)
            return {'CANCELLED'}
        except Exception as e:
            raise e

    return handled_execute
