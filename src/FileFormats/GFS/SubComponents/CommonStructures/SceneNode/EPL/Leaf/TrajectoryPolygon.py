from ........serialization.Serializable import Serializable
from .....CommonStructures import ObjectName
from .Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafTrajectoryPolygon(Serializable):
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
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        self.unknown_0x28 = EPLLeafCommonData2(endianness)
        self.unknown_0x2C = EPLLeafCommonData2(endianness)
        self.unknown_0x30 = EPLLeafCommonData(endianness)
        
        self.particle_emitter = ParticleEmitter(endianness)
        self.has_embedded_file = None
        self.embedded_file = EPLEmbeddedFile(endianness)

    def read_write(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        if version < 0x01104170:
            self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)

        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_uint32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        if version > 0x01104170:
            self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        rw.rw_obj(self.unknown_0x28, version)
        rw.rw_obj(self.unknown_0x2C, version)
        
        rw.rw_obj(self.unknown_0x30, version)
        rw.rw_obj(self.particle_emitter, version, self.type)
        self.has_embedded_file = rw.rw_uint8(self.has_embedded_file)
        if self.has_embedded_file:
            rw.rw_obj(self.embedded_file, version)


class EPLLeafTrajectoryPolygon2(EPLLeafTrajectoryPolygon):
    pass
