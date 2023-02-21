from ........serialization.Serializable import Serializable
from .....CommonStructures import ObjectName
from .Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafGlitterPolygon(Serializable):
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
        
        self.unknown_0x20 = None
        self.unknown_0x28 = EPLLeafCommonData(endianness)
        self.unknown_0x2C = None
        
        self.unknown_0x30 = EPLLeafCommonData2(endianness)
        self.unknown_0x34 = EPLLeafCommonData2(endianness)
        self.unknown_0x38 = None
        self.unknown_0x3C = None
        
        self.unknown_0x40 = None
        self.unknown_0x44 = None
        self.has_embedded_file = None
            
        self.polygon = None
        self.embedded_file = EPLEmbeddedFile(endianness)
    
    
    def read_write(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_uint32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_uint32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        
        rw.rw_obj(self.unknown_0x28, version)
        self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
        rw.rw_obj(self.unknown_0x30, version)
        rw.rw_obj(self.unknown_0x34, version)
        self.unknown_0x38 = rw.rw_float32(self.unknown_0x38)
        self.unknown_0x3C = rw.rw_float32(self.unknown_0x3C)
        
        self.unknown_0x40 = rw.rw_float32(self.unknown_0x40)
        self.unknown_0x44 = rw.rw_float32(self.unknown_0x44)

        if self.type == 1:
            PolygonType = EPLGlitterPolygonExplosion
        elif self.type == 2:
            PolygonType = EPLGlitterPolygonSplash
        elif self.type == 3:
            PolygonType = EPLGlitterPolygonCylinder
        elif self.type == 4:
            PolygonType = EPLGlitterPolygonWall
        else:
            raise NotImplementedError(f"Unknown EPLLeafGlitterPolygon type '{self.type}'")
        
        self.polygon = rw.rw_new_obj(self.polygon, lambda: PolygonType(self.context.endianness), version)
        self.has_embedded_file = rw.rw_uint8(self.has_embedded_file)
        if self.has_embedded_file:
            rw.rw_obj(self.embedded_file, version)

class EPLLeafGlitterPolygon2(EPLLeafGlitterPolygon):
    pass

class EPLGlitterPolygonExplosion(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness

        self.unknown_0x00 = None
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 2)
        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        

class EPLGlitterPolygonSplash(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness

        self.unknown_0x00 = EPLLeafCommonData(endianness)
        self.unknown_0x04 = EPLLeafCommonData(endianness)
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
    
    def read_write(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        rw.rw_obj(self.unknown_0x04, version)
        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)


class EPLGlitterPolygonCylinder(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness

        self.unknown_0x00 = EPLLeafCommonData(endianness)
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
    
    def read_write(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_uint32(self.unknown_0x2C)


class EPLGlitterPolygonWall(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness

        self.unknown_0x00 = EPLLeafCommonData(endianness)
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
    
    def read_write(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
