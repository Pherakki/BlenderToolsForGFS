from .......serialization.Serializable import Serializable
from .......serialization.utils import safe_format, hex32_format
from ....CommonStructures import ObjectName, BitVector0x20
from .EPLAnimationBinary import EPLAnimationBinary
from .. import NodeBinary


class EPLFlags(BitVector0x20):
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


class EPLBinary(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = EPLFlags()
        self.root_node = NodeBinary.SceneNodeBinary(endianness)
        self.animation = EPLAnimationBinary(endianness)
        self.unknown = 0
                   
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL {safe_format(self.flags._value, hex32_format)}]"
            
    def read_write(self, rw, version):
        rw.rw_obj(self.flags)
        rw.rw_obj(self.root_node, version)
        rw.rw_obj(self.animation, version)
        if version > 0x01105060:
            self.unknown = rw.rw_uint16(self.unknown)
