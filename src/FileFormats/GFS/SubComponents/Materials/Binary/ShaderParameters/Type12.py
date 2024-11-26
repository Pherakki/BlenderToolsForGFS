from ....CommonStructures import BitVector0x20


class ShaderParametersType12Flags(BitVector0x20):
    pass


class ShaderParametersType12:
    def __init__(self):
        self.base_color     = [1., 1., 1., 1.]
        self.edge_color     = [1., 1., 1., 1.]
        self.emissive_color = [1., 1., 1., 1.]
        
        self.metallic                  = 0.
        self.edge_threshold            = 0.
        self.edge_factor               = 0.
        self.flags                     = ShaderParametersType12Flags()
        
        self.unknown_0x40              = 0.
        self.unknown_0x44              = [1., 1., 1.]
        
        self.unknown_0x50              = 0.
        self.edge_remove_y_axis_factor = 0.
        self.unknown_0x58              = 0.
        self.unknown_0x5C              = 0.
        
        self.unknown_0x60              = 0.
        self.unknown_0x64              = 0.
        self.specular_color            = [1., 1., 1.]
        self.specular_threshold        = 0.
        
        self.specular_power            = 0.
        self.roughness                 = 0.
        self.ramp_alpha                = 0.
        self.shadow_color              = [1., 1., 1., 1.]
        self.shadow_threshold          = 0.
        self.shadow_factor             = 0.
        
    def exbip_rw(self, rw, version):
        self.base_color                = rw.rw_float32s(self.base_color, 4)
        self.edge_color                = rw.rw_float32s(self.edge_color, 4)
        self.emissive_color            = rw.rw_float32s(self.emissive_color, 4)
        self.metallic                  = rw.rw_float32(self.metallic)
        self.edge_threshold            = rw.rw_float32(self.edge_threshold)
        self.edge_factor               = rw.rw_float32(self.edge_factor)
        self.flags                     = rw.rw_obj(self.flags)
        self.unknown_0x40              = rw.rw_float32(self.unknown_0x40)
        self.unknown_0x44              = rw.rw_float32s(self.unknown_0x44, 3)
        self.unknown_0x50              = rw.rw_float32(self.unknown_0x50)
        self.edge_remove_y_axis_factor = rw.rw_float32(self.edge_remove_y_axis_factor)
        
        if version > 0x02109500:
            self.unknown_0x58          = rw.rw_float32(self.unknown_0x58)
            self.unknown_0x5C          = rw.rw_float32(self.unknown_0x5C)
            self.unknown_0x60          = rw.rw_float32(self.unknown_0x60)
        if version > 0x02109600:
            self.unknown_0x64          = rw.rw_float32(self.unknown_0x64)
        if version > 0x02109700:
            self.specular_color        = rw.rw_float32s(self.specular_color, 3)
            self.specular_threshold    = rw.rw_float32(self.specular_threshold)
            self.specular_power        = rw.rw_float32(self.specular_power)
            self.roughness             = rw.rw_float32(self.roughness)
            self.ramp_alpha            = rw.rw_float32(self.ramp_alpha)
        if version > 0x02110070:
            self.shadow_color          = rw.rw_float32s(self.shadow_color, 4)
            self.shadow_threshold      = rw.rw_float32(self.shadow_threshold)
            self.shadow_factor         = rw.rw_float32(self.shadow_factor)

    def tex2Name(self):
        return "Normal Map"
    
    def tex3Name(self):
        return "Ramp Map"  # Presumably a CLUT
    
    def tex5Name(self):
        return "Multiply Map"
    
    def tex6Name(self):
        return "Toon Params 2 Map"
    
    def tex9Name(self):
        return "Toon Edge Color Map"
