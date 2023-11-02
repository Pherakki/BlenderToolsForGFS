from .......serialization.Serializable import Serializable
from ....CommonStructures import ObjectName


class EPLEmbeddedFile(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name = ObjectName()
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.payload_size = None
        self.payload      = None
        
    def read_write(self, rw, version):
        rw.rw_obj(self.name, version)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        if self.unknown_0x04 == 2:
            self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)
            self.payload_size = rw.rw_uint32(self.payload_size)
            self.payload      = rw.rw_bytestring(self.payload, self.payload_size)


class EPLLeafCommonData(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.payload = None
        self.unknown_0x14 = None
        self.unknown_0x24 = None
        
    def read_write(self, rw, version):
        self.type = rw.rw_uint16(self.type)
        if self.type == 0:
            self.payload = rw.rw_int32s(self.payload, 2)
        elif self.type == 1:
            self.payload = rw.rw_float32s(self.payload, 2)
        elif self.type == 2:
            self.payload = rw.rw_uint32s(self.payload, 2)
        elif self.type == 3:
            self.payload = rw.rw_float32s(self.payload, 4)
        else:
            raise NotImplementedError(f"Unknown EPLLeafCommonData type: '{self.type}'")
    
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 4)
        self.unknown_0x24 = rw.rw_bytestring(self.unknown_0x24, 0x2E)


class EPLLeafCommonData2(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.payload = None
        self.unknown_0x14 = None
        self.unknown_0x24 = None
        
    def read_write(self, rw, version):
        self.type = rw.rw_uint16(self.type)
        if self.type == 0:
            self.payload = rw.rw_int32s(self.payload, 4)
        elif self.type == 1:
            self.payload = rw.rw_float32s(self.payload, 4)
        elif self.type == 2:
            self.payload = rw.rw_uint32s(self.payload, 4)
        elif self.type == 3:
            self.payload = rw.rw_float32s(self.payload, 8)
        else:
            raise NotImplementedError(f"Unknown EPLLeafCommonData type: '{self.type}'")
    
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 4)
        self.unknown_0x24 = rw.rw_bytestring(self.unknown_0x24, 0x2E)


class ParticleEmitter(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        
        self.unknown_0x28 = EPLLeafCommonData2(endianness)
        self.unknown_0x2C = None
        self.unknown_0x30 = None
        
        self.unknown_0x34 = None
        self.unknown_0x38 = None
        self.unknown_0x40 = None
        self.unknown_0x48 = None
        self.unknown_0x50 = None
        self.unknown_0x54 = None
        self.unknown_0x58 = None
        self.unknown_0x5C = None
        self.unknown_0x60 = None
        self.unknown_0x64 = None
        
        self.payload = None
        
    def read_write(self, rw, version, ptype):
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_uint32(self.unknown_0x1C)
        
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        
        if version >= 0x01104041:
            rw.rw_obj(self.unknown_0x28, version)
        if version >= 0x01104701:
            self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
        if version >= 0x01104041:
            CommonType = EPLLeafCommonData2
        else:
            CommonType = EPLLeafCommonData
            
        self.unknown_0x30 = rw.rw_new_obj(self.unknown_0x30, lambda: CommonType(self.context.endianness), version)
        
        self.unknown_0x34 = rw.rw_float32(self.unknown_0x34)
        self.unknown_0x38 = rw.rw_float32(self.unknown_0x38)
        self.unknown_0x40 = rw.rw_float32s(self.unknown_0x40, 2)
        self.unknown_0x48 = rw.rw_float32s(self.unknown_0x48, 2)
        self.unknown_0x50 = rw.rw_float32(self.unknown_0x50)
        self.unknown_0x54 = rw.rw_uint32(self.unknown_0x54)
        self.unknown_0x58 = rw.rw_uint32(self.unknown_0x58)
        self.unknown_0x5C = rw.rw_float32(self.unknown_0x5C)
        self.unknown_0x60 = rw.rw_float32(self.unknown_0x60)
        self.unknown_0x64 = rw.rw_float32(self.unknown_0x64)
        
        if ptype == 1:
            ParticleType = EplSmokeEffectParams
        elif ptype == 2:
            ParticleType = EPLExplosionEffectParams
        elif ptype == 3:
            ParticleType = EPLSpiralEffectParams
        elif ptype == 4:
            ParticleType = EPLBallEffectParams
        elif ptype == 5:
            ParticleType = EPLCircleEffectParams
        elif ptype == 6:
            ParticleType = EPLStraightLineEffectParams
        else:
            raise NotImplementedError(f"Unknown ParticleEmitter type: '{self.type}'")
            
        self.payload = rw.rw_new_obj(self.payload, lambda: ParticleType(self.context.endianness), version)


class EplSmokeEffectParams(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x24 = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)
        self.unknown_0x24 = rw.rw_float32s(self.unknown_0x24, 2)


class EPLExplosionEffectParams(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 2)
        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)


class EPLSpiralEffectParams(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x28 = rw.rw_float32s(self.unknown_0x28, 2)


class EPLBallEffectParams(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 2)
        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)


class EPLCircleEffectParams(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 2)
        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x28 = rw.rw_float32s(self.unknown_0x28, 2)


class EPLStraightLineEffectParams(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x24 = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)
        self.unknown_0x24 = rw.rw_float32s(self.unknown_0x24, 2)
