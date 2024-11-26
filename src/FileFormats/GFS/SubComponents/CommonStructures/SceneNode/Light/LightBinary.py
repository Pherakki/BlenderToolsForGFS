from .......serialization.formatters import HEX32_formatter, list_formatter
from ....CommonStructures import BitVector0x20


class LightFlags(BitVector0x20):
    flag_0      = BitVector0x20.DEF_FLAG(0x00) # Usually True
    unk_setting = BitVector0x20.DEF_FLAG(0x01) # Switches mode
    flag_2      = BitVector0x20.DEF_FLAG(0x02) # Everything onwards unused


class LightBinary:
    def __init__(self):
        self.flags   = LightFlags()
        self.type    = None
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
        
        self.unknown_0x88 = 0
        self.unknown_0x8C = 0
                   
    def __repr__(self):
        out = f"[GFD::SceneContainer::SceneNode::Attachment::Light] " \
            f"{HEX32_formatter(self.flags._value)} {self.type}" \
            f"{list_formatter(self.color_1)}" \
            f"{list_formatter(self.color_2)}" \
            f"{list_formatter(self.color_3)}"
        
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
            
    def exbip_rw(self, rw, version):
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
        
        if version >= 0x02110192:
            self.unknown_0x88 = rw.rw_float32(self.unknown_0x88)
        if version >  0x02110202:
            self.unknown_0x8C = rw.rw_float32(self.unknown_0x8C)
