from ....ObjectNameModule import ObjectName
from ..Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafPostEffect:
    def __init__(self):
        self.type         = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        
        self.post_effect = None
        self.has_embedded_file = None
        self.embedded_file = EPLEmbeddedFile()

    def exbip_rw(self, rw, version):
        self.type         = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        
        if self.type == 1:
            PostEffectType = EplPostEffectRadiationBlurData
        elif self.type == 2:
            PostEffectType = EplPostEffectStraightBlurData
        elif self.type == 3:
            PostEffectType = EplPostEffectNoiseBlurData
        elif self.type == 4:
            PostEffectType = EplPostEffectDistortionBlurData
        elif self.type == 5:
            PostEffectType = EplPostEffectFillData
        elif self.type == 6:
            PostEffectType = EplPostEffectLensFlareData
        elif self.type == 7:
            PostEffectType = EplPostEffectColorCorrectionData
        elif self.type == 8:
            PostEffectType = EplPostEffectMonotoneData
        elif self.type == 9:
            if version >= 0x02000000:
                PostEffectType = EplPostEffectChromaticAberration
            else:
                PostEffectType = EplPostEffectLensFlareMake
        elif self.type == 10:
            if version >= 0x02000000:
                PostEffectType = EplPostEffectColorCorrectionExcludeToon
            else:
                PostEffectType = EplPostEffectMotionBlur
        elif self.type == 11:
            PostEffectType = EplPostEffectAfterImageBlur
        else:
            raise NotImplementedError(f"Unknown PostEffect type '{self.type}'")
        
        self.post_effect = rw.rw_dynamic_obj(self.post_effect, PostEffectType, version)
        self.has_embedded_file = rw.rw_uint8(self.has_embedded_file)
        if self.has_embedded_file:
            rw.rw_obj(self.embedded_file, version)


class EplPostEffectRadiationBlurData:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData2()
        self.unknown_0x04 = None
        self.unknown_0x08 = EPLLeafCommonData2()
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        rw.rw_obj(self.unknown_0x08, version)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        
        if version > 0x01104930:
            self.unknown_0x18 = rw.rw_uint8(self.unknown_0x18)


class EplPostEffectStraightBlurData:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData2()
        self.unknown_0x04 = None
        self.unknown_0x08 = EPLLeafCommonData2()
        self.unknown_0x0C = None
        
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        rw.rw_obj(self.unknown_0x08, version)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)


class EplPostEffectNoiseBlurData:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData2()
        self.unknown_0x04 = None
        self.unknown_0x08 = EPLLeafCommonData2()
        self.unknown_0x0C = EPLLeafCommonData2()
        self.unknown_0x10 = None
        
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        rw.rw_obj(self.unknown_0x08, version)
        rw.rw_obj(self.unknown_0x0C, version)
        if version > 0x01104920:
            self.unknown_0x10 = rw.rw_uint8(self.unknown_0x10)


class EplPostEffectDistortionBlurData:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData2()
        self.unknown_0x04 = None
        self.unknown_0x08 = EPLLeafCommonData2()
        self.unknown_0x0C = EPLLeafCommonData2()
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        rw.rw_obj(self.unknown_0x08, version)
        rw.rw_obj(self.unknown_0x0C, version)
        
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)


class EplPostEffectFillData:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData2()
        self.unknown_0x04 = EPLLeafCommonData2()
        self.unknown_0x08 = EPLLeafCommonData2()
        self.unknown_0x0C = EPLLeafCommonData2()
        self.unknown_0x10 = None
        
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.unknown_0x00, version)
        rw.rw_obj(self.unknown_0x04, version)
        rw.rw_obj(self.unknown_0x08, version)
        rw.rw_obj(self.unknown_0x0C, version)
        
        self.unknown_0x10 = rw.rw_uint32(self.unknown_0x10)


class EplPostEffectLensFlareData:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = EPLLeafCommonData2()
        self.unknown_0x10 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)
        rw.rw_obj(self.unknown_0x0C, version)
        
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)


class EplPostEffectColorCorrectionData:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 2)


class EplPostEffectMonotoneData:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32s(self.unknown_0x04, 2)


class EplPostEffectChromaticAberration:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x14 = None
    
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32s(self.unknown_0x0C, 2)
        self.unknown_0x14 = rw.rw_float32s(self.unknown_0x14, 2)


class EplPostEffectLensFlareMake:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = EPLLeafCommonData2()
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        self.unknown_0x30 = None
        self.unknown_0x34 = None
        self.unknown_0x38 = None
        self.unknown_0x3C = None
        self.unknown_0x40 = None
        self.unknown_0x44 = None
        self.unknown_0x48 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
        self.unknown_0x30 = rw.rw_float32(self.unknown_0x30)
        self.unknown_0x34 = rw.rw_float32(self.unknown_0x34)
        self.unknown_0x38 = rw.rw_float32(self.unknown_0x38)
        self.unknown_0x3C = rw.rw_float32(self.unknown_0x3C)
        self.unknown_0x40 = rw.rw_float32(self.unknown_0x40)
        self.unknown_0x44 = rw.rw_float32(self.unknown_0x44)
        self.unknown_0x48 = rw.rw_float32(self.unknown_0x48)


class EplPostEffectColorCorrectionExcludeToon:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
    
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32s(self.unknown_0x24, 2)


class EplPostEffectMotionBlur:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData2()
        self.unknown_0x04 = None
        self.unknown_0x08 = EPLLeafCommonData2()
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_obj(self.unknown_0x08, version)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)


class EplPostEffectAfterImageBlur:
    def __init__(self):
        self.unknown_0x00 = EPLLeafCommonData2()
        self.unknown_0x04 = None
        self.unknown_0x08 = EPLLeafCommonData2()
        self.unknown_0x0C = None
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_obj(self.unknown_0x00, version)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_obj(self.unknown_0x08, version)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
