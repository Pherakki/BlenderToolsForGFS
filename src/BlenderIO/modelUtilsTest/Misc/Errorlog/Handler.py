import functools
import traceback


def display_exceptions(unhandled_context_msg, unhandled_errorbox):
    def impl(function):
        @functools.wraps(function)
        def handled_execute(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except Exception as e:
                if getattr(self, "debug_mode", False):
                    raise e
                else:
                    print(''.join(traceback.TracebackException.from_exception(e).format()))
                    unhandled_errorbox('INVOKE_DEFAULT', exception_msg=str(e), context_msg=unhandled_context_msg)
                    return {"CANCELLED"}
        return handled_execute
    return impl
