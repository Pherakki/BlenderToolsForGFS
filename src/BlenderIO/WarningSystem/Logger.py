import textwrap

import bpy

from .UI import BasicErrorBox, BasicWarningBox
from .Warning import ReportableWarning, ReportableError


class ReportableErrorList(Exception):
    pass

class ErrorLogger:
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
        # This is wrong but can't do anything better for now.
        # Ideally should load all errors into a single popup.
        if len(self.errors):
            err = self.errors[0]
            if err.HAS_DISPLAYABLE_ERROR:
                err.showErrorData()
        
            msg = f"({len(self.errors)}) error(s) were detected when trying to export. The first error is shown below, and displayed if appropriate."
            msg += "\n\n" + err.message
            if err.HAS_DISPLAYABLE_ERROR:
                msg += "\n\n" + "The relevant data has been selected for you."
            bpy.ops.gfstools.basicerrorbox("INVOKE_DEFAULT", message=msg)
        self.errors.clear()

    def log_error_message(self, message):
        self._errors.append(ReportableError(message))

    def log_error(self, error):
        self._errors.append(error)
        
    def digest_warnings(self):
        # This is wrong but can't do anything better for now.
        # Ideally should load all errors into a single popup.
        if len(self.warnings):
            msg = ""
            lines = []
            for i, warning in enumerate(self.warnings):
                current_warning = '\n'.join([
                    '\n'.join(textwrap.wrap(line, 80, break_long_words=False, replace_whitespace=False))
                    for line in f"{i+1}) {warning}".splitlines() if line.strip() != ''
                ])
                if len(lines) + len(current_warning) < 15:
                    lines.extend(current_warning)
                else:
                    break
            bpy.ops.gfstools.basicwarningbox("INVOKE_DEFAULT", message='\n'.join(msg))
        self.warnings.clear()

    def log_warning_message(self, message):
        self._errors.append(ReportableError(message))
        
    def log_warning(self, warning):
        self._warning.append(warning)
        
    def clear(self):
        self._errors.clear()
        self._warnings.clear()
