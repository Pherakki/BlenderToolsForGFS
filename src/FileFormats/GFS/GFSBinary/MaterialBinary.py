from ....serialization.Serializable import Serializable
from ....serialization.utils import safe_format, hex32_format
from .CommonStructures import ObjectName


class MaterialBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name         = ObjectName(endianness)
        self.flags        = None
        self.ambient      = None
        self.diffuse      = None
        self.specular     = None
        self.emissive     = None
        self.unknown_0x48 = None
        self.unknown_0x4C = None
        self.draw_method  = None
        self.unknown_0x51 = None
        self.unknown_0x56 = None
        self.unknown_0x58 = None
        self.unknown_0x5A = None
        self.unknown_0x5C = None
        self.unknown_0x5E = None
        self.unknown_0x60 = None
        self.unknown_0x64 = None
        self.disable_backface_culling = None
        self.unknown_0x6A = None
        
        self.diffuse_texture    = None
        self.normal_texture     = None
        self.specular_texture   = None
        self.reflection_texture = None
        self.highlight_texture  = None
        self.glow_texture       = None
        self.night_texture      = None
        self.detail_texture     = None
        self.shadow_texture     = None
        
        self.attribute_count = 0
        self.attributes = []
        
    def __repr__(self):
        return f"[GFD::Material] {self.name} "                                                                   \
               f"{safe_format(self.flags, hex32_format)} "                                                       \
               f"{safe_format(self.ambient, list)} {safe_format(self.diffuse, list)} "                           \
               f"{safe_format(self.specular, list)} {safe_format(self.emissive, list)} "                         \
               f"{self.unknown_0x48} {self.unknown_0x4C} "                                                       \
               f"{safe_format(self.unknown_0x50, list)} {self.unknown_0x56} "                                    \
               f"{self.unknown_0x58} {self.unknown_0x5A} {self.unknown_0x5C} {self.unknown_0x5E} "               \
               f"{safe_format(self.unknown_0x60, hex32_format)} {safe_format(self.unknown_0x64, hex32_format)} " \
               f"{self.disable_backface_culling} {self.unknown_0x6A} {self.attribute_count}"

    def read_write(self, rw):
        self.name         = rw.rw_obj(self.name)
        self.flags        = rw.rw_uint32(self.flags)
        
        self.ambient      = rw.rw_float32s(self.ambient, 4)
        self.diffuse      = rw.rw_float32s(self.diffuse, 4)
        self.specular     = rw.rw_float32s(self.specular, 4)
        self.emissive     = rw.rw_float32s(self.emissive, 4)
        self.unknown_0x48 = rw.rw_float32(self.unknown_0x48)
        self.unknown_0x4C = rw.rw_float32(self.unknown_0x4C)
        self.draw_method  = rw.rw_uint8(self.draw_method)
        self.unknown_0x51 = rw.rw_uint8s(self.unknown_0x51, 5)
        self.unknown_0x56 = rw.rw_uint16(self.unknown_0x56)
        self.unknown_0x58 = rw.rw_uint16(self.unknown_0x58)
        self.unknown_0x5A = rw.rw_int16(self.unknown_0x5A)
        self.unknown_0x5C = rw.rw_int16(self.unknown_0x5C)
        self.unknown_0x5E = rw.rw_int16(self.unknown_0x5E)
        self.unknown_0x60 = rw.rw_uint32(self.unknown_0x60)
        self.unknown_0x64 = rw.rw_uint32(self.unknown_0x64)
        self.disable_backface_culling = rw.rw_int16(self.disable_backface_culling)
        self.unknown_0x6A = rw.rw_uint32(self.unknown_0x6A)
        
        # Handle textures
        if self.flags & 0x00100000:
            if rw.mode() == "read": self.diffuse_texture    = TextureRefBinary()
            rw.rw_obj(self.diffuse_texture)
        if self.flags & 0x00200000:
            if rw.mode() == "read": self.normal_texture     = TextureRefBinary()
            rw.rw_obj(self.normal_texture)
        if self.flags & 0x00400000:
            if rw.mode() == "read": self.specular_texture   = TextureRefBinary()
            rw.rw_obj(self.specular_texture)
        if self.flags & 0x00800000:
            if rw.mode() == "read": self.reflection_texture = TextureRefBinary()
            rw.rw_obj(self.reflection_texture)
        if self.flags & 0x01000000:
            if rw.mode() == "read": self.highlight_texture  = TextureRefBinary()
            rw.rw_obj(self.highlight_texture)
        if self.flags & 0x02000000:
            if rw.mode() == "read": self.glow_texture       = TextureRefBinary()
            rw.rw_obj(self.glow_texture)
        if self.flags & 0x04000000:
            if rw.mode() == "read": self.night_texture      = TextureRefBinary()
            rw.rw_obj(self.night_texture)
        if self.flags & 0x08000000:
            if rw.mode() == "read": self.detail_texture     = TextureRefBinary()
            rw.rw_obj(self.detail_texture)
        if self.flags & 0x10000000:
            if rw.mode() == "read": self.shadow_texture     = TextureRefBinary()
            rw.rw_obj(self.shadow_texture)
            
        # Attributes
        if self.flags & 0x00010000:
            self.attribute_count = rw.rw_uint32(self.attribute_count)
            self.attributes = rw.rw_obj_array(self.attributes, MaterialAttributeBinary, self.attribute_count)


class TextureRefBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name     = ObjectName(endianness)
        self.unknowns = None
        
    def __repr__(self):
        return f"[GFD::Material::TextureRef] {self.name} {self.unknowns}"
        
    def read_write(self, rw):
        self.name         = rw.rw_obj(self.name)
        self.unknowns     = rw.rw_uint32s(self.unknowns, 0x12)


class MaterialAttributeBinary(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.ID    = None
        self.data  = []
        
    def __repr__(self):
        return f"[GFD::Material::Attribute] {safe_format(self.flags, hex32_format)} {self.ID} {safe_format(self.data, list)}"
    
    def read_write(self, rw):
        self.flags = rw.rw_uint16(self.flags)
        self.ID = rw.rw_uint16(self.ID)
    
        if self.ID == 0:
            self.data = rw.rw_bytestring(self.data, 40)
        elif self.ID == 1:
            self.data = rw.rw_bytestring(self.data, 52)
        elif self.ID == 2:
            self.data = rw.rw_bytestring(self.data, 8)
        elif self.ID == 3:
            self.data = rw.rw_bytestring(self.data, 52)
        elif self.ID == 4:
            self.data = rw.rw_bytestring(self.data, 81)
        elif self.ID == 5:
            self.data = rw.rw_bytestring(self.data, 68)
        elif self.ID == 6:
            self.data = rw.rw_bytestring(self.data, 12)
        elif self.ID == 7:
            self.data = rw.rw_bytestring(self.data, 0)
        else:
            raise NotImplementedError(f"Unrecognised Attribute ID: {self.ID}")
