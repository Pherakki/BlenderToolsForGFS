import copy
from ......serialization.formatters import HEX32_formatter


class MaterialAnimationType:
    NODE_TR               = 1
    NODE_TRS              = 2
    MATERIAL_AMBIENT_RGB  = 6
    MATERIAL_DIFFUSE_RGB  = 7
    MATERIAL_SPECULAR_RGB = 8
    MATERIAL_OPACITY      = 12
    MATERIAL_TEX0_UVS     = 13
    MATERIAL_EMISSION_RGB = 14


class AnimationTrackBinary:
    def __init__(self):
        self.keyframe_type = None
        self.keyframe_count = None
        
        self.frames = []
        self.values = []
        
        self.base_position = [1., 1., 1.]
        self.base_scale    = [1., 1., 1.]
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track {HEX32_formatter(self.keyframe_type)}] Keyframes: {self.keyframe_count}"

    def exbip_rw(self, rw, version):
        self.keyframe_type  = rw.rw_uint32(self.keyframe_type)
        self.keyframe_count = rw.rw_uint32(self.keyframe_count)
        
        self.frames = rw.rw_float32s(self.frames, self.keyframe_count)
        
        if version >= 0x02000000:
            kf_type = KEYFRAME_TYPES_V2[self.keyframe_type]
        else:
            kf_type = KEYFRAME_TYPES_V1[self.keyframe_type]
        
        try:
            self.values = rw.rw_dynamic_objs(self.values, kf_type, self.keyframe_count)
        except Exception as e:
            raise e
        
        if version >= 0x02000000:
            if self.keyframe_type in [26, 27, 28, 32]:
                self.base_position = rw.rw_float32s(self.base_position, 3)
            if self.keyframe_type in [26, 27, 28, 31, 32]:
                self.base_scale = rw.rw_float32s(self.base_scale, 3)
        else:
            if self.keyframe_type in [26, 27, 28, 31, 32, 33, 34, 35]: # If has float16 pos...
                self.base_position = rw.rw_float32s(self.base_position, 3)
                self.base_scale = rw.rw_float32s(self.base_scale, 3)


################
# BASE CLASSES #
################          
class TexUVKeyframe:
    def __init__(self, transforms=None):
        if transforms is None:
            self.translate_u = 0.
            self.translate_v = 0.
            self.scale_u     = 1.
            self.scale_v     = 1.
            self.rotation    = 0.
        else:
            self.translate_u, \
            self.translate_v, \
            self.scale_u,     \
            self.scale_v,     \
            self.rotation = transforms
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::{self.CLASSNAME}] {self.translate_u} {self.translate_v} {self.scale_x} {self.scale_y} {self.rotation}"
        
    def exbip_rw(self, rw):
        self.translate_u = rw.rw_float32(self.translate_u)
        self.translate_v = rw.rw_float32(self.translate_v)
        self.scale_u     = rw.rw_float32(self.scale_u)
        self.scale_v     = rw.rw_float32(self.scale_v)
        self.rotation    = rw.rw_float32(self.rotation)
    
    def size(self):
        return 20


class ColorKeyframe:
    def __init__(self, color=None):
        if color is None:
            self.r = 1.
            self.g = 1.
            self.b = 1.
        else:
            self.r, \
            self.g, \
            self.b = color
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::{self.CLASSNAME}] {self.r} {self.g} {self.b}"
        
    def exbip_rw(self, rw):
        self.r = rw.rw_float32(self.r)
        self.g = rw.rw_float32(self.g)
        self.b = rw.rw_float32(self.b)
    
    def size(self):
        return 12


class NodeTR:
    """Node Keyframe"""
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 1
        
    def __init__(self, position=None, rotation=None):
        self.position = position
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType1] {self.position} {self.rotation}"
        
    def exbip_rw(self, rw):
        self.position = rw.rw_float32s(self.position, 3)
        self.rotation = rw.rw_float32s(self.rotation, 4)
    
    def size(self):
        return 28


class NodeTRS:
    """Node Keyframe"""
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 2
    
    def __init__(self, position=None, rotation=None, scale=None):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType2] {self.position} {self.rotation} {self.scale}"
        
    def exbip_rw(self, rw):
        self.position = rw.rw_float32s(self.position, 3)
        self.rotation = rw.rw_float32s(self.rotation, 4)
        self.scale    = rw.rw_float32s(self.scale, 3)
    
    def size(self):
        return 40


