from ....ObjectNameModule import ObjectName
from ..Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafLight:
    def __init__(self):
        self.type = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        
        self.light_params = None
        self.has_embedded_file = None
        self.embedded_file = EPLEmbeddedFile()

    def exbip_rw(self, rw, version):
        self.type         = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        
        if self.type == 1:
            LightType = EplLightMeshData
        elif self.type == 2:
            LightType = EplLightSceneData
        elif self.type == 3:
            LightType = EplLightPointData
        elif self.type == 4:
            LightType = EplLightSpotData
        else:
            raise NotImplementedError(f"Unknown Light type '{self.type}'")
        self.light_params = rw.rw_dynamic_obj(self.light_params, LightType, version)
        self.has_embedded_file = rw.rw_uint8(self.has_embedded_file)
        if self.has_embedded_file:
            rw.rw_obj(self.embedded_file, version)


class EplLightMeshData:
    def __init__(self):
        pass

    def exbip_rw(self, rw, version):
        pass


class EplLightSceneData:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_uint32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_uint32(self.unknown_0x14)
        
        if version > 0x01104910:
            self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
            self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
            self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)


class EplLightPointData:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x0C = EPLLeafCommonData2()
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        rw.rw_obj(self.unknown_0x0C, version)
        
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)


class EplLightSpotData:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x0C = EPLLeafCommonData2()
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        rw.rw_obj(self.unknown_0x0C, version)
        
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
