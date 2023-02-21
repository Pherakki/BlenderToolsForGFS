from ........serialization.Serializable import Serializable
from .....CommonStructures import ObjectName
from .Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafBoardPolygon(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness

        self.type = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        
        
        self.polygon = None
        self.embedded_file = EPLEmbeddedFile(endianness)
    
    def read_write(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_uint32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)

        if self.type == 1:
            PolygonType = EPLSquareBoardPolygon
        elif self.type == 2:
            PolygonType = EPLRectangleBoardPolygon
            
        self.polygon = rw.rw_new_obj(self.polygon, lambda: PolygonType(self.context.endianness), version)
        rw.rw_obj(self.embedded_file, version)


class EPLSquareBoardPolygon(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = EPLLeafCommonData2(endianness)
        self.unknown_0x04 = EPLLeafCommonData2(endianness)
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x24 = None
        self.unknown_0x28 = None
        
    def read_write(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        rw.rw_obj(self.unknown_0x04, version)
        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_uint32(self.unknown_0x18)
        
        if version > 0x01104280:
            self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)
            if version > 0x01104290:
                self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
                self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)


class EPLRectangleBoardPolygon(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = EPLLeafCommonData2(endianness)
        self.unknown_0x04 = EPLLeafCommonData2(endianness)
        self.unknown_0x08 = EPLLeafCommonData2(endianness)
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        
    def read_write(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        rw.rw_obj(self.unknown_0x04, version)
        rw.rw_obj(self.unknown_0x08, version)
        
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_uint32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