class KeyframeType3:
    """Morph Keyframe"""
    
    OBJ_VARIANT_TYPE = 4
    VARIANT_TYPE = 3
    
    def __init__(self, unknown=None):
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType3] {self.unknown}"
        
    def exbip_rw(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 3)

    def size(self):
        return 12


class KeyframeType4:
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 4
    
    def __init__(self, rotation=None):
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType4] {self.rotation}"
        
    def exbip_rw(self, rw):
        self.rotation = rw.rw_float32s(self.unknown, 4)

    def size(self):
        return 16


class KeyframeType5:
    OBJ_VARIANT_TYPE = 5
    VARIANT_TYPE = 5
    
    def __init__(self, unknown=None):
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType5] {self.unknown}"
        
    def exbip_rw(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
    
    def size(self):
        return 4


class AmbientRGB(ColorKeyframe):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 6
    CLASSNAME = "AmbientRGB"
        
class DiffuseRGB(ColorKeyframe):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 7
    CLASSNAME = "DiffuseRGB"
        
class SpecularRGB(ColorKeyframe):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 8
    CLASSNAME = "SpecularRGB"
                
class SpecularPower:
    """Material Keyframe"""
    
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 9
    
    def __init__(self, unknown=None):
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType9] {self.unknown}"
        
    def exbip_rw(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
    
    def size(self):
        return 4


class KeyframeType10:
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 10
    
    def __init__(self, rotation=None):
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType10] {self.rotation}"
        
    def exbip_rw(self, rw):
        self.rotation = rw.rw_float32s(self.unknown, 4)
    
    def size(self):
        return 16


class KeyframeType11:
    """Material Keyframe"""
    
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 11
    
    def __init__(self, unknown=None):
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType11] {self.unknown}"
        
    def exbip_rw(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
    
    def size(self):
        return 4

        
class Opacity:
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 12
    
    def __init__(self, opacity=1):
        self.opacity = opacity
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::MaterialOpacity] {self.opacity}"
        
    def exbip_rw(self, rw):
        self.opacity = rw.rw_float32(self.opacity)
    
    def size(self):
        return 4

                
class Tex0UV(TexUVKeyframe):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 13
    CLASSNAME = "Tex0UV"

class EmissiveRGB(ColorKeyframe):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 14
    CLASSNAME = "EmissiveRGB"
                
class KeyframeType15:
    """Material Keyframe"""
    
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 15
    
    def __init__(self, unknown=None):
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType15] {self.unknown}"
        
    def exbip_rw(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
    
    def size(self):
        return 4

                
class KeyframeType16:
    """Node Keyframe"""
    
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 16
    
    def __init__(self, unknown=None):
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType16] {self.unknown}"
        
    def exbip_rw(self, rw):
        self.unknown = rw.rw_float32(self.unknown)

    def size(self):
        return 4


class KeyframeType17:
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 17
    
    def __init__(self, position=None, rotation=None, scale=None, unknown=None):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType17] {self.position} {self.rotation} {self.scale} {self.unknown}"
        
    def exbip_rw(self, rw):
        self.position = rw.rw_float32s(self.position, 3)
        self.rotation = rw.rw_float32s(self.rotation, 4)
        self.scale    = rw.rw_float32s(self.scale, 3)
        self.unknown  = rw.rw_uint8(self.unknown)

    def size(self):
        return 41


class KeyframeType18:
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 18
    
    def __init__(self, unknown_0x00=None, unknown_0x04=None, unknown_0x08=None, unknown_0x0C=None):
        self.unknown_0x00 = unknown_0x00
        self.unknown_0x04 = unknown_0x04
        self.unknown_0x08 = unknown_0x08
        self.unknown_0x0C = unknown_0x0C
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType18] {self.unknown_0x00} {self.unknown_0x04} {self.unknown_0x08} {self.unknown_0x0C}"
        
    def exbip_rw(self, rw):
        self.unknown_0x00  = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04  = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08  = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C  = rw.rw_uint8(self.unknown_0x0C)
    
    def size(self):
        return 13


