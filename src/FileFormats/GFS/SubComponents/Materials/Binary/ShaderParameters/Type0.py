from ....CommonStructures import BitVector0x20


class ShaderParametersType0Flags(BitVector0x20):
    influenced_by_sky     = BitVector0x20.DEF_FLAG(0x05)
    transparency          = BitVector0x20.DEF_FLAG(0x06)
    multi_texture_mask    = BitVector0x20.DEF_FLAG(0x07)
    remove_diffuse_shadow = BitVector0x20.DEF_FLAG(0x08)
    billboard_shadow_map  = BitVector0x20.DEF_FLAG(0x09)


class ShaderParametersType0:
    def __init__(self):
        self.base_color        = [255,255,255,255]
        self.emissive_strength = 0
        self.roughness         = 0
        self.metallic          = 0
        self.multi_alpha       = 1
        self.bloom_intensity   = 1
        self.flags             = ShaderParametersType0Flags()
        self.unused_param      = 0
    
    def exbip_rw(self, rw, version):
        self.base_color = rw.rw_float32s(self.base_color, 4)
        self.emissive_strength = rw.rw_float32(self.emissive_strength)
        self.roughness         = rw.rw_float32(self.roughness)
        self.metallic          = rw.rw_float32(self.metallic)
        if version >= 0x02000004:
            self.multi_alpha = rw.rw_float32(self.multi_alpha)
        if version >= 0x02030001:
            self.bloom_intensity = rw.rw_float32(self.bloom_intensity)
        
        if version == 0x02110040:
            self.unused_param = rw.rw_float32(self.unused_param)
        elif version > 0x02110040:
            self.flags        = rw.rw_obj(self.flags)
    
    def tex2Name(self):
        return "Normal Map"
    
    def tex5Name(self):
        return "Multiply Map"
    
    def tex8Name(self):
        return "PBR Params Map" # Roughness, Metallic, Emissive, Intensity
