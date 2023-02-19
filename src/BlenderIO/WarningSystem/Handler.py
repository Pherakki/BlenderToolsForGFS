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
        def handled_execute(operator, context):
            try:
                return function(operator, context)
            except Exception as e:
                print(''.join(traceback.TracebackException.from_exception(e).format()))
                bpy.ops.gfsblendertools.unhandlederrorbox('INVOKE_DEFAULT', exception_msg=str(e), context_msg=unhandled_context_msg)
    
        return handled_execute
    return impl
