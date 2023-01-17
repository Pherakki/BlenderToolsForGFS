from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format
from ...CommonStructures import ObjectName, BitVector0x20, SizedObjArray
from ...Animations.Binary.AnimationBinary import AnimationBinary


class EPLAnimationFlags(BitVector0x20):
    flag_0      = BitVector0x20.DEF_FLAG(0x00)
    flag_1      = BitVector0x20.DEF_FLAG(0x01)
    flag_2      = BitVector0x20.DEF_FLAG(0x02)
    flag_3      = BitVector0x20.DEF_FLAG(0x03)
    flag_4      = BitVector0x20.DEF_FLAG(0x04)
    flag_5      = BitVector0x20.DEF_FLAG(0x05)
    flag_6      = BitVector0x20.DEF_FLAG(0x06)
    flag_7      = BitVector0x20.DEF_FLAG(0x07)
    flag_8      = BitVector0x20.DEF_FLAG(0x08)
    flag_9      = BitVector0x20.DEF_FLAG(0x09)
    flag_10     = BitVector0x20.DEF_FLAG(0x0A)
    flag_11     = BitVector0x20.DEF_FLAG(0x0B)
    flag_12     = BitVector0x20.DEF_FLAG(0x0C)
    flag_13     = BitVector0x20.DEF_FLAG(0x0D)
    flag_14     = BitVector0x20.DEF_FLAG(0x0E)
    flag_15     = BitVector0x20.DEF_FLAG(0x0F)
    flag_16     = BitVector0x20.DEF_FLAG(0x10)
    flag_17     = BitVector0x20.DEF_FLAG(0x11)
    flag_18     = BitVector0x20.DEF_FLAG(0x12)
    flag_19     = BitVector0x20.DEF_FLAG(0x13)
    flag_20     = BitVector0x20.DEF_FLAG(0x14)
    flag_21     = BitVector0x20.DEF_FLAG(0x15)
    flag_22     = BitVector0x20.DEF_FLAG(0x16)
    flag_23     = BitVector0x20.DEF_FLAG(0x17)
    flag_24     = BitVector0x20.DEF_FLAG(0x18)
    flag_25     = BitVector0x20.DEF_FLAG(0x19)
    flag_26     = BitVector0x20.DEF_FLAG(0x1A)
    flag_27     = BitVector0x20.DEF_FLAG(0x1B)
    flag_28     = BitVector0x20.DEF_FLAG(0x1C)
    flag_29     = BitVector0x20.DEF_FLAG(0x1D)
    flag_30     = BitVector0x20.DEF_FLAG(0x1E)
    flag_31     = BitVector0x20.DEF_FLAG(0x1F)


class EPLAnimationBinary(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = EPLAnimationFlags()
        self.unknown_0x04 = None
        self.animation = AnimationBinary()
        self.epl_controllers = SizedObjArray(EPLAnimationController)
                   
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Animation]"
            
    def read_write(self, rw, version):
        rw.rw_obj(self.flags)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        rw.rw_obj(self.animation, version)
        rw.rw_obj(self.epl_controllers)

class EPLAnimationController(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.controller_idx = None
        self.unknown_0x0C = None
        
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Animation::Controller] {self.unknown_0x00} {self.unknown_0x04} {self.controller_idx} {self.unknown_0x0C}"
    
    def read_write(self, rw):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.controller_idx = rw.rw_uint32(self.controller_idx)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)
