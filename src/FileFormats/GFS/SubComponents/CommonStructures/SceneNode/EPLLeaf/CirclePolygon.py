from .......serialization.Serializable import Serializable
from ....CommonStructures import ObjectName
from .Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2


class EPLLeafCirclePolygon(Serializable):
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
        self.unknown_0x24 = None
        
        self.polygon = None
        self.embedded_file = EPLEmbeddedFile(endianness)
        
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Leaf::CirclePolygon] {self.type}"
    
    def read_write(self, rw, version):
        self.type         = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_uint32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_uint32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)

        if self.type == 1:
            PolygonType = EPLCirclePolygonRing
        elif self.type == 2:
            PolygonType = EPLCirclePolygonTrajectory
        elif self.type == 3:
            PolygonType = EPLCirclePolygonFill
        elif self.type == 4:
            PolygonType = EPLCirclePolygonHoop
        else:
            raise NotImplementedError(f"Unknown EPLLeafCirclePolygon type '{self.type}'")
        
        self.polygon = rw.rw_new_obj(self.polygon, lambda: PolygonType(self.context.endianness), version)
        
        if self.type != 1 and self.type != 3:
            rw.rw_obj(self.embedded_file, version)


class EPLCirclePolygonRing(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = EPLLeafCommonData(endianness)
        self.unknown_0x08 = EPLLeafCommonData(endianness)
        self.unknown_0x0C = None
        
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        rw.rw_obj(self.unknown_0x04, version)
        rw.rw_obj(self.unknown_0x08, version)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        
        self.unknown_0x14 = rw.rw_uint32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_uint32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_uint32(self.unknown_0x1C)


class EPLCirclePolygonTrajectory(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = EPLLeafCommonData(endianness)
        self.unknown_0x0C = EPLLeafCommonData(endianness)
        
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None

    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        rw.rw_obj(self.unknown_0x08, version)
        rw.rw_obj(self.unknown_0x0C, version)
        
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)


class EPLCirclePolygonFill(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = EPLLeafCommonData(endianness)
        self.unknown_0x08 = EPLLeafCommonData2(endianness)
        self.unknown_0x0C = EPLLeafCommonData2(endianness)
    
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        rw.rw_obj(self.unknown_0x04, version)
        rw.rw_obj(self.unknown_0x08, version)
        rw.rw_obj(self.unknown_0x0C, version)


class EPLCirclePolygonHoop(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        
        self.unknown_0x0C = EPLLeafCommonData(endianness)
        self.unknown_0x10 = None
        self.unknown_0x18 = EPLLeafCommonData2(endianness)
        self.unknown_0x1C = EPLLeafCommonData2(endianness)
        
        self.unknown_0x20 = EPLLeafCommonData2(endianness)
        self.unknown_0x24 = None
        self.unknown_0x28 = None
    
    
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        rw.rw_obj(self.unknown_0x0C, version)
        
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        rw.rw_obj(self.unknown_0x18, version)
        rw.rw_obj(self.unknown_0x1C, version)
        
        rw.rw_obj(self.unknown_0x20, version)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
