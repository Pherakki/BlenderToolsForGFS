from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format


class MaterialAnimationType:
    NODE_TR               = 1
    NODE_TRS              = 2
    MATERIAL_AMBIENT_RGB  = 6
    MATERIAL_DIFFUSE_RGB  = 7
    MATERIAL_SPECULAR_RGB = 8
    MATERIAL_OPACITY      = 12
    MATERIAL_TEX0_UVS     = 13
    MATERIAL_EMISSION_RGB = 14


class AnimationTrackBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.keyframe_type = None
        self.keyframe_count = None
        
        self.frames = []
        self.values = []
        
        self.base_position = [1., 1., 1.]
        self.base_scale    = [1., 1., 1.]
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track {safe_format(self.keyframe_type, hex32_format)}] Keyframes: {self.keyframe_count}"

    def read_write(self, rw, version):
        self.keyframe_type  = rw.rw_uint32(self.keyframe_type)
        self.keyframe_count = rw.rw_uint32(self.keyframe_count)
        
        self.frames = rw.rw_float32s(self.frames, self.keyframe_count)
        # Should use this to decide which "keyframe attributes" to r/w?
        # Need to figure out all kf attributes first since many overlap..?
        if self.keyframe_type == 1: # Node Anim: Only in extra data?
            kf_type = KeyframeType1
        elif self.keyframe_type == 2: # Node Anim: 0x01104970, 0x01105000, 0x01105010, 0x01105020, 0x01105030, 0x01105040, 0x01105060, 0x01105070, 0x01105080, 0x1105090, 0x1105100
            kf_type = KeyframeType2
        elif self.keyframe_type == 3: # Morph Anim: 0x01105060
            kf_type = KeyframeType3
        # elif self.keyframe_type == 4:
        #     kf_type = KeyframeType4
        elif self.keyframe_type == 5:
            kf_type = KeyframeType5
        elif self.keyframe_type == 6: # Material Anim: 0x01105040, 0x01105060, 0x01105070, 0x1105090, 0x01105100
            kf_type = AmbientRGB
        elif self.keyframe_type == 7: # Material Anim: 0x01105060, 0x01105070, 0x01105100
            kf_type = DiffuseRGB
        elif self.keyframe_type == 8: # Material Anim: 0x01105060, 0x01105070, 0x01105100
            kf_type = SpecularRGB
        elif self.keyframe_type == 9: # Material Anim: 0x01105060, 0x01105020, 0x01105100
            kf_type = KeyframeType9
        # elif self.keyframe_type == 10:
        #     kf_type = KeyframeType10
        elif self.keyframe_type == 11: # Material Anim: 0x01105040, 0x01105060, 0x01105070, 0x01105100
            kf_type = KeyframeType11
        elif self.keyframe_type == 12: # Material Anim: 0x01105000, 0x01105020, 0x01105030, 0x01105040, 0x01105060, 0x1105070, 0x01105080, 0x1105090, 0x1105100
            kf_type = Opacity
        elif self.keyframe_type == 13: # Material Anim: 0x01105020, 0x01105030, 0x01105040, 0x01105060, 0x01105070, 0x1105090, 0x01105100
            kf_type = Tex0UV
        elif self.keyframe_type == 14: # Material Anim: 0x01105020, 0x01105030, 0x01105040, 0x01105060, 0x01105070, 0x1105090, 0x01105100
            kf_type = EmissionRGB
        elif self.keyframe_type == 15: # Material Anim: 0x01105060, 0x01105070, 0x01105100
            kf_type = KeyframeType15
        elif self.keyframe_type == 16: # Node Anim: 0x01105060, 0x01105070
            kf_type = KeyframeType16
        # elif self.keyframe_type == 17:
        #     kf_type = KeyframeType17
        # elif self.keyframe_type == 18:
        #     kf_type = KeyframeType18
        # elif self.keyframe_type == 19:
        #     kf_type = KeyframeType19
        elif self.keyframe_type == 20: # Material Anim: 0x01105100
            kf_type = KeyframeType20
        elif self.keyframe_type == 21: # Material Anim: 0x01105020, 0x1105030, 0x01105040, 0x01105060, 0x01105070, 0x1105090, 0x01105100
            kf_type = KeyframeType21
        # elif self.keyframe_type == 22:
        #     kf_type = KeyframeType22
        elif self.keyframe_type == 23: # Camera Anim: 0x01105040, 0x01105060, 0x01105070, 0x01105100
            kf_type = KeyframeType23
        elif self.keyframe_type == 24: # Camera Anim: 0x01105060, 0x01105070
            kf_type = KeyframeType24
        elif self.keyframe_type == 25: # Material Anim: 0x01105070, 0x1105090, 0x01105100
            kf_type = KeyframeType25
        elif self.keyframe_type == 26:
            kf_type = KeyframeType26
        elif self.keyframe_type == 27: # Node Anim: 0x01104970, 0x01105000, 0x01105010, 0x01105020, 0x01105030, 0x01105040, 0x01105070, 0x01105080, 0x1105090, 0x01105100
            kf_type = KeyframeType27
        elif self.keyframe_type == 28: # Node Anim: 0x01104970, 0x01105000, 0x01105010, 0x01105020, 0x01105030, 0x01105040, 0x01105060, 0x01105070, 0x01105080, 0x1105090, 0x01105100
            kf_type = KeyframeType28
        elif self.keyframe_type == 29: # Material Anim: 0x01105030, 0x01105040, 0x01105060, 0x01105070, 0x01105080, 0x1105090, 0x01105100
            kf_type = KeyframeType29
        elif self.keyframe_type == 30: # Material Anim: 0x01105060, 0x1105070
            kf_type = KeyframeType30
        elif self.keyframe_type == 31:
            kf_type = KeyframeType31
        elif self.keyframe_type == 32:
            kf_type = KeyframeType32
        elif self.keyframe_type == 33:
            kf_type = KeyframeType33
        elif self.keyframe_type == 34:
            kf_type = KeyframeType34
        elif self.keyframe_type == 35:
            kf_type = KeyframeType35
        elif self.keyframe_type == 36: # Material Anim: 0x1105100
            kf_type = KeyframeType36
        else:
            raise NotImplementedError(f"Unknown Keyframe type: '{self.keyframe_type}'")
            
        self.values = rw.rw_obj_array(self.values, kf_type, self.keyframe_count)
        
        # Flag instead?!
        if self.keyframe_type in [26, 27, 28, 31, 32, 33, 34, 35]: # If has float16 pos...
            self.base_position = rw.rw_float32s(self.base_position, 3)
            self.base_scale = rw.rw_float32s(self.base_scale, 3)


