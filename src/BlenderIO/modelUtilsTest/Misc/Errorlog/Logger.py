import bpy

from ...API.Operator import get_op
from ...Utils.TextWrapping import wrapText
from .Warnings import ReportableError
from .Handler import display_exceptions
from .UI import ErrorBoxBase
from .UI import WarningBoxBase
from .UI import UnhandledBoxBase


def ErrorLogBase(namespace, plugin_name, unhandled_error_message):
    class ErrorLog:
        _popup_warningbox = WarningBoxBase(namespace, plugin_name)
        _popup_errorbox   = ErrorBoxBase(namespace, plugin_name)
        _popup_unhandled  = UnhandledBoxBase(namespace, plugin_name, unhandled_error_message)
        
        _make_warning_popup   = get_op(_popup_warningbox)
        _make_error_popup     = get_op(_popup_errorbox)
        _make_unhandled_popup = get_op(_popup_unhandled)
        
        def __init__(self):
            self._errors   = []
            self._warnings = []

        #############
        # STATE API #
        #############
        def clear(self):
            self._errors.clear()
            self._warnings.clear()

        ################
        # WARNINGS API #
        ################
        def has_warnings(self):
            return len(self._warnings) > 0
          
        @property
        def warnings(self):
            return self._warnings
        
        def log_warning_message(self, message):
            """Used to create a generic warning message from a string."""
            self._warnings.append(ReportableError(message))
            
        def log_warning(self, warning):
            """Used to create a specialised warning message using a class derived from ErrorLog.BaseError."""
            assert hasattr(warning, "msg") and hasattr(warning, "HAS_DISPLAYABLE_ERROR"), f"Logged warning must be a class with a member 'msg' and class member 'HAS_DISPLAYABLE_ERROR', received '{type(warning)}'. Use log_warning_message for string-like warning messages"
            self._warnings.append(warning)
            
        def digest_warnings(self, debug_mode=False):
            """Launch warning window if any warnings exist, and clear warning list."""
            # This is wrong but can't do anything better for now.
            # Ideally should load all errors into a single popup.
            if len(self.warnings):
                lines = []
                for i, warning in enumerate(self.warnings):
                    warning_text = f"{i+1}) {warning.msg}"
                    current_warning = wrapText(warning_text, 80)
                    if len(lines) + len(current_warning) < 15:
                        lines.append(warning_text)
                        print(warning.msg)
                    else:
                        lines.append(f"Plus {len(self.warnings) - i} additional warnings. Check the console for details.")
                        for warning in self.warnings[i:]:
                            print(warning.msg)
                        break
                
                self._make_warning_popup("INVOKE_DEFAULT", message='\n'.join(lines))
            self.warnings.clear()
        
        ##############
        # ERRORS API #
        ##############
        def has_errors(self):
            return len(self._errors) > 0
            
        @property
        def errors(self):
            return self._errors

        def log_error_message(self, message):
            """Used to create a generic error message from a string."""
            self._errors.append(ReportableError(message))
    
        def log_error(self, error):
            """Used to create a specialised error message using a class derived from ErrorLog.BaseError."""
            assert hasattr(error, "msg") and hasattr(error, "HAS_DISPLAYABLE_ERROR"), f"Logged error must be a class with a member 'msg' and class member 'HAS_DISPLAYABLE_ERROR', received '{type(error)}'. Use log_error_message for string-like error messages"
            self._errors.append(error)
            
        def digest_errors(self, debug_mode=False):
            """Launch error window if any errors exist, and clear error list."""
            # This is wrong but can't do anything better for now.
            # Ideally should load all errors into a single popup.
            if len(self.errors):
                if debug_mode:
                    raise Exception(self.errors[0].msg)
                err = self.errors[0]
                if err.HAS_DISPLAYABLE_ERROR:
                    err.showErrorData()
            
                msg = f"({len(self.errors)}) error(s) were detected when trying to export. The first error is shown below, and displayed if appropriate."
                msg += "\n" + err.msg
                if err.HAS_DISPLAYABLE_ERROR:
                    msg += "\n" + "The relevant data has been selected for you."
                self._make_error_popup("INVOKE_DEFAULT", message=msg)
            self.errors.clear()
    
        #########################
        # CONVENIENCE UTILITIES #
        #########################
        # Having these utils here keeps everything under a single namespace,
        # making the errorlog much easier to use.
        @property
        def BaseError(self):
            return ReportableError
        
        @classmethod
        def display_exceptions(cls, unhandled_context_msg):
            return display_exceptions(unhandled_context_msg, cls._make_unhandled_popup)
        
        #################
        # BPY UTILITIES #
        #################      
        # Registry functions so that *only* the errorlog needs to be registered
        # with bpy for the entire errorlog to work.
        
        @classmethod
        def register(cls):
            bpy.utils.register_class(cls._popup_warningbox)
            bpy.utils.register_class(cls._popup_errorbox)
            bpy.utils.register_class(cls._popup_unhandled)
        
        @classmethod
        def unregister(cls):
            bpy.utils.unregister_class(cls._popup_warningbox)
            bpy.utils.unregister_class(cls._popup_errorbox)
            bpy.utils.unregister_class(cls._popup_unhandled)

    return ErrorLog
