from ......serialization.formatters import HEX32_formatter, safe_formatter
from ...CommonStructures import BitVector0x20
from ...CommonStructures.SizedObjArrayModule import SizedObjArray
from .AnimationBinary import AnimationBinary
from .AnimationBinary import LookAtAnimationsBinary


class AnimationPackFlags(BitVector0x20):
    has_lookat_anims  = BitVector0x20.DEF_FLAG(0x02) # USED
    flag_3            = BitVector0x20.DEF_FLAG(0x03) # USED


class AnimationPayload:
    TYPECODE = 0x000100FD
    
    def __init__(self):
        self.flags              = AnimationPackFlags()
        self.animations         = SizedObjArray(AnimationBinary)
        self.blend_animations   = SizedObjArray(AnimationBinary)
        self.lookat_animations  = None
        self.unknown_animations = SizedObjArray(AnimationBinary)
        
    def __repr__(self):
        return f"[GFDBinary::AnimationData {HEX32_formatter(self.flags._value)}] Anims: {self.animations.count} Blend Anims: {self.blend_animations.count} Extra: {safe_formatter(lambda x: bool(x.has_lookat_anims))(self.flags)}"

    def exbip_rw(self, rw, version):
        if version > 0x01104950:
            self.flags = rw.rw_obj(self.flags)
        rw.rw_obj(self.animations, version)
        rw.rw_obj(self.blend_animations, version)
        
        if self.flags.has_lookat_anims:
            self.lookat_animations = rw.rw_dynamic_obj(self.lookat_animations, LookAtAnimationsBinary, version)

        if version > 0x02109900:
            rw.rw_obj(self.unknown_animations, version)