class KeyframeType1(Serializable):
    """Node Keyframe"""
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 1
        
    def __init__(self, position=None, rotation=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = position
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType1] {self.position} {self.rotation}"
        
    def read_write(self, rw):
        self.position = rw.rw_float32s(self.position, 3)
        self.rotation = rw.rw_float32s(self.rotation, 4)

class KeyframeType2(Serializable):
    """Node Keyframe"""
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 2
    
    def __init__(self, position=None, rotation=None, scale=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = position
        self.rotation = rotation
        self.scale = scale
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType2] {self.position} {self.rotation} {self.scale}"
        
    def read_write(self, rw):
        self.position = rw.rw_float32s(self.position, 3)
        self.rotation = rw.rw_float32s(self.rotation, 4)
        self.scale    = rw.rw_float32s(self.scale, 3)

class KeyframeType3(Serializable):
    """Morph Keyframe"""
    
    OBJ_VARIANT_TYPE = 4
    VARIANT_TYPE = 3
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType3] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 3)
        
class KeyframeType4(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 4
    
    def __init__(self, rotation=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType4] {self.rotation}"
        
    def read_write(self, rw):
        self.rotation = rw.rw_float32s(self.unknown, 4)
        
class KeyframeType5(Serializable):
    OBJ_VARIANT_TYPE = 5
    VARIANT_TYPE = 5
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType5] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
        
class AmbientRGB(Serializable):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 6
    
    def __init__(self, r=0, g=0, b=0, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.r = r
        self.g = g
        self.b = b
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::AmbientRGB] {self.r} {self.g} {self.b}"
        
    def read_write(self, rw):
        self.r = rw.rw_float32(self.r)
        self.g = rw.rw_float32(self.g)
        self.b = rw.rw_float32(self.b)
        
class DiffuseRGB(Serializable):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 7
    
    def __init__(self, r=0, g=0, b=0, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.r = r
        self.g = g
        self.b = b
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::DiffuseRGB] {self.r} {self.g} {self.b}"
        
    def read_write(self, rw):
        self.r = rw.rw_float32(self.r)
        self.g = rw.rw_float32(self.g)
        self.b = rw.rw_float32(self.b)
        
