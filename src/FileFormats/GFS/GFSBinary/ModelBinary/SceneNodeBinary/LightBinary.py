from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format


class LightBinary(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.type  = None
        self.color_1 = None
        self.color_2 = None
        self.color_3 = None
        
        # Hacky for now, fix if any correspondences between light types is found
        
        # Type 1 data
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        self.unknown_0x30 = None
        
        # Type 2 data
        self.unknown_0x34 = None
        self.unknown_0x38 = None
        self.unknown_0x3C = None
        self.unknown_0x40 = None
        self.unknown_0x44 = None
        self.unknown_0x48 = None
        self.unknown_0x4C = None
        self.unknown_0x50 = None
        
        # Type 3 data
        self.unknown_0x54 = None
        self.unknown_0x58 = None
        self.unknown_0x5C = None
        self.unknown_0x60 = None
        self.unknown_0x64 = None
        self.unknown_0x68 = None
        self.unknown_0x6C = None
        self.unknown_0x70 = None
        self.unknown_0x74 = None
        self.unknown_0x78 = None
        self.unknown_0x7C = None
        self.unknown_0x80 = None
        self.unknown_0x84 = None
                   
    def __repr__(self):
        out = f"[GFD::SceneContainer::SceneNode::Attachment::Light] " \
            f"{safe_format(self.flags, hex32_format)} {self.type}" \
            f"{safe_format(self.color_1, list)}" \
            f"{safe_format(self.color_2, list)}" \
            f"{safe_format(self.color_3, list)}"
        
        if self.type == 1:
            out += f"\n{self.unknown_0x28} {self.unknown_0x2C} {self.unknown_0x30}"
        elif self.type == 2:
            out += f"\n{self.unknown_0x34} {self.unknown_0x38} {self.unknown_0x3C}"
            out += f"\n{self.unknown_0x40} {self.unknown_0x44} {self.unknown_0x48} {self.unknown_0x4C} {self.unknown_0x50}"
        elif self.type == 3:
            out += f"\n{self.unknown_0x54} {self.unknown_0x58} {self.unknown_0x5C} {self.unknown_0x60} "
            out += f"{self.unknown_0x64} {self.unknown_0x68} {self.unknown_0x6C} {self.unknown_0x70} "
            out += f"\n{self.unknown_0x74} {self.unknown_0x78} {self.unknown_0x7C} {self.unknown_0x80} {self.unknown_0x84}"
            
        return out
            
    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        self.type = rw.rw_uint32(self.type)
        self.color_1 = rw.rw_float32s(self.color_1, 4)
        self.color_2 = rw.rw_float32s(self.color_2, 4)
        self.color_3 = rw.rw_float32s(self.color_3, 4)
        
        if self.type == 1:
            self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
            self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
            self.unknown_0x30 = rw.rw_float32(self.unknown_0x30)
        elif self.type == 2:
            self.unknown_0x34 = rw.rw_float32(self.unknown_0x34)
            self.unknown_0x38 = rw.rw_float32(self.unknown_0x38)
            self.unknown_0x3C = rw.rw_float32(self.unknown_0x3C)
            
            if self.flags & 0x00000002:
                self.unknown_0x40 = rw.rw_float32(self.unknown_0x40)
                self.unknown_0x44 = rw.rw_float32(self.unknown_0x44)
            else:
                self.unknown_0x48 = rw.rw_float32(self.unknown_0x48)
                self.unknown_0x4C = rw.rw_float32(self.unknown_0x4C)
                self.unknown_0x50 = rw.rw_float32(self.unknown_0x50)
        elif self.type == 3:
            self.unknown_0x54 = rw.rw_float32(self.unknown_0x54)
            self.unknown_0x58 = rw.rw_float32(self.unknown_0x58)
            self.unknown_0x5C = rw.rw_float32(self.unknown_0x5C)
            self.unknown_0x60 = rw.rw_float32(self.unknown_0x60)
            
            self.unknown_0x64 = rw.rw_float32(self.unknown_0x64)
            self.unknown_0x68 = rw.rw_float32(self.unknown_0x68)
            self.unknown_0x6C = rw.rw_float32(self.unknown_0x6C)
            self.unknown_0x70 = rw.rw_float32(self.unknown_0x70)
            
            if self.flags & 0x00000002:
                self.unknown_0x74 = rw.rw_float32(self.unknown_0x74)
                self.unknown_0x78 = rw.rw_float32(self.unknown_0x78)
            else:
                self.unknown_0x7C = rw.rw_float32(self.unknown_0x7C)
                self.unknown_0x80 = rw.rw_float32(self.unknown_0x80)
                self.unknown_0x84 = rw.rw_float32(self.unknown_0x84)
        else:
            raise NotImplementedError(f"Unknown light type '{self.type}'")