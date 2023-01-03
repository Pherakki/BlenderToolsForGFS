from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format
from ...CommonStructures import ObjectName, SizedObjArray, BitVector
from .TextureReference import TextureRefBinary


class MaterialFlags(BitVector):
    flag_0                 = BitVector.DEF_FLAG(0x00)
    flag_1                 = BitVector.DEF_FLAG(0x01)
    flag_2                 = BitVector.DEF_FLAG(0x02)
    flag_3                 = BitVector.DEF_FLAG(0x03)
    use_vertex_colors      = BitVector.DEF_FLAG(0x04)
    flag_5                 = BitVector.DEF_FLAG(0x05)
    flag_6                 = BitVector.DEF_FLAG(0x06)
    use_light_1            = BitVector.DEF_FLAG(0x07)
    flag_8                 = BitVector.DEF_FLAG(0x08)
    flag_9                 = BitVector.DEF_FLAG(0x09)
    flag_10                = BitVector.DEF_FLAG(0x0A)
    use_light_2            = BitVector.DEF_FLAG(0x0B)
    purple_wireframe       = BitVector.DEF_FLAG(0x0C)
    flag_13                = BitVector.DEF_FLAG(0x0D)
    receive_shadow         = BitVector.DEF_FLAG(0x0E)
    cast_shadow            = BitVector.DEF_FLAG(0x0F)
    has_attributes         = BitVector.DEF_FLAG(0x10)
    flag_17                = BitVector.DEF_FLAG(0x11)
    flag_18                = BitVector.DEF_FLAG(0x12)
    disable_bloom          = BitVector.DEF_FLAG(0x13)
    has_diffuse_texture    = BitVector.DEF_FLAG(0x14)
    has_normal_texture     = BitVector.DEF_FLAG(0x15)
    has_specular_texture   = BitVector.DEF_FLAG(0x16)
    has_reflection_texture = BitVector.DEF_FLAG(0x17)
    has_highlight_texture  = BitVector.DEF_FLAG(0x18)
    has_glow_texture       = BitVector.DEF_FLAG(0x19)
    has_night_texture      = BitVector.DEF_FLAG(0x1A)
    has_detail_texture     = BitVector.DEF_FLAG(0x1B)
    has_shadow_texture     = BitVector.DEF_FLAG(0x1C)
    flag_29                = BitVector.DEF_FLAG(0x1D)
    flag_30                = BitVector.DEF_FLAG(0x1E)
    flag_31                = BitVector.DEF_FLAG(0x1F)


class MaterialBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name         = ObjectName(endianness)
        self.flags        = MaterialFlags(endianness)
        self.ambient      = None
        self.diffuse      = None
        self.specular     = None
        self.emissive     = None
        self.unknown_0x48 = None
        self.unknown_0x4C = None
        self.draw_method  = None
        self.unknown_0x51 = None
        self.unknown_0x52 = None
        self.unknown_0x53 = None
        self.unknown_0x54 = None
        self.unknown_0x55 = None
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
        
        self.attributes = SizedObjArray(MaterialAttributeBinary)
        
    def __repr__(self):
        return f"[GFD::Material] {self.name} "                                                                   \
               f"{safe_format(self.flags._value, hex32_format)} "                                                       \
               f"{safe_format(self.ambient, list)} {safe_format(self.diffuse, list)} "                           \
               f"{safe_format(self.specular, list)} {safe_format(self.emissive, list)} "                         \
               f"{self.unknown_0x48} {self.unknown_0x4C} "                                                       \
               f"{safe_format(self.unknown_0x50, list)} {self.unknown_0x56} "                                    \
               f"{self.unknown_0x58} {self.unknown_0x5A} {self.unknown_0x5C} {self.unknown_0x5E} "               \
               f"{safe_format(self.unknown_0x60, hex32_format)} {safe_format(self.unknown_0x64, hex32_format)} " \
               f"{self.disable_backface_culling} {self.unknown_0x6A} {self.attribute_count}"

    def read_write(self, rw, version):
        self.name         = rw.rw_obj(self.name, version)
        self.flags        = rw.rw_obj(self.flags)
        
        self.ambient      = rw.rw_float32s(self.ambient, 4)
        self.diffuse      = rw.rw_float32s(self.diffuse, 4)
        self.specular     = rw.rw_float32s(self.specular, 4)
        self.emissive     = rw.rw_float32s(self.emissive, 4)
        self.unknown_0x48 = rw.rw_float32(self.unknown_0x48)
        self.unknown_0x4C = rw.rw_float32(self.unknown_0x4C)
        self.draw_method  = rw.rw_uint8(self.draw_method)
        self.unknown_0x51 = rw.rw_uint8(self.unknown_0x51)
        self.unknown_0x52 = rw.rw_uint8(self.unknown_0x52)
        self.unknown_0x53 = rw.rw_uint8(self.unknown_0x53)
        self.unknown_0x54 = rw.rw_uint8(self.unknown_0x54)
        self.unknown_0x55 = rw.rw_uint8(self.unknown_0x55)
        self.unknown_0x56 = rw.rw_uint16(self.unknown_0x56)
        self.unknown_0x58 = rw.rw_uint16(self.unknown_0x58)
        self.unknown_0x5A = rw.rw_int16(self.unknown_0x5A)
        self.unknown_0x5C = rw.rw_int16(self.unknown_0x5C)
        self.unknown_0x5E = rw.rw_int16(self.unknown_0x5E)
        self.unknown_0x60 = rw.rw_uint32(self.unknown_0x60)
        self.unknown_0x64 = rw.rw_uint32(self.unknown_0x64)
        self.disable_backface_culling = rw.rw_int16(self.disable_backface_culling)
        self.unknown_0x6A = rw.rw_uint32(self.unknown_0x6A) # NOT present for 0x01105080
        
        # Handle textures
        if self.flags.has_diffuse_texture:    self.diffuse_texture    = rw.rw_new_obj(self.diffuse_texture,    TextureRefBinary, version)
        if self.flags.has_normal_texture:     self.normal_texture     = rw.rw_new_obj(self.normal_texture,     TextureRefBinary, version)
        if self.flags.has_specular_texture:   self.specular_texture   = rw.rw_new_obj(self.specular_texture,   TextureRefBinary, version)
        if self.flags.has_reflection_texture: self.reflection_texture = rw.rw_new_obj(self.reflection_texture, TextureRefBinary, version)
        if self.flags.has_highlight_texture:  self.highlight_texture  = rw.rw_new_obj(self.highlight_texture,  TextureRefBinary, version)
        if self.flags.has_glow_texture:       self.glow_texture       = rw.rw_new_obj(self.glow_texture,       TextureRefBinary, version)
        if self.flags.has_night_texture:      self.night_texture      = rw.rw_new_obj(self.night_texture,      TextureRefBinary, version)
        if self.flags.has_detail_texture:     self.detail_texture     = rw.rw_new_obj(self.detail_texture,     TextureRefBinary, version)
        if self.flags.has_shadow_texture:     self.shadow_texture     = rw.rw_new_obj(self.shadow_texture,     TextureRefBinary, version)
            
        # Attributes
        if self.flags.has_attributes:
            rw.rw_obj(self.attributes, version)


