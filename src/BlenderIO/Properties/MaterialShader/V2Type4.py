import bpy
from ....FileFormats.GFS.SubComponents.Materials.Binary.ShaderParameters.Type4 import ShaderParametersType4, ShaderParametersType4Flags
from .Utils import copy_list


class V2Type4Support:
    def from_V2_type4_params(self, params):
        self.type4_flags.from_flags(params.flags)
        copy_list(self.base_color, params.base_color, 4)
        copy_list(self.emissive_color, params.emissive_color, 4)
        self.distortion_power     = params.distortion_power
        self.distortion_threshold = params.distortion_threshold
        self.type4_unknown_0x28   = params.unknown_0x28
        self.bloom_intensity      = params.bloom_intensity
        self.type4_unknown_0x34   = params.unknown_0x34
        self.type4_unknown_0x38   = params.unknown_0x38
    
    def to_V2_type4_params(self):
        params = ShaderParametersType4()
        params.base_color           = self.base_color
        params.emissive_color       = self.emissive_color
        params.distortion_power     = self.distortion_power
        params.distortion_threshold = self.distortion_threshold
        params.unknown_0x28         = self.type4_unknown_0x28
        params.bloom_intensity      = self.bloom_intensity
        params.flags                = self.type4_flags.to_flags()
        params.unknown_0x34         = self.type4_unknown_0x34
        params.unknown_0x38         = self.type4_unknown_0x38
        return params

    def draw_V2_type4_params(self, layout):
        self.type4_flags.draw(layout)
        layout.prop(self, "base_color")
        layout.prop(self, "emissive_color")
        layout.prop(self, "distortion_power")
        layout.prop(self, "distortion_threshold")
        layout.prop(self, "type4_unknown_0x28")
        layout.prop(self, "bloom_intensity")
        layout.prop(self, "type4_unknown_0x34")
        layout.prop(self, "type4_unknown_0x38")