class KeyframeType19:
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 19
    
    def __init__(self, unknown_1=None, unknown_2=None):
        self.unknown_1 = unknown_1
        self.unknown_2 = unknown_2
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType19] {self.unknown_1} {self.unknown_2}"
        
    def exbip_rw(self, rw):
        self.unknown_1 = rw.rw_float32(self.unknown_1)
        self.unknown_2  = rw.rw_uint8(self.unknown_2)
    
    def size(self):
        return 5


class Tex1UV(TexUVKeyframe):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 20
    CLASSNAME = "Tex1UV"
    
class Tex0UVSnap(TexUVKeyframe):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 21
    CLASSNAME = "Tex0UVSnap"
                
class KeyframeType22:
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 22
    
    def __init__(self, unknown_0x00=None, unknown_0x04=None, unknown_0x08=None,
                 unknown_0x0A=None, unknown_0x0E=None, unknown_0x12=None,
                 unknown_0x16=None, unknown_0x1A=None, unknown_0x1C=None,
                 unknown_0x20=None, unknown_0x24=None, unknown_0x28=None):
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
        
    def exbip_rw(self, rw):
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
    
    def size(self):
        return 29


class CameraFOV:
    """Camera Keyframe"""
    OBJ_VARIANT_TYPE = 3
    VARIANT_TYPE = 23
    
    def __init__(self, fov=None):
        self.camera_fov = fov
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType23] {self.camera_fov}"
    
    def exbip_rw(self, rw):
        self.camera_fov = rw.rw_float32(self.camera_fov)

    def size(self):
        return 4


class CameraRoll:
    """Camera Keyframe"""
    OBJ_VARIANT_TYPE = 3
    VARIANT_TYPE = 24
    
    def __init__(self, roll=None):
        self.roll = roll
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType24] {self.unknown_float}"
    
    def exbip_rw(self, rw):
        self.roll = rw.rw_float32(self.roll)
    
    def size(self):
        return 4


class OpacitySnap:
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 25
    
    def __init__(self, opacity=None):
        self.opacity = opacity
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::OpacitySnap] {self.unknown_float}"
    
    def exbip_rw(self, rw):
        self.opacity = rw.rw_float32(self.opacity)
    
    def size(self):
        return 4


class KeyframeType26: # What is different about this one and 28?!
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 26
    
    def __init__(self, position=None, rotation=None):
        self.position = position
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType26] {self.position} {self.rotation}"
        
    def exbip_rw(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.rotation = rw.rw_float16s(self.rotation, 4)
    
    def size(self):
        return 14
    
class NodeTRSHalf:
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 27
    
    def __init__(self, position=None, rotation=None, scale=None):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::NodeTRSHalf] {self.position} {self.rotation} {self.scale}"
        
    def exbip_rw(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.rotation = rw.rw_float16s(self.rotation, 4)
        self.scale    = rw.rw_float16s(self.scale, 3)
    
    def size(self):
        return 20

class KeyframeType28:
    """Node Keyframe"""
    OBJ_VARIANT_TYPE = 1
    VARIANT_TYPE = 28
    
    def __init__(self, position=None, rotation=None):
        self.position = position
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType28] {self.position} {self.rotation}"
        
    def exbip_rw(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.rotation = rw.rw_float16s(self.rotation, 4)
    
    def size(self):
        return 14


class KeyframeType29:
    """Material Keyframe"""
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 29
    
    def __init__(self, unknown=None):
        self.unknown = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType29] {self.unknown}"
        
    def exbip_rw(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
    
    def size(self):
        return 4


class KeyframeType30:
    """Material Keyframe"""
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 30
    
    def __init__(self, unknown=None):
        self.unknown_float = unknown
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType30] {self.unknown_float}"
    
    def exbip_rw(self, rw):
        self.unknown_float = rw.rw_float32(self.unknown_float)
        
    def size(self):
        return 4


