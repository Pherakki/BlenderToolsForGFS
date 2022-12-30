from ...CommonStructures import SizedObjArray
from .MaterialBinary import MaterialBinary


class MaterialPayload(SizedObjArray):
    TYPECODE = 0x000100FB
    
    APPROVED_VERSIONS = set([
        #0x01104920,
        #0x01105000,
        #0x01105010,
        #0x01105020,
        #0x01105030,
        #0x01105040,
        #0x01105060,
        #0x01105070,
        #0x01105080,
        #0x01105090,
        0x01105100
        ])
    
    def __init__(self, endianness='>'):
        super().__init__(MaterialBinary, endianness)
