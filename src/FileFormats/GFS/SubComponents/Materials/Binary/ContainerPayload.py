from ...CommonStructures import SizedObjArray
from .MaterialBinary import MaterialBinary


class MaterialPayload(SizedObjArray):
    TYPECODE = 0x000100FB
    
    def __init__(self):
        super().__init__(MaterialBinary)
