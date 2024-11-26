from ....CommonStructures import BitVector0x20


class ShaderParametersType2Flags(BitVector0x20):
    pass


class ShaderParametersType2:
    def __init__(self):
        self.base_color         = [1.,1.,1.,1.]
        self.shadow_color       = [1.,1.,1.,1.]
        self.edge_color         = [1.,1.,1.,1.]
        self.emissive_color     = [1.,1.,1.,1.]
        self.specular_color     = [1.,1.,1.]
        
        self.specular_power     = 0
        self.metallic           = 0
        self.edge_threshold     = 0
        self.edge_factor        = 0
        
        self.shadow_threshold   = 0
        self.shadow_factor      = 0
        self.flags              = ShaderParametersType2Flags()
        self.unknown_0x6C       = 0
        
        self.unknown_0x70       = [0,0,0]
        self.bloom_intensity    = 0.5
        
        self.specular_threshold = 0.5
        self.edge_remove_y_axis_factor = 3
        self.unknown_0x78       = 1
        self.unknown_0x7C       = -1
        
        self.unknown_0x80       = 0
        self.unknown_0x84       = 0.1
        self.roughness          = 0
        self.fitting_tile       = 0
        self.multi_fitting_tile = 0
        
        
    def exbip_rw(self, rw, version):
        self.base_color       = rw.rw_float32s(self.base_color,     4)
        self.shadow_color     = rw.rw_float32s(self.shadow_color,   4)
        self.edge_color       = rw.rw_float32s(self.edge_color,     4)
        self.emissive_color   = rw.rw_float32s(self.emissive_color, 4)
        self.specular_color   = rw.rw_float32s(self.specular_color, 3)
        
        self.specular_power   = rw.rw_float32(self.specular_power)
        self.metallic         = rw.rw_float32(self.metallic)
        self.edge_threshold   = rw.rw_float32(self.edge_threshold)
        self.edge_factor      = rw.rw_float32(self.edge_factor)
        
        self.shadow_threshold = rw.rw_float32(self.shadow_threshold)
        self.shadow_factor    = rw.rw_float32(self.shadow_factor)
        self.flags            = rw.rw_obj(self.flags)
        if version >= 0x02010000:
            self.unknown_0x6C = rw.rw_float32(self.unknown_0x6C)
            self.unknown_0x70 = rw.rw_float32s(self.unknown_0x70, 3)

        if version >= 0x02030001:
            self.bloom_intensity    = rw.rw_float32(self.bloom_intensity)
        if version >= 0x02090000:
            self.specular_threshold = rw.rw_float32(self.specular_threshold)    
        if version >= 0x02094001:
            self.edge_remove_y_axis_factor = rw.rw_float32(self.edge_remove_y_axis_factor)
        if version >= 0x02109501:
            self.unknown_0x78       = rw.rw_float32(self.unknown_0x78)
            self.unknown_0x7C       = rw.rw_float32(self.unknown_0x7C)
            self.unknown_0x80       = rw.rw_float32(self.unknown_0x80)
        if version >= 0x02109601:
            self.unknown_0x84       = rw.rw_float32(self.unknown_0x84)
        if version >= 0x02110198:
            self.roughness          = rw.rw_float32(self.roughness)
        if version >= 0x02110204:
            self.fitting_tile       = rw.rw_float32(self.fitting_tile)
        if version >= 0x02110210:
            self.multi_fitting_tile = rw.rw_float32(self.multi_fitting_tile)
  
    def tex2Name(self):
        return "Normal Map"

    def tex3Name(self):
        return "Toon Shadow Color Map"
    
    def tex5Name(self):
        return "Multiply Map"
    
    def tex6Name(self):
        return "Toon Params 2 Map"
    
    def tex8Name(self):
        return "Toon Params Map"
    
    def tex9Name(self):
        return "Toon Edge Color Map"
