class ReportableWarning:
    pass

class ReportableError:
    __slots__ = ("msg",)
    
    def __init__(self, msg):
        self.msg = msg
    
    def showErrorData(self):
        pass
    
    def hideErrorData(self):
        pass
