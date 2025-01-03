from ....ObjectNameModule import ObjectName
from ..Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2


class EPLLeafFlashPolygon:
    def __init__(self):
        self.type = None
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        self.unknown_0x24 = EPLLeafCommonData()
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        self.unknown_0x30 = None
        self.unknown_0x34 = None
        
        self.polygon = None
        self.embedded_file = EPLEmbeddedFile()
        
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Leaf::FlashPolygon] {self.type}"
    
    def exbip_rw(self, rw, version):
        self.type         = rw.rw_uint32(self.type)
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_uint32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_uint32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        
        rw.rw_obj(self.unknown_0x24, version)
        if version > 0x01104700:
            self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        if version > 0x01104050:
            self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
            self.unknown_0x30 = rw.rw_float32(self.unknown_0x30)

        if self.type == 1:
            PolygonType = EPLFlashPolygonRadiation
        elif self.type == 2:
            PolygonType = EPLFlashPolygonExplosion
        elif self.type == 3:
            PolygonType = EPLFlashPolygonRing
        elif self.type == 4:
            PolygonType = EPLFlashPolygonSplash
        elif self.type == 5:
            PolygonType = EPLFlashPolygonCylinder
        else:
            raise NotImplementedError(f"Unknown EPLLeafFlashPolygon type '{self.type}'")
            
        self.polygon = rw.rw_dynamic_obj(self.polygon, PolygonType, version)
        rw.rw_obj(self.embedded_file, version)


class EPLFlashPolygonRadiation:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_uint32(self.unknown_0x2C) # Flags?


class EPLFlashPolygonExplosion:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 2)
        self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)


class EPLFlashPolygonRing:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData()
        self.unknown_0x04 = EPLLeafCommonData()
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        self.unknown_0x30 = None
        self.unknown_0x34 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_obj(self.unknown_0x04, version)
        self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x28 = rw.rw_float32s(self.unknown_0x28, 2)
        
        self.unknown_0x30 = rw.rw_float32(self.unknown_0x30)
        self.unknown_0x34 = rw.rw_uint32(self.unknown_0x34) # Flags?


class EPLFlashPolygonSplash:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData()
        self.unknown_0x04 = EPLLeafCommonData()
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        self.unknown_0x30 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_obj(self.unknown_0x04, version)
        self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x28 = rw.rw_float32s(self.unknown_0x28, 2)
        
        self.unknown_0x30 = rw.rw_float32(self.unknown_0x30)


class EPLFlashPolygonCylinder:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData()
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        self.unknown_0x2C = None
        self.unknown_0x30 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_obj(self.unknown_0x00, version)
        if version <= 0x01104040:
            CommonType = EPLLeafCommonData
        else:
            CommonType = EPLLeafCommonData2
        self.unknown_0x04 = rw.rw_dynamic_obj(self.unknown_0x04, CommonType, version)

        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32s(self.unknown_0x24, 2)
        self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
        self.unknown_0x30 = rw.rw_uint32(self.unknown_0x30) # Flags?
