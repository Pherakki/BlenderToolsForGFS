from .Binary import MaterialBinary
from .Binary.TextureSampler import TextureSamplerBinary
from .Binary.MaterialBinary import MaterialAttributeBinary, TextureMapIndices
from .Binary.MaterialBinary import ToonShadingProperty
from .Binary.MaterialBinary import Property1
from .Binary.MaterialBinary import OutlineProperty
from .Binary.MaterialBinary import Property3
from .Binary.MaterialBinary import Property4
from .Binary.MaterialBinary import Property5
from .Binary.MaterialBinary import Property6
from .Binary.MaterialBinary import Property7


class MaterialInterface:
    def __init__(self):
        
        # Flags
        self.flag_0              = None
        self.flag_1              = None
        self.enable_specular     = None
        self.flag_3              = None
        self.use_vertex_colors   = None
        self.flag_5              = None
        self.flag_6              = None
        self.enable_uv_animation = None
        self.enable_emissive     = None
        self.flag_9              = None
        self.flag_10             = None
        self.use_light_2         = None
        self.purple_wireframe    = None
        self.flag_13             = None
        self.receive_shadow      = None
        self.cast_shadow         = None
        self.flag_18             = None
        self.disable_bloom       = None
        self.flag_29             = None
        self.flag_30             = None
        self.flag_31             = None
        
        # Presumably some of these can be removed...
        self.name_bytes    = None
        # self.ambient      = None
        # self.diffuse      = None
        # self.specular     = None
        # self.emissive     = None
        # self.reflectivity = None
        # self.outline_idx  = None
        self.params_type   = None
        self.shader_params = None
        self.draw_method  = None
        self.unknown_0x51 = None
        self.unknown_0x52 = None
        self.unknown_0x53 = None
        self.unknown_0x54 = None
        self.unknown_0x55 = None
        self.unknown_0x56 = None
        self.unknown_0x58 = None
        self.unknown_0x5A = 1
        self.unknown_0x5C = None
        self.unknown_0x5E = None
        self.texture_indices_1 = TextureMapIndices()
        self.texture_indices_2 = TextureMapIndices() # Change later...
        self.disable_backface_culling = None
        self.unknown_0x6A = None
        self.unknown_0x6C = None
        
        # Need to come up with a better way of assigning the extra data to these
        self.diffuse_texture    = None
        self.normal_texture     = None
        self.specular_texture   = None
        self.reflection_texture = None
        self.highlight_texture  = None
        self.glow_texture       = None
        self.night_texture      = None
        self.detail_texture     = None
        self.shadow_texture     = None
        
        self.attributes = []
    
    @property
    def name(self):
        return self.name_bytes.decode('utf8')
    @name.setter
    def name(self, value):
        self.name_bytes = value.encode('utf8')
    
    @property
    def name_safe(self):
        return self.name_bytes.decode('utf8', errors='replace')
    @name_safe.setter
    def name_safe(self, value):
        self.name_bytes = value.encode('utf8', errors='replace')
        
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        
        instance.name_bytes = binary.name.string
        instance.params_type   = binary.params_type
        instance.shader_params = binary.shader_params
        
        instance.draw_method  = binary.draw_method
        instance.unknown_0x51 = binary.unknown_0x51
        instance.unknown_0x52 = binary.unknown_0x52
        instance.unknown_0x53 = binary.unknown_0x53
        instance.unknown_0x54 = binary.unknown_0x54
        instance.unknown_0x55 = binary.unknown_0x55
        instance.unknown_0x56 = binary.unknown_0x56
        instance.unknown_0x58 = binary.unknown_0x58
        instance.unknown_0x5A = binary.unknown_0x5A
        instance.unknown_0x5C = binary.unknown_0x5C
        instance.unknown_0x5E = binary.unknown_0x5E
        instance.texture_indices_1 = binary.texture_indices_1
        instance.texture_indices_2 = binary.texture_indices_2
        instance.disable_backface_culling = binary.disable_backface_culling
        instance.unknown_0x6A = binary.unknown_0x6A
        instance.unknown_0x6C = binary.unknown_0x6C
        
        # Need to come up with a better way of assigning the extra data to these
        # Since it's unclear what this extra data does... leave it for now
        instance.diffuse_texture    = binary.diffuse_texture
        instance.normal_texture     = binary.normal_texture
        instance.specular_texture   = binary.specular_texture
        instance.reflection_texture = binary.reflection_texture
        instance.highlight_texture  = binary.highlight_texture
        instance.glow_texture       = binary.glow_texture
        instance.night_texture      = binary.night_texture
        instance.detail_texture     = binary.detail_texture
        instance.shadow_texture     = binary.shadow_texture
        
        # Attributes
        instance.attributes = binary.attributes.data
        
        # Deal with other flags
        instance.flag_0              = binary.flags.flag_0
        instance.flag_1              = binary.flags.flag_1
        instance.enable_specular     = binary.flags.enable_specular
        instance.flag_3              = binary.flags.flag_3
        instance.use_vertex_colors   = binary.flags.use_vertex_colors
        instance.flag_5              = binary.flags.flag_5
        instance.flag_6              = binary.flags.flag_6
        instance.enable_uv_animation = binary.flags.enable_uv_animation
        instance.enable_emissive     = binary.flags.enable_emissive
        instance.flag_9              = binary.flags.flag_9
        instance.flag_10             = binary.flags.flag_10
        instance.use_light_2         = binary.flags.use_light_2
        instance.purple_wireframe    = binary.flags.purple_wireframe
        instance.flag_13             = binary.flags.flag_13
        instance.receive_shadow      = binary.flags.receive_shadow
        instance.cast_shadow         = binary.flags.cast_shadow
        instance.flag_18             = binary.flags.flag_18
        instance.disable_bloom       = binary.flags.disable_bloom
        instance.flag_29             = binary.flags.flag_29
        instance.flag_30             = binary.flags.flag_30
        instance.flag_31             = binary.flags.flag_31
        
        return instance
    
    def to_binary(self):
        binary = MaterialBinary()
        
        binary.flags.flag_0                 = self.flag_0
        binary.flags.flag_1                 = self.flag_1
        binary.flags.enable_specular        = self.enable_specular
        binary.flags.flag_3                 = self.flag_3
        binary.flags.use_vertex_colors      = self.use_vertex_colors
        binary.flags.flag_5                 = self.flag_5
        binary.flags.flag_6                 = self.flag_6
        binary.flags.enable_uv_animation    = self.enable_uv_animation
        binary.flags.enable_emissive        = self.enable_emissive
        binary.flags.flag_9                 = self.flag_9
        binary.flags.flag_10                = self.flag_10
        binary.flags.use_light_2            = self.use_light_2
        binary.flags.purple_wireframe       = self.purple_wireframe
        binary.flags.flag_13                = self.flag_13
        binary.flags.receive_shadow         = self.receive_shadow
        binary.flags.cast_shadow            = self.cast_shadow
        binary.flags.has_attributes         = len(self.attributes) > 0
        binary.flags.has_outline            = any([a.ID == 2 for a in self.attributes])
        binary.flags.flag_18                = self.flag_18
        binary.flags.disable_bloom          = self.disable_bloom
        binary.flags.has_diffuse_texture    = self.diffuse_texture    is not None
        binary.flags.has_normal_texture     = self.normal_texture     is not None
        binary.flags.has_specular_texture   = self.specular_texture   is not None
        binary.flags.has_reflection_texture = self.reflection_texture is not None
        binary.flags.has_highlight_texture  = self.highlight_texture  is not None
        binary.flags.has_glow_texture       = self.glow_texture       is not None
        binary.flags.has_night_texture      = self.night_texture      is not None
        binary.flags.has_detail_texture     = self.detail_texture     is not None
        binary.flags.has_shadow_texture     = self.shadow_texture     is not None
        binary.flags.flag_29                = self.flag_29
        binary.flags.flag_30                = self.flag_30
        binary.flags.flag_31                = self.flag_31
        
        binary.name                     = binary.name.from_bytestring(self.name_bytes)
        binary.params_type              = self.params_type
        binary.shader_params            = self.shader_params
        binary.draw_method              = self.draw_method
        binary.unknown_0x51             = self.unknown_0x51
        binary.unknown_0x52             = self.unknown_0x52
        binary.unknown_0x53             = self.unknown_0x53
        binary.unknown_0x54             = self.unknown_0x54
        binary.unknown_0x55             = self.unknown_0x55
        binary.unknown_0x56             = self.unknown_0x56
        binary.unknown_0x58             = self.unknown_0x58
        binary.unknown_0x5A             = self.unknown_0x5A
        binary.unknown_0x5C             = self.unknown_0x5C
        binary.unknown_0x5E             = self.unknown_0x5E
        binary.texture_indices_1        = self.texture_indices_1
        binary.texture_indices_2        = self.texture_indices_2
        binary.disable_backface_culling = self.disable_backface_culling
        binary.unknown_0x6A             = self.unknown_0x6A
        binary.unknown_0x6C             = self.unknown_0x6C
        
        binary.diffuse_texture    = self.diffuse_texture
        binary.normal_texture     = self.normal_texture
        binary.specular_texture   = self.specular_texture
        binary.reflection_texture = self.reflection_texture
        binary.highlight_texture  = self.highlight_texture
        binary.glow_texture       = self.glow_texture
        binary.night_texture      = self.night_texture
        binary.detail_texture     = self.detail_texture
        binary.shadow_texture     = self.shadow_texture
        
        binary.attributes.data = self.attributes
        binary.attributes.count = len(self.attributes)
        
        return binary
    
    def _make_texture_sampler(self, name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C):
        ts = TextureSamplerBinary()
        
        ts.name = ts.name.from_name(name, encoding="shift-jis")
        ts.unknown_0x04          = unknown_0x04
        ts.unknown_0x08          = unknown_0x08
        ts.has_texture_filtering = has_texture_filtering
        ts.wrap_mode_u           = wrap_mode_u
        ts.wrap_mode_v           = wrap_mode_v
        ts.unknown_0x0C          = unknown_0x0C
        
        return ts
    
    def set_diffuse_texture(self, tex_idx_1, tex_idx_2, name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C):
        self.texture_indices_1.diffuse = tex_idx_1
        self.texture_indices_2.diffuse = tex_idx_2
        self.diffuse_texture = self._make_texture_sampler(name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C)
    
    def set_normal_texture(self, tex_idx_1, tex_idx_2, name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C):
        self.texture_indices_1.normal = tex_idx_1
        self.texture_indices_2.normal = tex_idx_2
        self.normal_texture = self._make_texture_sampler(name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C)
    
    def set_specular_texture(self, tex_idx_1, tex_idx_2, name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C):
        self.texture_indices_1.specular = tex_idx_1
        self.texture_indices_2.specular = tex_idx_2
        self.specular_texture = self._make_texture_sampler(name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C)
    
    def set_reflection_texture(self, tex_idx_1, tex_idx_2, name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C):
        self.texture_indices_1.reflection = tex_idx_1
        self.texture_indices_2.reflection = tex_idx_2
        self.reflection_texture = self._make_texture_sampler(name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C)
    
    def set_highlight_texture(self, tex_idx_1, tex_idx_2, name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C):
        self.texture_indices_1.highlight = tex_idx_1
        self.texture_indices_2.highlight = tex_idx_2
        self.highlight_texture = self._make_texture_sampler(name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C)
    
    def set_glow_texture(self, tex_idx_1, tex_idx_2, name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C):
        self.texture_indices_1.glow = tex_idx_1
        self.texture_indices_2.glow = tex_idx_2
        self.glow_texture = self._make_texture_sampler(name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C)
    
    def set_night_texture(self, tex_idx_1, tex_idx_2, name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C):
        self.texture_indices_1.night = tex_idx_1
        self.texture_indices_2.night = tex_idx_2
        self.night_texture = self._make_texture_sampler(name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C)
    
    def set_detail_texture(self, tex_idx_1, tex_idx_2, name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C):
        self.texture_indices_1.detail = tex_idx_1
        self.texture_indices_2.detail = tex_idx_2
        self.detail_texture = self._make_texture_sampler(name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C)
    
    def set_shadow_texture(self, tex_idx_1, tex_idx_2, name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C):
        self.texture_indices_1.shadow = tex_idx_1
        self.texture_indices_2.shadow = tex_idx_2
        self.shadow_texture = self._make_texture_sampler(name, unknown_0x04, unknown_0x08, has_texture_filtering, wrap_mode_u, wrap_mode_v, unknown_0x0C)

    def add_toon_shading_attribute(self, colour, light_threshold, light_factor, light_brightness, shadow_threshold, shadow_factor):
        attr = MaterialAttributeBinary()
        attr.ID = 0
        attr.data = ToonShadingProperty()
        
        attr.data.colour           = colour
        attr.data.light_threshold  = light_threshold
        attr.data.light_factor     = light_factor
        attr.data.light_brightness = light_brightness
        attr.data.shadow_threshold = shadow_threshold
        attr.data.shadow_factor    = shadow_factor
        
        self.attributes.append(attr)
        return attr


    def add_attribute_1(self, unknown_0x00, unknown_0x04, unknown_0x08, unknown_0x0C, 
                              unknown_0x10, unknown_0x14, unknown_0x18, unknown_0x1C,
                              unknown_0x20, unknown_0x24, unknown_0x28, unknown_0x2C):
        attr = MaterialAttributeBinary()
        attr.ID = 1
        attr.data = Property1()
        
        attr.data.unknown_0x00 = unknown_0x00
        attr.data.unknown_0x04 = unknown_0x04
        attr.data.unknown_0x08 = unknown_0x08
        attr.data.unknown_0x0C = unknown_0x0C
        attr.data.unknown_0x10 = unknown_0x10
        attr.data.unknown_0x14 = unknown_0x14
        attr.data.unknown_0x18 = unknown_0x18
        attr.data.unknown_0x1C = unknown_0x1C
        attr.data.unknown_0x20 = unknown_0x20
        attr.data.unknown_0x24 = unknown_0x24
        attr.data.unknown_0x28 = unknown_0x28
        attr.data.unknown_0x2C = unknown_0x2C
        
        self.attributes.append(attr)
        return attr
    
    def add_outline_attribute(self, type, colour):
        attr = MaterialAttributeBinary()
        attr.ID = 2
        attr.data = OutlineProperty()
        
        attr.data.type   = type
        attr.data.colour = colour
        
        self.attributes.append(attr)
        return attr
    
    def add_attribute_3(self, unknown_0x00, unknown_0x04, unknown_0x08, unknown_0x0C, 
                              unknown_0x10, unknown_0x14, unknown_0x18, unknown_0x1C,
                              unknown_0x20, unknown_0x24, unknown_0x28, unknown_0x2C):
        attr = MaterialAttributeBinary()
        attr.ID = 3
        attr.data = Property3()
        
        attr.data.unknown_0x00 = unknown_0x00
        attr.data.unknown_0x04 = unknown_0x04
        attr.data.unknown_0x08 = unknown_0x08
        attr.data.unknown_0x0C = unknown_0x0C
        attr.data.unknown_0x10 = unknown_0x10
        attr.data.unknown_0x14 = unknown_0x14
        attr.data.unknown_0x18 = unknown_0x18
        attr.data.unknown_0x1C = unknown_0x1C
        attr.data.unknown_0x20 = unknown_0x20
        attr.data.unknown_0x24 = unknown_0x24
        attr.data.unknown_0x28 = unknown_0x28
        attr.data.unknown_0x2C = unknown_0x2C
        
        self.attributes.append(attr)
        return attr    

    def add_attribute_4(self, unknown_0x00, unknown_0x04, unknown_0x08, unknown_0x0C, 
                              unknown_0x10, unknown_0x14, unknown_0x18, unknown_0x1C,
                              unknown_0x20, unknown_0x24, unknown_0x28, unknown_0x2C,
                              unknown_0x30, unknown_0x34, unknown_0x38, unknown_0x3C,
                              unknown_0x40, unknown_0x44, unknown_0x45, unknown_0x49):
        attr = MaterialAttributeBinary()
        attr.ID = 4
        attr.data = Property4()
        
        attr.data.unknown_0x00 = unknown_0x00
        attr.data.unknown_0x04 = unknown_0x04
        attr.data.unknown_0x08 = unknown_0x08
        attr.data.unknown_0x0C = unknown_0x0C
        attr.data.unknown_0x10 = unknown_0x10
        attr.data.unknown_0x14 = unknown_0x14
        attr.data.unknown_0x18 = unknown_0x18
        attr.data.unknown_0x1C = unknown_0x1C
        attr.data.unknown_0x20 = unknown_0x20
        attr.data.unknown_0x24 = unknown_0x24
        attr.data.unknown_0x28 = unknown_0x28
        attr.data.unknown_0x2C = unknown_0x2C
        attr.data.unknown_0x30 = unknown_0x30
        attr.data.unknown_0x34 = unknown_0x34
        attr.data.unknown_0x38 = unknown_0x38
        attr.data.unknown_0x3C = unknown_0x3C
        attr.data.unknown_0x40 = unknown_0x40
        attr.data.unknown_0x44 = unknown_0x44
        attr.data.unknown_0x45 = unknown_0x45
        attr.data.unknown_0x49 = unknown_0x49
        
        self.attributes.append(attr)
        return attr
    

    def add_attribute_5(self, unknown_0x00, unknown_0x04, unknown_0x08, unknown_0x0C, 
                              unknown_0x10, unknown_0x14, unknown_0x18, unknown_0x1C,
                              unknown_0x20, unknown_0x24, unknown_0x28, unknown_0x2C,
                              unknown_0x30                                           ):
        attr = MaterialAttributeBinary()
        attr.ID = 5
        attr.data = Property5()
        
        attr.data.unknown_0x00 = unknown_0x00
        attr.data.unknown_0x04 = unknown_0x04
        attr.data.unknown_0x08 = unknown_0x08
        attr.data.unknown_0x0C = unknown_0x0C
        attr.data.unknown_0x10 = unknown_0x10
        attr.data.unknown_0x14 = unknown_0x14
        attr.data.unknown_0x18 = unknown_0x18
        attr.data.unknown_0x1C = unknown_0x1C
        attr.data.unknown_0x20 = unknown_0x20
        attr.data.unknown_0x24 = unknown_0x24
        attr.data.unknown_0x28 = unknown_0x28
        attr.data.unknown_0x2C = unknown_0x2C
        attr.data.unknown_0x30 = unknown_0x30
        
        self.attributes.append(attr)
        return attr
    
    def add_attribute_6(self, unknown_0x00, unknown_0x04, unknown_0x08):
        attr = MaterialAttributeBinary()
        attr.ID = 6
        attr.data = Property6()
        
        attr.data.unknown_0x00 = unknown_0x00
        attr.data.unknown_0x04 = unknown_0x04
        attr.data.unknown_0x08 = unknown_0x08
        
        self.attributes.append(attr)
        return attr
    
    def add_attribute_7(self):
        attr = MaterialAttributeBinary()
        attr.ID = 7
        attr.data = Property7()
        
        self.attributes.append(attr)
        return attr
