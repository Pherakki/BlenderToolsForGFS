from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format
from ...CommonStructures import ObjectName, SizedObjArray, BitVector, BitVector0x10, BitVector0x20, BitChunkVector
from .TextureSampler import TextureSamplerBinary


class TextureMapIndices(BitChunkVector):
    MAXCHUNKS = 10
    CHUNKSIZE = 3
    MASK      = BitChunkVector.CALC_MASK(3)
    DEFAULT   = 0xFFFFFFFF
    
    diffuse    = BitChunkVector.DEF_CHUNK(0)
    normal     = BitChunkVector.DEF_CHUNK(1)
    specular   = BitChunkVector.DEF_CHUNK(2)
    reflection = BitChunkVector.DEF_CHUNK(3)
    highlight  = BitChunkVector.DEF_CHUNK(4)
    glow       = BitChunkVector.DEF_CHUNK(5)
    night      = BitChunkVector.DEF_CHUNK(6)
    detail     = BitChunkVector.DEF_CHUNK(7)
    shadow     = BitChunkVector.DEF_CHUNK(8)


class MaterialFlags(BitVector0x20):
    flag_0                 = BitVector.DEF_FLAG(0x00)
    flag_1                 = BitVector.DEF_FLAG(0x01)
    enable_specular        = BitVector.DEF_FLAG(0x02)
    flag_3                 = BitVector.DEF_FLAG(0x03) # Opaque Alpha?
    use_vertex_colors      = BitVector.DEF_FLAG(0x04)
    flag_5                 = BitVector.DEF_FLAG(0x05)
    flag_6                 = BitVector.DEF_FLAG(0x06)
    enable_uv_animation    = BitVector.DEF_FLAG(0x07)
    enable_emissive        = BitVector.DEF_FLAG(0x08)
    flag_9                 = BitVector.DEF_FLAG(0x09) # Some attribute?
    flag_10                = BitVector.DEF_FLAG(0x0A) # Unused?
    use_light_2            = BitVector.DEF_FLAG(0x0B)
    purple_wireframe       = BitVector.DEF_FLAG(0x0C)
    flag_13                = BitVector.DEF_FLAG(0x0D)
    receive_shadow         = BitVector.DEF_FLAG(0x0E)
    cast_shadow            = BitVector.DEF_FLAG(0x0F)
    has_attributes         = BitVector.DEF_FLAG(0x10)
    has_outline            = BitVector.DEF_FLAG(0x11)
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
        self.reflectivity = None
        self.outline_idx  = None
        self.draw_method  = None
        self.unknown_0x51 = None
        self.unknown_0x52 = None
        self.unknown_0x53 = None
        self.unknown_0x54 = None
        self.unknown_0x55 = None # Highlight map blend mode: 1 -> Normal, 2 -> dodge, 4 -> multiply
        self.unknown_0x56 = None
        self.unknown_0x58 = None
        self.unknown_0x5A = 1
        self.unknown_0x5C = None
        self.unknown_0x5E = None # 0, 2?
        self.texture_indices_1 = TextureMapIndices()
        self.texture_indices_2 = TextureMapIndices()
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
        return f"[GFD::Material] {self.name} "                                                     \
               f"{safe_format(self.flags._value, hex32_format)} "                                  \
               f"{safe_format(self.ambient, list)} {safe_format(self.diffuse, list)} "             \
               f"{safe_format(self.specular, list)} {safe_format(self.emissive, list)} "           \
               f"{self.reflectivity} {self.outline_idx} "                                          \
               f"{self.draw_method} {self.unknown_0x51} {self.unknown_0x52} {self.unknown_0x53} "  \
               f"{self.unknown_0x54} {self.unknown_0x55} {self.unknown_0x56} "                     \
               f"{self.unknown_0x58} {self.unknown_0x5A} {self.unknown_0x5C} {self.unknown_0x5E} " \
               f"{safe_format(self.texture_indices_1._value, hex32_format)} "                      \
               f"{safe_format(self.texture_indices_2._value, hex32_format)} "                      \
               f"{self.disable_backface_culling} {self.unknown_0x6A} {len(self.attributes)}"

    def read_write(self, rw, version):
        self.name         = rw.rw_obj(self.name, version)
        self.flags        = rw.rw_obj(self.flags)
        
        self.ambient      = rw.rw_float32s(self.ambient, 4)
        self.diffuse      = rw.rw_float32s(self.diffuse, 4)
        self.specular     = rw.rw_float32s(self.specular, 4)
        self.emissive     = rw.rw_float32s(self.emissive, 4)
        self.reflectivity = rw.rw_float32(self.reflectivity)
        self.outline_idx  = rw.rw_float32(self.outline_idx)
        
        if version < 0x01103040:
            self.draw_method  = rw.rw_uint16(self.draw_method)
            self.unknown_0x51 = rw.rw_uint16(self.unknown_0x51)
            self.unknown_0x52 = rw.rw_uint16(self.unknown_0x52)
            self.unknown_0x53 = rw.rw_uint16(self.unknown_0x53)
            self.unknown_0x54 = rw.rw_uint16(self.unknown_0x54)
            if version > 0x0108011B:
                self.unknown_0x55 = rw.rw_uint16(self.unknown_0x55)
        else:
            self.draw_method  = rw.rw_uint8(self.draw_method)
            self.unknown_0x51 = rw.rw_uint8(self.unknown_0x51)
            self.unknown_0x52 = rw.rw_uint8(self.unknown_0x52)
            self.unknown_0x53 = rw.rw_uint8(self.unknown_0x53)
            self.unknown_0x54 = rw.rw_uint8(self.unknown_0x54)
            self.unknown_0x55 = rw.rw_uint8(self.unknown_0x55)
            
        self.unknown_0x56 = rw.rw_uint16(self.unknown_0x56)
        self.unknown_0x58 = rw.rw_uint16(self.unknown_0x58)
        
        
        if version <= 0x01104800:
            self.unknown_0x5A = 1
            self.unknown_0x5C = rw.rw_int32(self.unknown_0x5C)
        else:
            self.unknown_0x5A = rw.rw_int16(self.unknown_0x5A) # 1 = Bloom, 0x0100 = Refl map something, 0x0002 = ???, 0x0004 = ???
            self.unknown_0x5C = rw.rw_int16(self.unknown_0x5C)
            
        self.unknown_0x5E = rw.rw_int16(self.unknown_0x5E)
        self.texture_indices_1 = rw.rw_obj(self.texture_indices_1)
        self.texture_indices_2 = rw.rw_obj(self.texture_indices_2)
        
        self.disable_backface_culling = rw.rw_int16(self.disable_backface_culling)
        self.unknown_0x6A = rw.rw_int32(self.unknown_0x6A)
        
        # Handle textures
        if self.flags.has_diffuse_texture:    self.diffuse_texture    = rw.rw_new_obj(self.diffuse_texture,    TextureSamplerBinary, version)
        if self.flags.has_normal_texture:     self.normal_texture     = rw.rw_new_obj(self.normal_texture,     TextureSamplerBinary, version)
        if self.flags.has_specular_texture:   self.specular_texture   = rw.rw_new_obj(self.specular_texture,   TextureSamplerBinary, version)
        if self.flags.has_reflection_texture: self.reflection_texture = rw.rw_new_obj(self.reflection_texture, TextureSamplerBinary, version)
        if self.flags.has_highlight_texture:  self.highlight_texture  = rw.rw_new_obj(self.highlight_texture,  TextureSamplerBinary, version)
        if self.flags.has_glow_texture:       self.glow_texture       = rw.rw_new_obj(self.glow_texture,       TextureSamplerBinary, version)
        if self.flags.has_night_texture:      self.night_texture      = rw.rw_new_obj(self.night_texture,      TextureSamplerBinary, version)
        if self.flags.has_detail_texture:     self.detail_texture     = rw.rw_new_obj(self.detail_texture,     TextureSamplerBinary, version)
        if self.flags.has_shadow_texture:     self.shadow_texture     = rw.rw_new_obj(self.shadow_texture,     TextureSamplerBinary, version)
            
        # Attributes
        if self.flags.has_attributes:
            rw.rw_obj(self.attributes, version)


