from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format
from ...CommonStructures import BitVector0x20


class LightFlags(BitVector0x20):
    flag_0      = BitVector0x20.DEF_FLAG(0x00) # Usually True
    unk_setting = BitVector0x20.DEF_FLAG(0x01) # Switches mode
    flag_2      = BitVector0x20.DEF_FLAG(0x02) # Everything onwards unused
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


class LightBinary(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = LightFlags(endianness)
        self.type  = None
        self.color_1 = None # Always [1., 1., 1., 1.]
        self.color_2 = None
        self.color_3 = None # Always [1., 1., 1., 1.]
        
        self.inner_radius = None
        self.outer_radius = None
        
        # Hacky for now, fix if any correspondences between light types is found
        
        # Type 1 data
        self.unknown_0x28 = None # unk 1
        self.unknown_0x2C = None # unk 2
        self.unknown_0x30 = None # unk 3
        
        # Type 2 data
        self.unknown_0x34 = None # unk 1 # 0
        self.unknown_0x38 = None # unk 2 # 0
        self.unknown_0x3C = None # unk 3 # 0
        
        self.unknown_0x48 = None # unk 4 # 0
        self.unknown_0x4C = None # unk 5 # 0
        self.unknown_0x50 = None # unk 6 # 0
        
        # Type 3 data
        self.unknown_0x54 = None # unk 1 # 0
        self.unknown_0x58 = None # unk 2 # 0
        self.unknown_0x5C = None # unk 3 # 1
        
        self.unknown_0x60 = None # 0 - 0.79
        self.unknown_0x64 = None # 0 - 0.94
        self.unknown_0x68 = None # 0
        self.unknown_0x6C = None # 0
        self.unknown_0x70 = None # 0
        
        self.unknown_0x7C = None # unk 4 # 0
        self.unknown_0x80 = None # unk 5 # 0
        self.unknown_0x84 = None # unk 6 # 0
                   
    def __repr__(self):
        out = f"[GFD::SceneContainer::SceneNode::Attachment::Light] " \
            f"{safe_format(self.flags._value, hex32_format)} {self.type}" \
            f"{safe_format(self.color_1, list)}" \
            f"{safe_format(self.color_2, list)}" \
            f"{safe_format(self.color_3, list)}"
        
        if self.type == 1:
            out += f"\n{self.unknown_0x28} {self.unknown_0x2C} {self.unknown_0x30}"
        elif self.type == 2:
            out += f"\n{self.unknown_0x34} {self.unknown_0x38} {self.unknown_0x3C}"
            out += f"\n{self.inner_radius} {self.outer_radius} {self.unknown_0x48} {self.unknown_0x4C} {self.unknown_0x50}"
        elif self.type == 3:
            out += f"\n{self.unknown_0x54} {self.unknown_0x58} {self.unknown_0x5C} {self.unknown_0x60} "
            out += f"{self.unknown_0x64} {self.unknown_0x68} {self.unknown_0x6C} {self.unknown_0x70} "
            out += f"\n{self.inner_radius} {self.outer_radius} {self.unknown_0x7C} {self.unknown_0x80} {self.unknown_0x84}"
            
        return out
            
    def read_write(self, rw, version):
        self.flags   = rw.rw_obj(self.flags)
        self.type    = rw.rw_uint32(self.type)
        self.color_1 = rw.rw_float32s(self.color_1, 4)
        self.color_2 = rw.rw_float32s(self.color_2, 4)
        self.color_3 = rw.rw_float32s(self.color_3, 4)
        
        if self.type == 1: # Directional
            self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
            self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
            self.unknown_0x30 = rw.rw_float32(self.unknown_0x30)
        elif self.type == 2: # Sphere / Point
            self.unknown_0x34 = rw.rw_float32(self.unknown_0x34)
            self.unknown_0x38 = rw.rw_float32(self.unknown_0x38)
            self.unknown_0x3C = rw.rw_float32(self.unknown_0x3C)
            
            if self.flags.unk_setting:
                self.inner_radius = rw.rw_float32(self.inner_radius)
                self.outer_radius = rw.rw_float32(self.outer_radius)
            else:
                self.unknown_0x48 = rw.rw_float32(self.unknown_0x48)
                self.unknown_0x4C = rw.rw_float32(self.unknown_0x4C)
                self.unknown_0x50 = rw.rw_float32(self.unknown_0x50)
        elif self.type == 3: # Hemisphere / Spot
            self.unknown_0x54 = rw.rw_float32(self.unknown_0x54)
            self.unknown_0x58 = rw.rw_float32(self.unknown_0x58)
            self.unknown_0x5C = rw.rw_float32(self.unknown_0x5C)
            
            self.unknown_0x60 = rw.rw_float32(self.unknown_0x60)
            self.unknown_0x64 = rw.rw_float32(self.unknown_0x64)
            self.unknown_0x68 = rw.rw_float32(self.unknown_0x68)
            self.unknown_0x6C = rw.rw_float32(self.unknown_0x6C)
            self.unknown_0x70 = rw.rw_float32(self.unknown_0x70)
            
            if self.flags.unk_setting:
                self.inner_radius = rw.rw_float32(self.inner_radius)
                self.outer_radius = rw.rw_float32(self.outer_radius)
            else:
                self.unknown_0x7C = rw.rw_float32(self.unknown_0x7C)
                self.unknown_0x80 = rw.rw_float32(self.unknown_0x80)
                self.unknown_0x84 = rw.rw_float32(self.unknown_0x84)
        else:
            raise NotImplementedError(f"Unknown light type '{self.type}'")
