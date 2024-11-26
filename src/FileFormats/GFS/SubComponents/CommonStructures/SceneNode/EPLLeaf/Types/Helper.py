from ....ObjectNameModule import ObjectName
from ..Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafHelper:
    def __init__(self):
        self.type = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        
        
        self.has_embedded_file_1 = None
        self.embedded_file_1 = EPLEmbeddedFile()
        self.has_embedded_file_2 = None
        self.embedded_file_2 = EPLEmbeddedFile()

    def exbip_rw(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        
        self.has_embedded_file_1 = rw.rw_uint8(self.has_embedded_file_1)
        if self.has_embedded_file_1:
            rw.rw_obj(self.embedded_file_1, version)
        self.has_embedded_file_2 = rw.rw_uint8(self.has_embedded_file_2)
        if self.has_embedded_file_2:
            rw.rw_obj(self.embedded_file_2, version)