class MaterialAttributeFlags(BitVector0x10):
    flag_0  = BitVector.DEF_FLAG(0x00)
    flag_1  = BitVector.DEF_FLAG(0x01)
    flag_2  = BitVector.DEF_FLAG(0x02)
    flag_3  = BitVector.DEF_FLAG(0x03)
    flag_4  = BitVector.DEF_FLAG(0x04)
    flag_5  = BitVector.DEF_FLAG(0x05)
    flag_6  = BitVector.DEF_FLAG(0x06)
    flag_7  = BitVector.DEF_FLAG(0x07)
    flag_8  = BitVector.DEF_FLAG(0x08)
    flag_9  = BitVector.DEF_FLAG(0x09)
    flag_10 = BitVector.DEF_FLAG(0x0A)
    flag_11 = BitVector.DEF_FLAG(0x0B)
    flag_12 = BitVector.DEF_FLAG(0x0C)
    flag_13 = BitVector.DEF_FLAG(0x0D)
    flag_14 = BitVector.DEF_FLAG(0x0E)
    flag_15 = BitVector.DEF_FLAG(0x0F)
    
    
class MaterialAttributeBinary(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = MaterialAttributeFlags(endianness)
        self.ID    = None
        self.data  = []
        
    def __repr__(self):
        return f"[GFD::Material::AttributeBinary] {safe_format(self.flags._value, hex32_format)} {self.ID}"
    
    def read_write(self, rw, version):
        self.flags = rw.rw_obj(self.flags)
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
        rw.rw_obj(self.data, version)


class MaterialAttributeSubTypeFlags(BitVector):
    MAXFLAGS = 0x20
    
    # Are the flags different for different versions?
    def read_write(self, rw, version):
        # RW different values depending on the version
        self._value = rw.rw_uint32(self._value)


class ToonShadingPropertyFlags(MaterialAttributeSubTypeFlags):
    flag_0  = BitVector.DEF_FLAG(0x00)
    flag_1  = BitVector.DEF_FLAG(0x01) # Something to do with outline attribute
    flag_2  = BitVector.DEF_FLAG(0x02)
    flag_3  = BitVector.DEF_FLAG(0x03)
    flag_4  = BitVector.DEF_FLAG(0x04)
    flag_5  = BitVector.DEF_FLAG(0x05) # Something to do with outline attribute
    flag_6  = BitVector.DEF_FLAG(0x06)
    flag_7  = BitVector.DEF_FLAG(0x07)
    flag_8  = BitVector.DEF_FLAG(0x08)
    flag_9  = BitVector.DEF_FLAG(0x09)
    flag_10 = BitVector.DEF_FLAG(0x0A)
    flag_11 = BitVector.DEF_FLAG(0x0B)
    flag_12 = BitVector.DEF_FLAG(0x0C)
    flag_13 = BitVector.DEF_FLAG(0x0D)
    flag_14 = BitVector.DEF_FLAG(0x0E)
    flag_15 = BitVector.DEF_FLAG(0x0F)
    flag_16 = BitVector.DEF_FLAG(0x10)
    flag_17 = BitVector.DEF_FLAG(0x11)
    flag_18 = BitVector.DEF_FLAG(0x12)
    flag_19 = BitVector.DEF_FLAG(0x13)
    flag_20 = BitVector.DEF_FLAG(0x14)
    flag_21 = BitVector.DEF_FLAG(0x15)
    flag_22 = BitVector.DEF_FLAG(0x16)
    flag_23 = BitVector.DEF_FLAG(0x17)
    flag_24 = BitVector.DEF_FLAG(0x18)
    flag_25 = BitVector.DEF_FLAG(0x19)
    flag_26 = BitVector.DEF_FLAG(0x1A)
    flag_27 = BitVector.DEF_FLAG(0x1B)
    flag_28 = BitVector.DEF_FLAG(0x1C)
    flag_29 = BitVector.DEF_FLAG(0x1D)
    flag_30 = BitVector.DEF_FLAG(0x1E)
    flag_31 = BitVector.DEF_FLAG(0x1F)


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
        self.flags            = ToonShadingPropertyFlags(endianness)
        
    def read_write(self, rw, version):
        self.colour           = rw.rw_float32s(self.colour, 4)
        self.light_threshold  = rw.rw_float32(self.light_threshold)
        self.light_factor     = rw.rw_float32(self.light_factor)
        self.light_brightness = rw.rw_float32(self.light_brightness)
        self.shadow_threshold = rw.rw_float32(self.shadow_threshold)
        self.shadow_factor    = rw.rw_float32(self.shadow_factor)
        self.flags            = rw.rw_obj(self.flags, version)
        

class Property1Flags(MaterialAttributeSubTypeFlags):
    flag_0  = BitVector.DEF_FLAG(0x00)
    flag_1  = BitVector.DEF_FLAG(0x01)
    flag_2  = BitVector.DEF_FLAG(0x02)
    flag_3  = BitVector.DEF_FLAG(0x03)
    flag_4  = BitVector.DEF_FLAG(0x04)
    flag_5  = BitVector.DEF_FLAG(0x05)
    flag_6  = BitVector.DEF_FLAG(0x06)
    flag_7  = BitVector.DEF_FLAG(0x07)
    flag_8  = BitVector.DEF_FLAG(0x08)
    flag_9  = BitVector.DEF_FLAG(0x09)
    flag_10 = BitVector.DEF_FLAG(0x0A)
    flag_11 = BitVector.DEF_FLAG(0x0B)
    flag_12 = BitVector.DEF_FLAG(0x0C)
    flag_13 = BitVector.DEF_FLAG(0x0D)
    flag_14 = BitVector.DEF_FLAG(0x0E)
    flag_15 = BitVector.DEF_FLAG(0x0F)
    flag_16 = BitVector.DEF_FLAG(0x10)
    flag_17 = BitVector.DEF_FLAG(0x11)
    flag_18 = BitVector.DEF_FLAG(0x12)
    flag_19 = BitVector.DEF_FLAG(0x13)
    flag_20 = BitVector.DEF_FLAG(0x14)
    flag_21 = BitVector.DEF_FLAG(0x15)
    flag_22 = BitVector.DEF_FLAG(0x16)
    flag_23 = BitVector.DEF_FLAG(0x17)
    flag_24 = BitVector.DEF_FLAG(0x18)
    flag_25 = BitVector.DEF_FLAG(0x19)
    flag_26 = BitVector.DEF_FLAG(0x1A)
    flag_27 = BitVector.DEF_FLAG(0x1B)
    flag_28 = BitVector.DEF_FLAG(0x1C)
    flag_29 = BitVector.DEF_FLAG(0x1D)
    flag_30 = BitVector.DEF_FLAG(0x1E)
    flag_31 = BitVector.DEF_FLAG(0x1F)


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
        self.flags        = Property1Flags(endianness)
        
    def read_write(self, rw, version):
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
        self.flags        = rw.rw_obj(self.flags, version)

class OutlineProperty(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type   = None
        self.colour = None
        
    def read_write(self, rw, version):
        self.type   = rw.rw_uint32(self.type)
        self.colour = rw.rw_uint32(self.colour)


class Property3Flags(MaterialAttributeSubTypeFlags):
    flag_0  = BitVector.DEF_FLAG(0x00)
    flag_1  = BitVector.DEF_FLAG(0x01)
    flag_2  = BitVector.DEF_FLAG(0x02)
    flag_3  = BitVector.DEF_FLAG(0x03)
    flag_4  = BitVector.DEF_FLAG(0x04)
    flag_5  = BitVector.DEF_FLAG(0x05)
    flag_6  = BitVector.DEF_FLAG(0x06)
    flag_7  = BitVector.DEF_FLAG(0x07)
    flag_8  = BitVector.DEF_FLAG(0x08)
    flag_9  = BitVector.DEF_FLAG(0x09)
    flag_10 = BitVector.DEF_FLAG(0x0A)
    flag_11 = BitVector.DEF_FLAG(0x0B)
    flag_12 = BitVector.DEF_FLAG(0x0C)
    flag_13 = BitVector.DEF_FLAG(0x0D)
    flag_14 = BitVector.DEF_FLAG(0x0E)
    flag_15 = BitVector.DEF_FLAG(0x0F)
    flag_16 = BitVector.DEF_FLAG(0x10)
    flag_17 = BitVector.DEF_FLAG(0x11)
    flag_18 = BitVector.DEF_FLAG(0x12)
    flag_19 = BitVector.DEF_FLAG(0x13)
    flag_20 = BitVector.DEF_FLAG(0x14)
    flag_21 = BitVector.DEF_FLAG(0x15)
    flag_22 = BitVector.DEF_FLAG(0x16)
    flag_23 = BitVector.DEF_FLAG(0x17)
    flag_24 = BitVector.DEF_FLAG(0x18)
    flag_25 = BitVector.DEF_FLAG(0x19)
    flag_26 = BitVector.DEF_FLAG(0x1A)
    flag_27 = BitVector.DEF_FLAG(0x1B)
    flag_28 = BitVector.DEF_FLAG(0x1C)
    flag_29 = BitVector.DEF_FLAG(0x1D)
    flag_30 = BitVector.DEF_FLAG(0x1E)
    flag_31 = BitVector.DEF_FLAG(0x1F)


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
        self.flags        = Property3Flags(endianness)
        
    def read_write(self, rw, version):
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
        self.flags        = rw.rw_obj(self.flags, version)
    

class Property4Flags(MaterialAttributeSubTypeFlags):
    flag_0  = BitVector.DEF_FLAG(0x00)
    flag_1  = BitVector.DEF_FLAG(0x01)
    flag_2  = BitVector.DEF_FLAG(0x02)
    flag_3  = BitVector.DEF_FLAG(0x03)
    flag_4  = BitVector.DEF_FLAG(0x04)
    flag_5  = BitVector.DEF_FLAG(0x05)
    flag_6  = BitVector.DEF_FLAG(0x06)
    flag_7  = BitVector.DEF_FLAG(0x07)
    flag_8  = BitVector.DEF_FLAG(0x08)
    flag_9  = BitVector.DEF_FLAG(0x09)
    flag_10 = BitVector.DEF_FLAG(0x0A)
    flag_11 = BitVector.DEF_FLAG(0x0B)
    flag_12 = BitVector.DEF_FLAG(0x0C)
    flag_13 = BitVector.DEF_FLAG(0x0D)
    flag_14 = BitVector.DEF_FLAG(0x0E)
    flag_15 = BitVector.DEF_FLAG(0x0F)
    flag_16 = BitVector.DEF_FLAG(0x10)
    flag_17 = BitVector.DEF_FLAG(0x11)
    flag_18 = BitVector.DEF_FLAG(0x12)
    flag_19 = BitVector.DEF_FLAG(0x13)
    flag_20 = BitVector.DEF_FLAG(0x14)
    flag_21 = BitVector.DEF_FLAG(0x15)
    flag_22 = BitVector.DEF_FLAG(0x16)
    flag_23 = BitVector.DEF_FLAG(0x17)
    flag_24 = BitVector.DEF_FLAG(0x18)
    flag_25 = BitVector.DEF_FLAG(0x19)
    flag_26 = BitVector.DEF_FLAG(0x1A)
    flag_27 = BitVector.DEF_FLAG(0x1B)
    flag_28 = BitVector.DEF_FLAG(0x1C)
    flag_29 = BitVector.DEF_FLAG(0x1D)
    flag_30 = BitVector.DEF_FLAG(0x1E)
    flag_31 = BitVector.DEF_FLAG(0x1F)
    
    
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
        self.flags        = Property4Flags(endianness)
        
    def read_write(self, rw, version):
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
        self.flags        = rw.rw_obj(self.flags, version)


class Property5Flags(MaterialAttributeSubTypeFlags):
    flag_0  = BitVector.DEF_FLAG(0x00)
    flag_1  = BitVector.DEF_FLAG(0x01)
    flag_2  = BitVector.DEF_FLAG(0x02)
    flag_3  = BitVector.DEF_FLAG(0x03)
    flag_4  = BitVector.DEF_FLAG(0x04)
    flag_5  = BitVector.DEF_FLAG(0x05)
    flag_6  = BitVector.DEF_FLAG(0x06)
    flag_7  = BitVector.DEF_FLAG(0x07)
    flag_8  = BitVector.DEF_FLAG(0x08)
    flag_9  = BitVector.DEF_FLAG(0x09)
    flag_10 = BitVector.DEF_FLAG(0x0A)
    flag_11 = BitVector.DEF_FLAG(0x0B)
    flag_12 = BitVector.DEF_FLAG(0x0C)
    flag_13 = BitVector.DEF_FLAG(0x0D)
    flag_14 = BitVector.DEF_FLAG(0x0E)
    flag_15 = BitVector.DEF_FLAG(0x0F)
    flag_16 = BitVector.DEF_FLAG(0x10)
    flag_17 = BitVector.DEF_FLAG(0x11)
    flag_18 = BitVector.DEF_FLAG(0x12)
    flag_19 = BitVector.DEF_FLAG(0x13)
    flag_20 = BitVector.DEF_FLAG(0x14)
    flag_21 = BitVector.DEF_FLAG(0x15)
    flag_22 = BitVector.DEF_FLAG(0x16)
    flag_23 = BitVector.DEF_FLAG(0x17)
    flag_24 = BitVector.DEF_FLAG(0x18)
    flag_25 = BitVector.DEF_FLAG(0x19)
    flag_26 = BitVector.DEF_FLAG(0x1A)
    flag_27 = BitVector.DEF_FLAG(0x1B)
    flag_28 = BitVector.DEF_FLAG(0x1C)
    flag_29 = BitVector.DEF_FLAG(0x1D)
    flag_30 = BitVector.DEF_FLAG(0x1E)
    flag_31 = BitVector.DEF_FLAG(0x1F)


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
        self.flags        = Property5Flags(endianness)
        
    def read_write(self, rw, version):
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
        self.flags        = rw.rw_obj(self.flags, version)
        
class Property6(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_uint32(self.unknown_0x08)

class Property7(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
    def read_write(self, rw, version):
        pass