class MaterialAttributeBinary(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.ID    = None
        self.data  = []
        
    def __repr__(self):
        return f"[GFD::Material::AttributeBinary] {safe_format(self.flags, hex32_format)} {self.ID} {safe_format(self.data, list)}"
    
    def read_write(self, rw, version):
        self.flags = rw.rw_uint16(self.flags)
        self.ID = rw.rw_uint16(self.ID)
    
        if self.ID == 0:
            dtype = ToonShadingProperty
        elif self.ID == 1:
            dtype = Property1 # Inner glow
        elif self.ID == 2:
            dtype = OutlineProperty
        elif self.ID == 3:
            dtype = Property3
        elif self.ID == 4:
            dtype = Property4 # Texture Scrolling
        elif self.ID == 5:
            dtype = Property5
        elif self.ID == 6:
            dtype = Property6
        elif self.ID == 7:
            dtype = Property7
        else:
            raise NotImplementedError(f"Unrecognised Attribute ID: {self.ID}")
            
        if rw.mode() == "read":
            self.data = dtype()
        
        if type(self.data) is not dtype:
            raise ValueError(f"Unexpected Material Attribute type: expected '{dtype}', found '{type(self.data)}")
        rw.rw_obj(self.data)

class ToonShadingProperty(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        self.colour = None
        self.light_threshold  = None
        self.light_factor     = None
        self.light_brightness = None
        self.shadow_threshold = None
        self.shadow_factor    = None
        self.flags = None
        
    def read_write(self, rw):
        self.colour           = rw.rw_float32s(self.colour, 4)
        self.light_threshold  = rw.rw_float32(self.light_threshold)
        self.light_factor     = rw.rw_float32(self.light_factor)
        self.light_brightness = rw.rw_float32(self.light_brightness)
        self.shadow_threshold = rw.rw_float32(self.shadow_threshold)
        self.shadow_factor    = rw.rw_float32(self.shadow_factor)
        self.flags            = rw.rw_uint32(self.flags) # Flags are version-dependant
        
class Property1(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        self.flags = None
        
    def read_write(self, rw):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
        self.flags = rw.rw_uint32(self.flags)

class OutlineProperty(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type   = None
        self.colour = None
        
    def read_write(self, rw):
        self.type   = rw.rw_uint32(self.type)
        self.colour = rw.rw_uint32(self.colour)
                
class Property3(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        self.flags = None
        
    def read_write(self, rw):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
        self.flags = rw.rw_uint32(self.flags)        
        
class Property4(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        self.unknown_0x30 = None
        self.unknown_0x34 = None
        self.unknown_0x38 = None
        self.unknown_0x3C = None
        self.unknown_0x40 = None
        self.unknown_0x44 = None
        self.unknown_0x45 = None
        self.unknown_0x49 = None
        self.flags = None
        
    def read_write(self, rw):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
        self.unknown_0x30 = rw.rw_float32(self.unknown_0x30)
        self.unknown_0x34 = rw.rw_float32(self.unknown_0x34)
        self.unknown_0x38 = rw.rw_float32(self.unknown_0x38)
        self.unknown_0x3C = rw.rw_float32(self.unknown_0x3C)
        self.unknown_0x40 = rw.rw_float32(self.unknown_0x40)
        self.unknown_0x44 = rw.rw_uint8(self.unknown_0x44)
        self.unknown_0x45 = rw.rw_float32(self.unknown_0x45)
        self.unknown_0x49 = rw.rw_float32(self.unknown_0x49)
        self.flags = rw.rw_uint32(self.flags)
        
class Property5(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0C = None
        self.unknown_0x10 = None
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        self.unknown_0x28 = None
        self.unknown_0x2C = None
        self.unknown_0x30 = None
        self.flags = None
        
    def read_write(self, rw):
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
        self.unknown_0x30 = rw.rw_float32(self.unknown_0x30)
        self.flags = rw.rw_uint32(self.flags)
        
class Property6(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        
    def read_write(self, rw):
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)

class Property7(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
    def read_write(self, rw):
        pass
