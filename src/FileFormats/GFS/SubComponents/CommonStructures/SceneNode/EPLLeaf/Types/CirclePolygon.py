from ....ObjectNameModule import ObjectName
from ..Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2


class EPLLeafCirclePolygon:
    def __init__(self):
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
        self.embedded_file = EPLEmbeddedFile()
        
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Leaf::CirclePolygon] {self.type}"
    
    def exbip_rw(self, rw, version):
        self.type         = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_uint32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_uint32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        
        if version >= 0x1104051:
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
        
        self.polygon = rw.rw_dynamic_obj(self.polygon, PolygonType, version)
        
        if self.type != 1 and self.type != 3:
            rw.rw_obj(self.embedded_file, version)


class EPLCirclePolygonRing:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = EPLLeafCommonData()
        self.unknown_0x08 = EPLLeafCommonData()
        self.unknown_0x0C = None
        
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        rw.rw_obj(self.unknown_0x04, version)
        rw.rw_obj(self.unknown_0x08, version)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        
        self.unknown_0x14 = rw.rw_uint32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_uint32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_uint32(self.unknown_0x1C)


class EPLCirclePolygonTrajectory:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = EPLLeafCommonData()
        self.unknown_0x0C = EPLLeafCommonData()
        
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None

    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        rw.rw_obj(self.unknown_0x08, version)
        rw.rw_obj(self.unknown_0x0C, version)
        
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)


class EPLCirclePolygonFill:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = EPLLeafCommonData()
        self.unknown_0x08 = EPLLeafCommonData2()
        self.unknown_0x0C = EPLLeafCommonData2()
    
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        rw.rw_obj(self.unknown_0x04, version)
        rw.rw_obj(self.unknown_0x08, version)
        rw.rw_obj(self.unknown_0x0C, version)


class EPLCirclePolygonHoop:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        
        self.unknown_0x0C = EPLLeafCommonData()
        self.unknown_0x10 = None
        self.unknown_0x18 = EPLLeafCommonData2()
        self.unknown_0x1C = EPLLeafCommonData2()
        
        self.unknown_0x20 = EPLLeafCommonData2()
        self.unknown_0x24 = None
        self.unknown_0x28 = None
    
    
    def exbip_rw(self, rw, version):
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
