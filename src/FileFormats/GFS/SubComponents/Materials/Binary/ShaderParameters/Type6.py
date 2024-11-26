from ....CommonStructures import BitVector0x20


class ShaderParametersType6Flags(BitVector0x20):
    pass


class ShaderParametersType6:
    def __init__(self):
        self.base_color              = [1., 1., 1., 1.]
        self.emissive                = 0.
        self.roughness               = 0.
        self.bloom_intensity         = 0.
        self.unknown                 = 0.
        
        self.overlay_base_color      = [1., 1., 1., 1.]
        self.overlay_emissive        = 0.
        self.overlay_roughness       = 0.
        self.overlay_bloom_intensity = 0.
        self.overlay_unknown         = 0.
        
        self.unknown_0x40            = 0.
        self.unknown_0x44            = 0.
        self.unknown_0x48            = 0.
        self.unknown_0x4C            = 0.
        
        self.flags                   = ShaderParametersType6Flags()
        
    
    def exbip_rw(self, rw, version):
        self.base_color              = rw.rw_float32s(self.base_color, 4)
        self.emissive                = rw.rw_float32(self.emissive)
        self.roughness               = rw.rw_float32(self.roughness)
        self.bloom_intensity         = rw.rw_float32(self.bloom_intensity)
        self.unknown                 = rw.rw_float32(self.unknown)
        
        self.overlay_base_color      = rw.rw_float32s(self.overlay_base_color, 4)
        self.overlay_emissive        = rw.rw_float32(self.overlay_emissive)
        self.overlay_roughness       = rw.rw_float32(self.overlay_roughness)
        self.overlay_bloom_intensity = rw.rw_float32(self.overlay_bloom_intensity)
        self.overlay_unknown         = rw.rw_float32(self.overlay_unknown)
        
        self.unknown_0x40            = rw.rw_float32(self.unknown_0x40)
        if version >= 0x02110021:
            self.unknown_0x44        = rw.rw_float32(self.unknown_0x44)
            self.unknown_0x48        = rw.rw_float32(self.unknown_0x48)
        self.unknown_0x4C            = rw.rw_float32(self.unknown_0x4C)
        
        self.flags = rw.rw_obj(self.flags)
        
    def tex1Name(self):
        return "Base Map"
    
    def tex2Name(self):
        return "Normal Map"
    
    def tex5Name(self):
        return "Blend Map"
    
    def tex6Name(self):
        return "PBR Params Map"
    
    def tex7Name(self):
        return "Overlay Base Map"
    
    def tex8Name(self):
        return "Overlay Normal Map"
    
    def tex9Name(self):
        return "Overlay PBR Params Map"
