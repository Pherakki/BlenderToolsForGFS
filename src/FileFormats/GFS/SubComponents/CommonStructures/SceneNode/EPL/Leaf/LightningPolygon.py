from ........serialization.Serializable import Serializable
from .....CommonStructures import ObjectName
from .Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2


class EPLLeafLightningPolygon(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness

        self.type = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        self.unknown_0x30 = None
        self.unknown_0x38 = None
        self.unknown_0x40 = None
        self.unknown_0x48 = None
        self.unknown_0x50 = None
        self.unknown_0x58 = None
        self.unknown_0x60 = None
        self.unknown_0x64 = None
        
        self.polygon = None
        
    def read_write(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)

        self.unknown_0x10 = rw.rw_uint32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_uint32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        
        self.unknown_0x20 = rw.rw_uint32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_uint32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_uint32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_uint32(self.unknown_0x2C)
        
        self.unknown_0x30 = rw.rw_float32s(self.unknown_0x30, 2)
        self.unknown_0x38 = rw.rw_float32s(self.unknown_0x38, 2)
        self.unknown_0x40 = rw.rw_float32s(self.unknown_0x40, 2)
        self.unknown_0x48 = rw.rw_float32s(self.unknown_0x48, 2)
        self.unknown_0x50 = rw.rw_float32s(self.unknown_0x50, 2)
        self.unknown_0x58 = rw.rw_float32s(self.unknown_0x58, 2)
        
        if version > 0x01104050:
            self.unknown_0x60 = rw.rw_float32(self.unknown_0x60)
            self.unknown_0x64 = rw.rw_float32(self.unknown_0x64)

        if self.type == 1:
            PolygonType = EPLLightningPolygonRod
        elif self.type == 2:
            PolygonType = EPLLightningPolygonBall
        else:
            raise NotImplementedError(f"Unimplemented EPLLeafLightningPolygon type: '{self.type}'")

        self.polygon = rw.rw_new_obj(self.polygon, lambda: PolygonType(self.context.endianness), version)        


class EPLLightningPolygonRod(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 2)


class EPLLightningPolygonBall(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = EPLLeafCommonData(endianness)
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x24 = None
        self.unknown_0x28 = None
        
    def read_write(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_uint32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_uint32(self.unknown_0x28)
  