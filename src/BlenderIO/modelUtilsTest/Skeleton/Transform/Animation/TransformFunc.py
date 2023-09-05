def NOT_IMPLEMENTED():
    raise NotImplementedError


def TransformFunc(default_transform, 
                  vector   =NOT_IMPLEMENTED, 
                  matrix3x3=NOT_IMPLEMENTED,
                  matrix4x4=NOT_IMPLEMENTED,
                  quat     =NOT_IMPLEMENTED):
    class Func:
        pass
    
    # Shaves off about one hundred nanoseconds per call to directly
    # set the class methods this way instead of wrapping them.
    # Micro-optimisation, woohoo!
    setattr(Func, "__call__",  staticmethod(default_transform))
    setattr(Func, "vector",    staticmethod(vector))
    setattr(Func, "matrix3x3", staticmethod(matrix3x3))
    setattr(Func, "matrix4x4", staticmethod(matrix4x4))
    setattr(Func, "quat",      staticmethod(quat))
    Func.__name__ = "TransformFunc"
    
    return Func()
