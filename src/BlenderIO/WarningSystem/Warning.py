class ReportableWarning:
    __slots__ = ("msg",)
    
    def __init__(self, msg):
        self.msg = msg

class ReportableError:
    __slots__ = ("msg",)
    
    HAS_DISPLAYABLE_ERROR = False
    
    def __init__(self, msg):
        self.msg = msg
    
    def showErrorData(self):
        pass
    
    def hideErrorData(self):
        pass
