from ....CommonStructures import BitVector0x20


class ShaderParametersType4Flags(BitVector0x20):
    flowmap_multi_as_map               = BitVector0x20.DEF_FLAG(0x00)
    flowmap_rim_transparency           = BitVector0x20.DEF_FLAG(0x01)
    rim_trans_negate                   = BitVector0x20.DEF_FLAG(0x02)
    flowmap_bg_distortion              = BitVector0x20.DEF_FLAG(0x03)
    flowmap_multialpha_color_blend     = BitVector0x20.DEF_FLAG(0x04)
    flowmap_alpha_distortion           = BitVector0x20.DEF_FLAG(0x05)
    flowmap_alphamask_distortion       = BitVector0x20.DEF_FLAG(0x06)
    flowmap_apply_alpha_only           = BitVector0x20.DEF_FLAG(0x07)
    soft_particle                      = BitVector0x20.DEF_FLAG(0x08)
    force_bloom_intensity              = BitVector0x20.DEF_FLAG(0x09)
    fitting                            = BitVector0x20.DEF_FLAG(0x0A)
    flowmap_disable_color_correction   = BitVector0x20.DEF_FLAG(0x0B)
    multifitting                       = BitVector0x20.DEF_FLAG(0x0C)
    flowmap_multi_ref_alpha_base_color = BitVector0x20.DEF_FLAG(0x0D)
    flowmap_bloom_ref_alpha_multicolor = BitVector0x20.DEF_FLAG(0x0E)


class ShaderParametersType4:
    def __init__(self):
        self.base_color           = [1., 1., 1., 1.]
        self.emissive_color       = [1., 1., 1., 1.]
        self.distortion_power     = 0.
        self.distortion_threshold = 0.
        self.unknown_0x28         = 0.
        self.flags                = ShaderParametersType4Flags()
        self.bloom_intensity      = 0.5
        self.unknown_0x34         = 1.
        self.unknown_0x38         = 0.
        
    def exbip_rw(self, rw, version):
        self.base_color           = rw.rw_float32s(self.base_color, 4)
        self.emissive_color       = rw.rw_float32s(self.emissive_color, 4)
        self.distortion_power     = rw.rw_float32(self.distortion_power)
        self.distortion_threshold = rw.rw_float32(self.distortion_threshold)
        self.unknown_0x28         = rw.rw_float32(self.unknown_0x28)
        self.flags                = rw.rw_obj(self.flags)
        if version >= 0x02110184:
            self.bloom_intensity  = rw.rw_float32(self.bloom_intensity)
        if version >= 0x02110204:
            self.unknown_0x34     = rw.rw_float32(self.unknown_0x34)
        if version >= 0x02110218:
            self.unknown_0x38     = rw.rw_float32(self.unknown_0x38)

        def tex3Name(self):
            return "Dissolve Map"
        
        def tex5Name(self):
            return "Multiply Map"
        
        def tex6Name(self):
            return "Emissive Map"
        
        def tex7Name(self):
            return "Transparency Map"
        
        def tex8Name(self):
            return "Distortion Map"
        
        def tex9Name(self):
            return "Alpha Mask Map"
        
        def tex10Name(self):
            return "Alpha Map"