class SpecularRGB(Serializable):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 8
    
    def __init__(self, r=0, g=0, b=0, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.r = r
        self.g = g
        self.b = b
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::SpecularRGB] {self.r} {self.g} {self.b}"
        
    def read_write(self, rw):
        self.r = rw.rw_float32(self.r)
        self.g = rw.rw_float32(self.g)
        self.b = rw.rw_float32(self.b)
                
class KeyframeType9(Serializable):
    """Material Keyframe"""
    
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 9
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType9] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
        
class KeyframeType10(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 10
    
    def __init__(self, rotation=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType10] {self.rotation}"
        
    def read_write(self, rw):
        self.rotation = rw.rw_float32s(self.unknown, 4)
                        
class KeyframeType11(Serializable):
    """Material Keyframe"""
    
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 11
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType11] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
        
class Opacity(Serializable):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 12
    
    def __init__(self, opacity=1, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.opacity = opacity
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType12] {self.unknown}"
        
    def read_write(self, rw):
        self.opacity = rw.rw_float32(self.opacity)
                
class Tex0UV(Serializable):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 13
    
    def __init__(self, translate_u=0, translate_v=0, scale_u=1, scale_v=1, rotation=0, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.translate_u = translate_u
        self.translate_v = translate_v
        self.scale_u = scale_u
        self.scale_v = scale_v
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::Tex0UV] {self.translate_u} {self.translate_v} {self.scale_x} {self.scale_y} {self.rotation}"
        
    def read_write(self, rw):
        self.translate_u = rw.rw_float32(self.translate_u)
        self.translate_v = rw.rw_float32(self.translate_v)
        self.scale_u     = rw.rw_float32(self.scale_u)
        self.scale_v     = rw.rw_float32(self.scale_v)
        self.rotation    = rw.rw_float32(self.rotation)

class EmissionRGB(Serializable):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 14
    
    def __init__(self, r=0, g=0, b=0, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.r = r
        self.g = g
        self.b = b
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::EmissionRGB] {self.r} {self.g} {self.b}"
        
    def read_write(self, rw):
        self.r = rw.rw_float32(self.r)
        self.g = rw.rw_float32(self.g)
        self.b = rw.rw_float32(self.b)
                
class KeyframeType15(Serializable):
    """Material Keyframe"""
    
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 15
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType15] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
                
class KeyframeType16(Serializable):
    """Node Keyframe"""
    
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 16
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType16] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)

class KeyframeType17(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 17
    
    def __init__(self, position=None, rotation=None, scale=None, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType17] {self.position} {self.rotation} {self.scale} {self.unknown}"
        
    def read_write(self, rw):
        self.position = rw.rw_float32s(self.position, 3)
        self.rotation = rw.rw_float32s(self.rotation, 4)
        self.scale    = rw.rw_float32s(self.scale, 3)
        self.unknown  = rw.rw_uint8(self.unknown)

class KeyframeType18(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 18
    
    def __init__(self, rotation=None, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.rotation  = rotation
        self.unknown_2 = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType18] {self.rotation} {self.unknown_2}"
        
    def read_write(self, rw):
        self.rotation  = rw.rw_float32s(self.rotation, 4)
        self.unknown_2 = rw.rw_uint8(self.unknown_2)

class KeyframeType19(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 19
    
    def __init__(self, unknown_1=None, unknown_2=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_1 = unknown_1
        self.unknown_2 = unknown_2
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType19] {self.unknown_1} {self.unknown_2}"
        
    def read_write(self, rw):
        self.unknown_1 = rw.rw_float32(self.unknown_1)
        self.unknown_2  = rw.rw_uint8(self.unknown_2)
                
class KeyframeType20(Serializable):
    """Material Keyframe"""
    
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 20
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType20] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 5)
                
class KeyframeType21(Serializable):
    """Material Keyframe"""
    
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 21
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType21] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 5)
                
