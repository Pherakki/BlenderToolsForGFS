from .....serialization.Serializable import Serializable
from ..CommonStructures import ObjectNameBase, ObjectName_0x01080010


class TextureRefBinaryBase(Serializable):
    OBJ_NAME_TYPE = ObjectNameBase
    
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name                  = self.OBJ_NAME_TYPE(endianness)
        self.unknown_0x04          = None
        self.unknown_0x08          = None
        self.has_texture_filtering = None
        self.unknown_0x0A          = None
        self.unknown_0x0B          = None
        self.unknown_0x0C          = None
        
    def __repr__(self):
        return f"[GFD::Material::TextureRef] {self.name.string} {self.unknown_0x04} {self.unknown_0x08} {self.has_texture_filtering} {self.unknown_0x0A} {self.unknown_0x0B} {self.unknown_0x0C}"
        
    def read_write(self, rw):
        self.name                  = rw.rw_obj(self.name)
        self.unknown_0x04          = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08          = rw.rw_uint8(self.unknown_0x08)
        self.has_texture_filtering = rw.rw_uint8(self.has_texture_filtering)
        self.unknown_0x0A          = rw.rw_uint8(self.unknown_0x0A)
        self.unknown_0x0B          = rw.rw_uint8(self.unknown_0x0B)
        self.unknown_0x0C          = rw.rw_float32s(self.unknown_0x0C, 0x10)


class TextureRefBinary_0x01080010(TextureRefBinaryBase):
    OBJ_NAME_TYPE = ObjectName_0x01080010
