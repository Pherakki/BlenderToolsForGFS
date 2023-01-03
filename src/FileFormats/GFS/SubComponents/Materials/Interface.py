from .Binary import MaterialBinary


class MaterialInterface:
    def __init__(self):
        
        # Flags
        self.flag_0            = None
        self.flag_1            = None
        self.flag_2            = None
        self.flag_3            = None
        self.use_vertex_colors = None
        self.flag_5            = None
        self.flag_6            = None
        self.use_light_1       = None
        self.flag_8            = None
        self.flag_9            = None
        self.flag_10           = None
        self.use_light_2       = None
        self.purple_wireframe  = None
        self.flag_13           = None
        self.receive_shadow    = None
        self.cast_shadow       = None
        self.flag_17           = None
        self.flag_18           = None
        self.disable_bloom     = None
        self.flag_29           = None
        self.flag_30           = None
        self.flag_31           = None
        
        # Presumably some of these can be removed...
        self.ambient = None
        self.diffuse = None
        self.specular = None
        self.emissive = None
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
    
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        
        instance.name = binary.name.string
        instance.flags = binary.flags
        # Can at least remove the flags for now
        instance.ambient = binary.ambient
        instance.diffuse = binary.diffuse
        instance.specular = binary.specular
        instance.emissive = binary.emissive
        instance.unknown_0x48 = binary.unknown_0x48
        instance.unknown_0x4C = binary.unknown_0x4C
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
        instance.unknown_0x60 = binary.unknown_0x60
        instance.unknown_0x64 = binary.unknown_0x64
        instance.disable_backface_culling = binary.disable_backface_culling
        instance.unknown_0x6A = binary.unknown_0x6A
        
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
        instance.flag_0            = binary.flags.flag_0
        instance.flag_1            = binary.flags.flag_1
        instance.flag_2            = binary.flags.flag_2
        instance.flag_3            = binary.flags.flag_3
        instance.use_vertex_colors = binary.flags.use_vertex_colors
        instance.flag_5            = binary.flags.flag_5
        instance.flag_6            = binary.flags.flag_6
        instance.use_light_1       = binary.flags.use_light_1
        instance.flag_8            = binary.flags.flag_8
        instance.flag_9            = binary.flags.flag_9
        instance.flag_10           = binary.flags.flag_10
        instance.use_light_2       = binary.flags.use_light_2
        instance.purple_wireframe  = binary.flags.purple_wireframe
        instance.flag_13           = binary.flags.flag_13
        instance.receive_shadow    = binary.flags.receive_shadow
        instance.cast_shadow       = binary.flags.cast_shadow
        instance.flag_17           = binary.flags.flag_17
        instance.flag_18           = binary.flags.flag_18
        instance.disable_bloom     = binary.flags.disable_bloom
        instance.flag_29           = binary.flags.flag_29
        instance.flag_30           = binary.flags.flag_30
        instance.flag_31           = binary.flags.flag_31
        
        return instance
    
    def to_binary(self):
        binary = MaterialBinary()
        
        binary.flags.flag_0                 = self.flag_0
        binary.flags.flag_1                 = self.flag_1
        binary.flags.flag_2                 = self.flag_2
        binary.flags.flag_3                 = self.flag_3
        binary.flags.use_vertex_colors      = self.use_vertex_colors
        binary.flags.flag_5                 = self.flag_5
        binary.flags.flag_6                 = self.flag_6
        binary.flags.use_light_1            = self.use_light_1
        binary.flags.flag_8                 = self.flag_8
        binary.flags.flag_9                 = self.flag_9
        binary.flags.flag_10                = self.flag_10
        binary.flags.use_light_2            = self.use_light_2
        binary.flags.purple_wireframe       = self.purple_wireframe
        binary.flags.flag_13                = self.flag_13
        binary.flags.receive_shadow         = self.receive_shadow
        binary.flags.cast_shadow            = self.cast_shadow
        binary.flags.has_attributes         = len(self.attributes) > 0
        binary.flags.flag_17                = self.flag_17
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
        
        binary.name                     = binary.name.from_name(self.name)
        binary.ambient                  = self.ambient
        binary.diffuse                  = self.diffuse
        binary.specular                 = self.specular
        binary.emissive                 = self.emissive
        binary.unknown_0x48             = self.unknown_0x48
        binary.unknown_0x4C             = self.unknown_0x4C
        binary.draw_method              = self.draw_method # 0 - opaque, 1 - translucent
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
        binary.unknown_0x60             = self.unknown_0x60
        binary.unknown_0x64             = self.unknown_0x64
        binary.disable_backface_culling = self.disable_backface_culling
        binary.unknown_0x6A             = self.unknown_0x6A
        
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