class NodeTHalf:
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 31
    
    def __init__(self, position=None):
        self.position = position
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::NodeTHalf] {self.position}"
        
    def exbip_rw(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        
    def size(self):
        return 6
        
class NodeTR31:
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 31
    
    def __init__(self, position=None, rotation=None):
        self.position = position
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::NodeTR[31]] {self.position} {self.rotation}"
        
    def exbip_rw(self, rw):
        self.position = rw.rw_float32s(self.position, 3)
        self.rotation = rw.rw_float32s(self.rotation, 4)

    def size(self):
        return 28
           
class NodeRHalf:
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 32
    
    def __init__(self, rotation=None):
        self.rotation = rotation
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::NodeRHalf] {self.rotation}"
        
    def exbip_rw(self, rw):
        self.rotation = rw.rw_float16s(self.rotation, 4)

    def size(self):
        return 20 # Why 20??


class NodeSHalf:
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 33
    
    def __init__(self, scale=None):
        self.scale = scale
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::NodeSHalf] {self.scale}"
        
    def exbip_rw(self, rw):
        self.scale = rw.rw_float16s(self.scale, 3)

    def size(self):
        return 6

             
class NodeTSHalf:
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 34
    
    def __init__(self, position=None, scale=None):
        self.position = position
        self.scale = scale
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::NodeTSHalf] {self.position} {self.scale}"
        
    def exbip_rw(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.scale = rw.rw_float16s(self.scale, 3)
    
    def size(self):
        return 12
    
class NodeRSHalf:
    OBJ_VARIANT_TYPE = None
    VARIANT_TYPE = 35
    
    def __init__(self, rotation=None, scale=None):
        self.rotation = rotation
        self.scale = scale
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::NodeRSHalf] {self.rotation} {self.scale}"
        
    def exbip_rw(self, rw):
        self.rotation = rw.rw_float16s(self.rotation, 4)
        self.scale = rw.rw_float16s(self.scale, 3)
    
    def size(self):
        return 14
        
class Tex1UVSnap(TexUVKeyframe):
    OBJ_VARIANT_TYPE = 2
    VARIANT_TYPE = 36
    CLASSNAME = "Tex1UVSnap"


KEYFRAME_TYPES_V1 = {
    1: NodeTR,
    2: NodeTRS,
    3: KeyframeType3,
    5: KeyframeType5,
    6: AmbientRGB,
    7: DiffuseRGB,
    8: SpecularRGB,
    9: SpecularPower,
    11: KeyframeType11,
    12: Opacity,
    13: Tex0UV,
    14: EmissiveRGB,
    15: KeyframeType15,
    16: KeyframeType16,
    17: KeyframeType17,
    18: KeyframeType18,
    19: KeyframeType19,
    20: Tex1UV,
    21: Tex0UVSnap,
    22: KeyframeType22,
    23: CameraFOV,
    24: CameraRoll,
    25: OpacitySnap,
    26: KeyframeType26,
    27: NodeTRSHalf,
    28: KeyframeType28,
    29: KeyframeType29,
    30: KeyframeType30,
    31: NodeTHalf,
    32: NodeRHalf,
    33: NodeSHalf,
    34: NodeTSHalf,
    35: NodeRSHalf,
    36: Tex1UVSnap
}

