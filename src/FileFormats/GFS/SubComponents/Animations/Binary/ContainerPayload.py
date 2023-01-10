from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format
from ...CommonStructures import SizedObjArray, BitVector
from .AnimationBinary import AnimationBinary
from .AnimationBinary import UnknownAnimationChunk


class AnimationPackFlags(BitVector):
    flag_0            = BitVector.DEF_FLAG(0x00)
    flag_1            = BitVector.DEF_FLAG(0x01)
    has_unknown_chunk = BitVector.DEF_FLAG(0x02)
    flag_3            = BitVector.DEF_FLAG(0x03)
    flag_4            = BitVector.DEF_FLAG(0x04)
    flag_5            = BitVector.DEF_FLAG(0x05)
    flag_6            = BitVector.DEF_FLAG(0x06)
    flag_7            = BitVector.DEF_FLAG(0x07)
    flag_8            = BitVector.DEF_FLAG(0x08)
    flag_9            = BitVector.DEF_FLAG(0x09)
    flag_10           = BitVector.DEF_FLAG(0x0A)
    flag_11           = BitVector.DEF_FLAG(0x0B)
    flag_12           = BitVector.DEF_FLAG(0x0C)
    flag_13           = BitVector.DEF_FLAG(0x0D)
    flag_14           = BitVector.DEF_FLAG(0x0E)
    flag_15           = BitVector.DEF_FLAG(0x0F)
    flag_16           = BitVector.DEF_FLAG(0x10)
    flag_17           = BitVector.DEF_FLAG(0x11)
    flag_18           = BitVector.DEF_FLAG(0x12)
    flag_19           = BitVector.DEF_FLAG(0x13)
    flag_20           = BitVector.DEF_FLAG(0x14)
    flag_21           = BitVector.DEF_FLAG(0x15)
    flag_22           = BitVector.DEF_FLAG(0x16)
    flag_23           = BitVector.DEF_FLAG(0x17)
    flag_24           = BitVector.DEF_FLAG(0x18)
    flag_25           = BitVector.DEF_FLAG(0x19)
    flag_26           = BitVector.DEF_FLAG(0x1A)
    flag_27           = BitVector.DEF_FLAG(0x1B)
    flag_28           = BitVector.DEF_FLAG(0x1C)
    flag_29           = BitVector.DEF_FLAG(0x1D)
    flag_30           = BitVector.DEF_FLAG(0x1E)
    flag_31           = BitVector.DEF_FLAG(0x1F)


class AnimationPayload(Serializable):
    TYPECODE = 0x000100FD
        
    APPROVED_VERSIONS = set([
        #0x01104920,
        #0x01104950,
        #0x01104960,
        #0x01104970,
        #0x01105000,
        #0x01105010,
        #0x01105020,
        #0x01105030,
        #0x01105040,
        #0x01105060,
        #0x01105070,
        #0x01105080,
        #0x01105090,
        0x01105100
        ])
    
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags              = AnimationPackFlags()
        self.animations         = SizedObjArray(AnimationBinary)
        self.blend_animations   = SizedObjArray(AnimationBinary)
        self.unknown_anim_chunk = None
        
    def __repr__(self):
        return f"[GFDBinary::AnimationData {safe_format(self.flags._value, hex32_format)}] Anims: {self.animations.count} Blend Anims: {self.blend_animations.count} Extra: {safe_format(self.flags, lambda x: bool(x.has_unknown_chunk))}"

    def read_write(self, rw, version):
        if version > 0x01104950:
            self.flags = rw.rw_obj(self.flags)
        rw.rw_obj(self.animations, version)
        rw.rw_obj(self.blend_animations, version)
        
        if self.flags.has_unknown_chunk:
            self.unknown_anim_chunk = rw.rw_new_obj(self.unknown_anim_chunk, UnknownAnimationChunk, version)

