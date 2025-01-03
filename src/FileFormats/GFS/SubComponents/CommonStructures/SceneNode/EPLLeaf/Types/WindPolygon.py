from ....ObjectNameModule import ObjectName
from ..Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafWindPolygon:
    def __init__(self):
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
        self.unknown_0x2C = None
        self.unknown_0x34 = None
        self.unknown_0x3C = None
        
        self.unknown_0x44 = None
        self.unknown_0x48 = None
        self.unknown_0x4C = None
        
        self.polygon = None
        self.embedded_file = EPLEmbeddedFile()

    def exbip_rw(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)

        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_uint32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_uint32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_uint32(self.unknown_0x1C)
        
        
        if version <= 0x1104040:
            CommonType = EPLLeafCommonData
        else:
            CommonType = EPLLeafCommonData2
            
        self.unknown_0x20 = rw.rw_dynamic_obj(self.unknown_0x20, CommonType, version)
        self.unknown_0x24 = rw.rw_float32s(self.unknown_0x24, 2)
        self.unknown_0x2C = rw.rw_float32s(self.unknown_0x2C, 2)
        self.unknown_0x34 = rw.rw_float32s(self.unknown_0x34, 2)
        
        self.unknown_0x3C = rw.rw_float32s(self.unknown_0x3C, 2)
        
        if version > 0x01104700:
            self.unknown_0x44 = rw.rw_float32(self.unknown_0x44)
        if version > 0x01104050:
            self.unknown_0x48 = rw.rw_float32(self.unknown_0x48)
            self.unknown_0x4C = rw.rw_float32(self.unknown_0x4C)
         
        if self.type == 1:
            PolygonType = EPLWindPolygonSpiral
        elif self.type == 2:
            PolygonType = EPLWindPolygonExplosion
        elif self.type == 3:
            PolygonType = EplWindPolygonBall
        else:
            raise NotImplementedError(f"Unknown EPLLeafWindPolygon type: '{self.type}'")
            
        self.polygon = rw.rw_dynamic_obj(self.polygon, PolygonType, version)
        rw.rw_obj(self.embedded_file, version)


class EPLWindPolygonSpiral:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData()
        self.unknown_0x04 = EPLLeafCommonData()
        self.unknown_0x08 = EPLLeafCommonData()
        
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x24 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        rw.rw_obj(self.unknown_0x04, version)
        rw.rw_obj(self.unknown_0x08, version)

        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)
        
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_uint32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_float32s(self.unknown_0x2C, 2)


class EPLWindPolygonExplosion:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData()
        
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None

    def exbip_rw(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)

        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        if version > 0x01104080:
            self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)


class EplWindPolygonBall:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData()
        self.unknown_0x04 = EPLLeafCommonData()
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
    
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        rw.rw_obj(self.unknown_0x04, version)

        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_uint32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)
