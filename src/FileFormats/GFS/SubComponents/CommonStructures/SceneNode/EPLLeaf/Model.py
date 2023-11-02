from .......serialization.Serializable import Serializable
from ....CommonStructures import ObjectName
from .Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafModel(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness

        self.type = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        
        
        self.model = None
        self.has_embedded_file = None
        self.embedded_file = EPLEmbeddedFile(endianness)


    def read_write(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        if version > 0x1104050:
            self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
            self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)

        if self.type == 1:
            ModelType = EPLModel3DData
        elif self.type == 2:
            ModelType = EPLModel2DData
            
        self.model = rw.rw_new_obj(self.model, lambda: ModelType(self.context.endianness), version)
        self.has_embedded_file = rw.rw_uint8(self.has_embedded_file)
        if self.has_embedded_file:
            rw.rw_obj(self.embedded_file, version)


class EPLModel3DData(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
    def read_write(self, rw, version):
        pass
    

class EPLModel2DData(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
