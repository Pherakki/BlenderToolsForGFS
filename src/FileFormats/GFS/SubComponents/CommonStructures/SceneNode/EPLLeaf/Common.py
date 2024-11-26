from ....CommonStructures.ObjectNameModule import ObjectName


class EPLEmbeddedFile:
    def __init__(self):
        self.name = ObjectName()
        self.embed_type   = None  # 1: File inside exe, 2: embedded subfile
        self.unknown_0x06 = None
        self.filetype     = None
        self.payload_size = None
        self.payload      = None
        
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.name, version)
        if version < 0x02000002:
            self.embed_type = rw.rw_uint32(self.embed_type)
        else:
            self.embed_type   = rw.rw_uint16(self.embed_type)
            self.unknown_0x06 = rw.rw_uint16(self.unknown_0x06)
            
        if self.embed_type == 2:
            self.filetype     = rw.rw_uint32(self.filetype)
            self.payload_size = rw.rw_uint32(self.payload_size)
            self.payload      = rw.rw_bytestring(self.payload, self.payload_size)


class EPLLeafCommonData:
    def __init__(self):
        self.type = None
        self.payload = None
        self.unknown_0x14 = None
        self.unknown_0x24 = None
        
    def exbip_rw(self, rw, version):
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
    
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 4) # Value keyframes
        self.unknown_0x24 = rw.rw_bytestring(self.unknown_0x24, 0x2E) # timeshift


class EPLLeafCommonData2:
    def __init__(self):
        self.type = None
        self.payload = None
        self.unknown_0x14 = None
        self.unknown_0x24 = None
        self.unknown_0x52 = 0
        
    def exbip_rw(self, rw, version):
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

        if version > 0x02110186:
            self.unknown_0x52 = rw.rw_uint16(self.unknown_0x52)

class ParticleEmitter:
    def __init__(self):
        self.unknown_0x00 = None # randomSpawnDelay
        self.unknown_0x04 = None # particleLifetime
        self.unknown_0x08 = None # angleSeed
        self.unknown_0x0C = None # despawnTimer
        self.unknown_0x10 = None # SpawnChoker
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None # colorOverLifeOffset
        self.unknown_0x2C = None # drawQueueIndex
        self.unknown_0x30 = None # OpacityOverLife
        self.unknown_0x38 = EPLLeafCommonData2()
        self.unknown_0x3C = None
        self.unknown_0x40 = None
        self.unknown_0x44 = None
        self.unknown_0x48 = None
        self.unknown_0x50 = None
        self.unknown_0x54 = EPLLeafCommonData()
        self.unknown_0x58 = None
        self.unknown_0x5C = None
        self.unknown_0x60 = None
        self.unknown_0x64 = None
        self.unknown_0x68 = None
        self.unknown_0x6C = None
        self.unknown_0x70 = None
        self.unknown_0x74 = None
        
        self.payload = None
        
    def exbip_rw(self, rw, version, ptype):
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        if version > 0x02107001:
            self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        if version > 0x02110193:
            self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_uint32(self.unknown_0x2C)
        self.unknown_0x30 = rw.rw_float32s(self.unknown_0x30, 2)
        if version > 0x01104040:
            rw.rw_obj(self.unknown_0x38, version)
        if version > 0x01104700:
            self.unknown_0x3C = rw.rw_float32(self.unknown_0x3C)
        if version > 0x01104040:
            self.unknown_0x40 = rw.rw_dynamic_obj(self.unknown_0x40, EPLLeafCommonData2, version)
        else:
            self.unknown_0x40 = rw.rw_dynamic_obj(self.unknown_0x40, EPLLeafCommonData, version)
        
        self.unknown_0x44 = rw.rw_float32(self.unknown_0x44)
        self.unknown_0x48 = rw.rw_float32(self.unknown_0x48)
        if version > 0x02107000:
            self.unknown_0x50 = rw.rw_float32s(self.unknown_0x50, 2)
        
        if version > 0x01104040:
            self.unknown_0x58 = rw.rw_float32s(self.unknown_0x58, 2) # spawner angles
            self.unknown_0x5C = rw.rw_float32s(self.unknown_0x5C, 2) # cycle rate from birth
        else:
            self.unknown_0x54 = rw.rw_obj(self.unknown_0x54, version) # spawner angle and cycle rate
            
        self.unknown_0x60 = rw.rw_float32(self.unknown_0x60) # CycleRateGlobal
        self.unknown_0x64 = rw.rw_uint32(self.unknown_0x64)
        
        if version > 0x1104170:
            self.unknown_0x68 = rw.rw_uint32(self.unknown_0x68) # particleMultiplier
            self.unknown_0x6C = rw.rw_float32(self.unknown_0x6C)
        
        if version > 0x1104050:
            self.unknown_0x70 = rw.rw_float32(self.unknown_0x70) # particleScale
            self.unknown_0x74 = rw.rw_float32(self.unknown_0x74) # particleSpeed
        
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
            
        self.payload = rw.rw_dynamic_obj(self.payload, ParticleType, version)


class EplSmokeEffectParams:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x24 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)
        self.unknown_0x24 = rw.rw_float32s(self.unknown_0x24, 2)


class EPLExplosionEffectParams:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 2)
        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)


class EPLSpiralEffectParams:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x28 = rw.rw_float32s(self.unknown_0x28, 2)


class EPLBallEffectParams:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 2)
        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 2)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)


class EPLCircleEffectParams:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x08 = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x28 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 2)
        self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 2)
        self.unknown_0x28 = rw.rw_float32s(self.unknown_0x28, 2)


class EPLStraightLineEffectParams:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
        self.unknown_0x1C = None
        self.unknown_0x24 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)
        self.unknown_0x1C = rw.rw_float32s(self.unknown_0x1C, 2)
        self.unknown_0x24 = rw.rw_float32s(self.unknown_0x24, 2)
