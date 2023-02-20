import bpy
import functools
import traceback


def handle_warning_system(unhandled_context_msg):
    def impl(function):
        """
        The mode of operation for this function is heavily derived from the Google-forms reporter at
        https://github.com/TheDuckCow/user-report-wrapper
        """
        @functools.wraps(function)
        def handled_execute(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except Exception as e:
                if getattr(self, "debug_mode", False):
                    raise e
                else:
                    print(''.join(traceback.TracebackException.from_exception(e).format()))
                    bpy.ops.gfstools.unhandlederrorbox('INVOKE_DEFAULT', exception_msg=str(e), context_msg=unhandled_context_msg)
            else:
                return {"CANCELLED"}
        return handled_execute
    return impl