KEYFRAME_TYPES_V2 = copy.deepcopy(KEYFRAME_TYPES_V1)
KEYFRAME_TYPES_V2[31] = NodeTR31

        # if   self.keyframe_type == 1:  kf_type = NodeTR         # Node Anim: Only in extra data?
        # elif self.keyframe_type == 2:  kf_type = NodeTRS        # Node Anim: 0x01104970, 0x01105000, 0x01105010, 0x01105020, 0x01105030, 0x01105040, 0x01105060, 0x01105070, 0x01105080, 0x1105090, 0x1105100
        # elif self.keyframe_type == 3:  kf_type = KeyframeType3  # Morph Anim: 0x01105060
        # # elif self.keyframe_type == 4: kf_type = KeyframeType4
        # elif self.keyframe_type == 5:  kf_type = KeyframeType5
        # elif self.keyframe_type == 6:  kf_type = AmbientRGB     # Material Anim: 0x01105040, 0x01105060, 0x01105070, 0x1105090, 0x01105100
        # elif self.keyframe_type == 7:  kf_type = DiffuseRGB     # Material Anim: 0x01105060, 0x01105070, 0x01105100
        # elif self.keyframe_type == 8:  kf_type = SpecularRGB    # Material Anim: 0x01105060, 0x01105070, 0x01105100
        # elif self.keyframe_type == 9:  kf_type = SpecularPower  # Material Anim: 0x01105060, 0x01105020, 0x01105100
        # # elif self.keyframe_type == 10: kf_type = KeyframeType10
        # elif self.keyframe_type == 11: kf_type = KeyframeType11 # Material Anim: 0x01105040, 0x01105060, 0x01105070, 0x01105100
        # elif self.keyframe_type == 12: kf_type = Opacity        # Material Anim: 0x01105000, 0x01105020, 0x01105030, 0x01105040, 0x01105060, 0x1105070, 0x01105080, 0x1105090, 0x1105100
        # elif self.keyframe_type == 13: kf_type = Tex0UV         # Material Anim: 0x01105020, 0x01105030, 0x01105040, 0x01105060, 0x01105070, 0x1105090, 0x01105100
        # elif self.keyframe_type == 14: kf_type = EmissiveRGB    # Material Anim: 0x01105020, 0x01105030, 0x01105040, 0x01105060, 0x01105070, 0x1105090, 0x01105100
        # elif self.keyframe_type == 15: kf_type = KeyframeType15 # Material Anim: 0x01105060, 0x01105070, 0x01105100
        # elif self.keyframe_type == 16: kf_type = KeyframeType16 # Node Anim: 0x01105060, 0x01105070
        # elif self.keyframe_type == 17: kf_type = KeyframeType17 # Seems to be related to EPLs; 17, 18, 19 come as a triplet
        # elif self.keyframe_type == 18: kf_type = KeyframeType18 # Seems to be related to EPLs; 17, 18, 19 come as a triplet
        # elif self.keyframe_type == 19: kf_type = KeyframeType19 # Seems to be related to EPLs; 17, 18, 19 come as a triplet  
        # elif self.keyframe_type == 20: kf_type = Tex1UV # Material Anim: 0x01105100
        # elif self.keyframe_type == 21: kf_type = Tex0UVSnap # Material Anim: 0x01105020, 0x1105030, 0x01105040, 0x01105060, 0x01105070, 0x1105090, 0x01105100
        # elif self.keyframe_type == 22: kf_type = KeyframeType22 # Related to EPLs?
        # elif self.keyframe_type == 23: kf_type = CameraFOV # Camera Anim: 0x01105040, 0x01105060, 0x01105070, 0x01105100
        # elif self.keyframe_type == 24: kf_type = CameraRoll # Camera Anim: 0x01105060, 0x01105070
        # elif self.keyframe_type == 25: kf_type = OpacitySnap    # Material Anim: 0x01105070, 0x1105090, 0x01105100
        # elif self.keyframe_type == 26: kf_type = KeyframeType26
        # elif self.keyframe_type == 27: kf_type = NodeTRSHalf    # Node Anim: 0x01104970, 0x01105000, 0x01105010, 0x01105020, 0x01105030, 0x01105040, 0x01105070, 0x01105080, 0x1105090, 0x01105100
        # elif self.keyframe_type == 28: kf_type = KeyframeType28 # Node Anim: 0x01104970, 0x01105000, 0x01105010, 0x01105020, 0x01105030, 0x01105040, 0x01105060, 0x01105070, 0x01105080, 0x1105090, 0x01105100
        # elif self.keyframe_type == 29: kf_type = KeyframeType29 # Material Anim: 0x01105030, 0x01105040, 0x01105060, 0x01105070, 0x01105080, 0x1105090, 0x01105100
        # elif self.keyframe_type == 30: kf_type = KeyframeType30 # Material Anim: 0x01105060, 0x1105070
        # elif self.keyframe_type == 31: kf_type = NodeTHalf
        # elif self.keyframe_type == 32: kf_type = NodeRHalf
        # elif self.keyframe_type == 33: kf_type = NodeSHalf
        # elif self.keyframe_type == 34: kf_type = NodeTSHalf
        # elif self.keyframe_type == 35: kf_type = NodeRSHalf
        # elif self.keyframe_type == 36: kf_type = Tex1UVSnap     # Material Anim: 0x1105100         
        # else: raise NotImplementedError(f"Unknown Keyframe type: '{self.keyframe_type}'")