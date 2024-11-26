from ....ObjectNameModule import ObjectName
from ..Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafModel:
    def __init__(self):
        self.type = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        
        self.unknown_0x10_P5R = None
        self.unknown_0x14_P5R = None
        self.unknown_0x18_P5R = None
        self.unknown_0x1C_P5R = None
        self.unknown_0x20_P5R = None
        self.unknown_0x24_P5R = None
        self.unknown_0x28_P5R = None
        self.unknown_0x2C_P5R = None
        
        self.unknown_0x10_MR = None
        self.unknown_0x14_MR = None
        self.unknown_0x18_MR = None
        self.unknown_0x20_MR = None
        self.unknown_0x28_MR = None
        self.unknown_0x2C_MR = None
        
        self.model = None
        self.has_embedded_file = None
        self.embedded_file = EPLEmbeddedFile()


    def exbip_rw(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        if version > 0x01104050:
            self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
            self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)

            if (self.unknown_0x04 & 0x10000000) > 0 and (0x01105070 < version < 0x02000000):
                self.unknown_0x10_P5R = rw.rw_float32(self.unknown_0x10_P5R)
                self.unknown_0x14_P5R = rw.rw_float32(self.unknown_0x14_P5R)
                self.unknown_0x18_P5R = rw.rw_float32(self.unknown_0x18_P5R)
                self.unknown_0x1C_P5R = rw.rw_float32(self.unknown_0x1C_P5R)
                
                self.unknown_0x20_P5R = rw.rw_float32(self.unknown_0x20_P5R)
                self.unknown_0x24_P5R = rw.rw_float32(self.unknown_0x24_P5R)
                self.unknown_0x28_P5R = rw.rw_uint32(self.unknown_0x28_P5R)
                self.unknown_0x2C_P5R = rw.rw_float32(self.unknown_0x2C_P5R)
                self.unknown_0x30_P5R = rw.rw_float32(self.unknown_0x30_P5R)
            if version > 0x02110031:
                self.unknown_0x10_MR = rw.rw_float32(self.unknown_0x10_MR)
                self.unknown_0x14_MR = rw.rw_uint32(self.unknown_0x14_MR)
                self.unknown_0x18_MR = rw.rw_float32s(self.unknown_0x18_MR, 2)
                self.unknown_0x20_MR = rw.rw_float32s(self.unknown_0x20_MR, 2)
                self.unknown_0x28_MR = rw.rw_float32(self.unknown_0x28_MR)
                self.unknown_0x2C_MR = rw.rw_uint32(self.unknown_0x2C_MR)

        if self.type == 1:
            ModelType = EPLModel3DData
        elif self.type == 2:
            ModelType = EPLModel2DData
            
        self.model = rw.rw_dynamic_obj(self.model, ModelType, version)
        self.has_embedded_file = rw.rw_uint8(self.has_embedded_file)
        if self.has_embedded_file:
            rw.rw_obj(self.embedded_file, version)


class EPLModel3DData:
    def __init__(self):
        pass
    
    def exbip_rw(self, rw, version):
        pass
    

class EPLModel2DData:
    def __init__(self):
        self.unknown_0x00 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
