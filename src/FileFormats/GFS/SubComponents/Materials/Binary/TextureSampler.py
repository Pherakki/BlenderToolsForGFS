from ......serialization.Serializable import Serializable
from ...CommonStructures import ObjectName


class TextureSamplerBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name                  = ObjectName(endianness)
        self.unknown_0x04          = None
        self.unknown_0x08          = None
        self.has_texture_filtering = None
        self.wrap_mode_u           = None
        self.wrap_mode_v           = None
        self.unknown_0x0C          = None
        
    def __repr__(self):
        return f"[GFD::Material::TextureSampler] {self.name.string} {self.unknown_0x04} {self.unknown_0x08} {self.has_texture_filtering} {self.wrap_mode_u} {self.wrap_mode_v} {self.unknown_0x0C}"
        
    def read_write(self, rw, version):
        self.name                  = rw.rw_obj(self.name, version, encoding="shift-jis")
        self.unknown_0x04          = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08          = rw.rw_uint8(self.unknown_0x08)
        self.has_texture_filtering = rw.rw_uint8(self.has_texture_filtering)
        self.wrap_mode_u           = rw.rw_uint8(self.wrap_mode_u)  # 0 = repeat, 1 = mirror
        self.wrap_mode_v           = rw.rw_uint8(self.wrap_mode_v)
        self.unknown_0x0C          = rw.rw_float32s(self.unknown_0x0C, 0x10)