class Type4Flags(bpy.types.PropertyGroup):
    flowmap_multi_as_map:               bpy.props.BoolProperty(name="Flowmap Multi As Map")
    flowmap_rim_transparency:           bpy.props.BoolProperty(name="Flowmap Rim Transparency")
    rim_trans_negate:                   bpy.props.BoolProperty(name="Rim Trans Negate")
    flowmap_bg_distortion:              bpy.props.BoolProperty(name="Flowmap BG Distortion")
    flowmap_multialpha_color_blend:     bpy.props.BoolProperty(name="Flowmap Multialpha Color Blend")
    flowmap_alpha_distortion:           bpy.props.BoolProperty(name="Flowmap Alpha Distortion")
    flowmap_alphamask_distortion:       bpy.props.BoolProperty(name="Flowmap Alphamask Distortion")
    flowmap_apply_alpha_only:           bpy.props.BoolProperty(name="Flowmap Apply Alpha Only")
    soft_particle:                      bpy.props.BoolProperty(name="Soft Particle")
    force_bloom_intensity:              bpy.props.BoolProperty(name="Force Bloom Intensity")
    fitting:                            bpy.props.BoolProperty(name="Fitting")
    flowmap_disable_color_correction:   bpy.props.BoolProperty(name="Flowmap Disable Color Correction")
    multifitting:                       bpy.props.BoolProperty(name="Multifitting")
    flowmap_multi_ref_alpha_base_color: bpy.props.BoolProperty(name="Flowmap Multi Ref Alpha Base Color")
    flowmap_bloom_ref_alpha_multicolor: bpy.props.BoolProperty(name="Flowmap Bloom Ref Alpha Multicolor")
    flag_15: bpy.props.BoolProperty(name="Flag 15")
    flag_16: bpy.props.BoolProperty(name="Flag 16")
    flag_17: bpy.props.BoolProperty(name="Flag 17")
    flag_18: bpy.props.BoolProperty(name="Flag 18")
    flag_19: bpy.props.BoolProperty(name="Flag 19")
    flag_20: bpy.props.BoolProperty(name="Flag 20")
    flag_21: bpy.props.BoolProperty(name="Flag 21")
    flag_22: bpy.props.BoolProperty(name="Flag 22")
    flag_23: bpy.props.BoolProperty(name="Flag 23")
    flag_24: bpy.props.BoolProperty(name="Flag 24")
    flag_25: bpy.props.BoolProperty(name="Flag 25")
    flag_26: bpy.props.BoolProperty(name="Flag 26")
    flag_27: bpy.props.BoolProperty(name="Flag 27")
    flag_28: bpy.props.BoolProperty(name="Flag 28")
    flag_29: bpy.props.BoolProperty(name="Flag 29")
    flag_30: bpy.props.BoolProperty(name="Flag 30")
    flag_31: bpy.props.BoolProperty(name="Flag 31")

    def from_flags(self, flags):
        self.flowmap_multi_as_map               = flags.flowmap_multi_as_map
        self.flowmap_rim_transparency           = flags.flowmap_rim_transparency
        self.rim_trans_negate                   = flags.rim_trans_negate
        self.flowmap_bg_distortion              = flags.flowmap_bg_distortion
        self.flowmap_multialpha_color_blend     = flags.flowmap_multialpha_color_blend
        self.flowmap_alpha_distortion           = flags.flowmap_alpha_distortion
        self.flowmap_alphamask_distortion       = flags.flowmap_alphamask_distortion
        self.flowmap_apply_alpha_only           = flags.flowmap_apply_alpha_only
        self.soft_particle                      = flags.soft_particle
        self.force_bloom_intensity              = flags.force_bloom_intensity
        self.fitting                            = flags.fitting
        self.flowmap_disable_color_correction   = flags.flowmap_disable_color_correction
        self.multifitting                       = flags.multifitting
        self.flowmap_multi_ref_alpha_base_color = flags.flowmap_multi_ref_alpha_base_color
        self.flowmap_bloom_ref_alpha_multicolor = flags.flowmap_bloom_ref_alpha_multicolor
        self.flag_15 = flags.flag_15
        self.flag_16 = flags.flag_16
        self.flag_17 = flags.flag_17
        self.flag_18 = flags.flag_18
        self.flag_19 = flags.flag_19
        self.flag_20 = flags.flag_20
        self.flag_21 = flags.flag_21
        self.flag_22 = flags.flag_22
        self.flag_23 = flags.flag_23
        self.flag_24 = flags.flag_24
        self.flag_25 = flags.flag_25
        self.flag_26 = flags.flag_26
        self.flag_27 = flags.flag_27
        self.flag_28 = flags.flag_28
        self.flag_29 = flags.flag_29
        self.flag_30 = flags.flag_30
        self.flag_31 = flags.flag_31

    def to_flags(self):
        flags = ShaderParametersType4Flags()
        flags.flowmap_multi_as_map               = self.flowmap_multi_as_map
        flags.flowmap_rim_transparency           = self.flowmap_rim_transparency
        flags.rim_trans_negate                   = self.rim_trans_negate
        flags.flowmap_bg_distortion              = self.flowmap_bg_distortion
        flags.flowmap_multialpha_color_blend     = self.flowmap_multialpha_color_blend
        flags.flowmap_alpha_distortion           = self.flowmap_alpha_distortion
        flags.flowmap_alphamask_distortion       = self.flowmap_alphamask_distortion
        flags.flowmap_apply_alpha_only           = self.flowmap_apply_alpha_only
        flags.soft_particle                      = self.soft_particle
        flags.force_bloom_intensity              = self.force_bloom_intensity
        flags.fitting                            = self.fitting
        flags.flowmap_disable_color_correction   = self.flowmap_disable_color_correction
        flags.multifitting                       = self.multifitting
        flags.flowmap_multi_ref_alpha_base_color = self.flowmap_multi_ref_alpha_base_color
        flags.flowmap_bloom_ref_alpha_multicolor = self.flowmap_bloom_ref_alpha_multicolor
        flags.flag_15 = self.flag_15
        flags.flag_16 = self.flag_16
        flags.flag_17 = self.flag_17
        flags.flag_18 = self.flag_18
        flags.flag_19 = self.flag_19
        flags.flag_20 = self.flag_20
        flags.flag_21 = self.flag_21
        flags.flag_22 = self.flag_22
        flags.flag_23 = self.flag_23
        flags.flag_24 = self.flag_24
        flags.flag_25 = self.flag_25
        flags.flag_26 = self.flag_26
        flags.flag_27 = self.flag_27
        flags.flag_28 = self.flag_28
        flags.flag_29 = self.flag_29
        flags.flag_30 = self.flag_30
        flags.flag_31 = self.flag_31
        return flags
            
    def draw(self, layout):
        layout.prop(self, "flowmap_multi_as_map")
        layout.prop(self, "flowmap_rim_transparency")
        layout.prop(self, "rim_trans_negate")
        layout.prop(self, "flowmap_bg_distortion")
        layout.prop(self, "flowmap_multialpha_color_blend")
        layout.prop(self, "flowmap_alpha_distortion")
        layout.prop(self, "flowmap_alphamask_distortion")
        layout.prop(self, "flowmap_apply_alpha_only")
        layout.prop(self, "soft_particle")
        layout.prop(self, "force_bloom_intensity")
        layout.prop(self, "fitting")
        layout.prop(self, "flowmap_disable_color_correction")
        layout.prop(self, "multifitting")
        layout.prop(self, "flowmap_multi_ref_alpha_base_color")
        layout.prop(self, "flowmap_bloom_ref_alpha_multicolor")
        layout.prop(self, "flag_15")
        layout.prop(self, "flag_16")
        layout.prop(self, "flag_17")
        layout.prop(self, "flag_18")
        layout.prop(self, "flag_19")
        layout.prop(self, "flag_20")
        layout.prop(self, "flag_21")
        layout.prop(self, "flag_22")
        layout.prop(self, "flag_23")
        layout.prop(self, "flag_24")
        layout.prop(self, "flag_25")
        layout.prop(self, "flag_26")
        layout.prop(self, "flag_27")
        layout.prop(self, "flag_28")
        layout.prop(self, "flag_29")
        layout.prop(self, "flag_30")
        layout.prop(self, "flag_31")
