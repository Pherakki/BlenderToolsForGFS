from ....ObjectNameModule import ObjectName
from ..Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafCamera:
    def __init__(self):
        self.type = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        
        self.camera_params = None
        self.has_embedded_file = None
        self.embedded_file = EPLEmbeddedFile()

    def exbip_rw(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_uint32(self.unknown_0x10)
        
        if self.type == 1:
            CameraType = EPLCameraMeshParams
        elif self.type == 2:
            CameraType = EPLCameraQuakeParams
        else:
            raise NotImplementedError(f"Unknown Camera type '{self.type}'")
        
        self.camera_params = rw.rw_dynamic_obj(self.camera_params, CameraType, version)
        self.has_embedded_file = rw.rw_uint8(self.has_embedded_file)
        if self.has_embedded_file:
            rw.rw_obj(self.embedded_file, version)


class EPLCameraMeshParams:
    def __init__(self):
        pass
    
    def exbip_rw(self, rw, version):
        pass


class EPLCameraQuakeParams:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