class KeyframeType22(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 22
    
    def __init__(self, unknown_0x00=None, unknown_0x04=None, unknown_0x08=None,
                 unknown_0x0A=None, unknown_0x0E=None, unknown_0x12=None,
                 unknown_0x16=None, unknown_0x1A=None, unknown_0x1C=None,
                 unknown_0x20=None, unknown_0x24=None, unknown_0x28=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = unknown_0x00
        self.unknown_0x04 = unknown_0x04
        self.unknown_0x08 = unknown_0x08
        self.unknown_0x0A = unknown_0x0A
        self.unknown_0x0E = unknown_0x0E
        self.unknown_0x12 = unknown_0x12
        self.unknown_0x16 = unknown_0x16
        self.unknown_0x1A = unknown_0x1A
        self.unknown_0x1C = unknown_0x1C
        self.unknown_0x20 = unknown_0x20
        self.unknown_0x24 = unknown_0x24
        self.unknown_0x28 = unknown_0x28
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType22] {self.unknown_0x00}"
        
    def read_write(self, rw):
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_uint16(self.unknown_0x08)
        self.unknown_0x0A = rw.rw_float32(self.unknown_0x0A)
        self.unknown_0x0E = rw.rw_float32(self.unknown_0x0E)
        self.unknown_0x12 = rw.rw_float32(self.unknown_0x12)
        self.unknown_0x16 = rw.rw_uint32(self.unknown_0x16)
        self.unknown_0x1A = rw.rw_uint16(self.unknown_0x1A)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_uint8(self.unknown_0x28)

class KeyframeType23(Serializable):
    """Camera Keyframe"""
    OBJ_VARIANT_TYPE = 3
    VARIANT_TYPE = 23
    
    def __init__(self, fov=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.camera_fov = fov
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType23] {self.camera_fov}"
    
    def read_write(self, rw):
        self.camera_fov = rw.rw_float32(self.camera_fov)

class KeyframeType24(Serializable):
    """Camera Keyframe"""
    OBJ_VARIANT_TYPE = 3
    VARIANT_TYPE = 24
    
    def __init__(self, unknown_float=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_float = unknown_float
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType24] {self.unknown_float}"
    
    def read_write(self, rw):
        self.unknown_float = rw.rw_float32(self.unknown_float)
        
class KeyframeType25(Serializable):
    """Material Keyframe"""
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 25
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_float = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType25] {self.unknown_float}"
    
    def read_write(self, rw):
        self.unknown_float = rw.rw_float32(self.unknown_float)
        
class KeyframeType26(Serializable): # What is different about this one and 28?!
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 26
    
    def __init__(self, position=None, rotation=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = position
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType26] {self.position} {self.rotation}"
        
    def read_write(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.rotation = rw.rw_float16s(self.rotation, 4)
        
class KeyframeType27(Serializable):
    """Node Keyframe"""
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 27
    
    def __init__(self, position=None, rotation=None, scale=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = position
        self.rotation = rotation
        self.scale = scale
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType27] {self.position} {self.rotation} {self.scale}"
        
    def read_write(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.rotation = rw.rw_float16s(self.rotation, 4)
        self.scale    = rw.rw_float16s(self.scale, 3)
        
class KeyframeType28(Serializable):
    """Node Keyframe"""
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 28
    
    def __init__(self, position=None, rotation=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = position
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType28] {self.position} {self.rotation}"
        
    def read_write(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.rotation = rw.rw_float16s(self.rotation, 4)
        
class KeyframeType29(Serializable):
    """Material Keyframe"""
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 29
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType29] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
                  
class KeyframeType30(Serializable):
    """Material Keyframe"""
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 30
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_float = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType30] {self.unknown_float}"
    
    def read_write(self, rw):
        self.unknown_float = rw.rw_float32(self.unknown_float)
        
class KeyframeType31(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 31
    
    def __init__(self, position=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = position
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType31] {self.position}"
        
    def read_write(self, rw):
        self.position = rw.rw_float16s(self.position, 3)

           
class KeyframeType32(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 32
    
    def __init__(self, rotation=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType32] {self.rotation}"
        
    def read_write(self, rw):
        self.rotation = rw.rw_float16s(self.rotation, 4)

         
class KeyframeType33(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 33
    
    def __init__(self, scale=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.scale = scale
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType33] {self.scale}"
        
    def read_write(self, rw):
        self.scale = rw.rw_float16s(self.scale, 3)

             
class KeyframeType34(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 34
    
    def __init__(self, position=None, scale=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = position
        self.scale = scale
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType34] {self.position} {self.scale}"
        
    def read_write(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.scale = rw.rw_float16s(self.scale, 3)
        
class KeyframeType35(Serializable):
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 35
    
    def __init__(self, rotation=None, scale=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.rotation = rotation
        self.scale = scale
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType35] {self.rotation} {self.scale}"
        
    def read_write(self, rw):
        self.rotation = rw.rw_float16s(self.rotation, 4)
        self.scale = rw.rw_float16s(self.scale, 3)
        
class KeyframeType36(Serializable):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 36
    
    def __init__(self, unknown=None, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType36] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 5)
    