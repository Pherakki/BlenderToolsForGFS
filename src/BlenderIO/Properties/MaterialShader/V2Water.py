import bpy
from ....FileFormats.GFS.SubComponents.Materials.Binary.ShaderParameters.WaterShader import WaterShaderParameters, WaterShaderParametersFlags


class V2WaterSupport:
    def from_V2_water_params(self, params):
        self.water_flags.from_flags(params.flags)
        self.water_unknown_0x00       = params.unknown_0x00
        self.water_unknown_0x04       = params.unknown_0x04
        self.tc_scale                 = params.tc_scale
        self.water_unknown_0x0C       = params.unknown_0x0C
        self.ocean_depth_scale        = params.ocean_depth_scale
        self.disturbance_camera_scale = params.disturbance_camera_scale
        self.disturbance_depth_scale  = params.disturbance_depth_scale
        self.scattering_camera_scale  = params.scattering_camera_scale
        self.disturbance_tolerance    = params.disturbance_tolerance
        self.foam_distance            = params.foam_distance
        self.caustics_tolerance       = params.caustics_tolerance
        self.water_unknown_0x2C       = params.unknown_0x2C
        self.texture_anim_speed       = params.texture_anim_speed
        self.water_unknown_0x34       = params.unknown_0x34

    def to_V2_water_params(self):
        params = WaterShaderParameters()
        params.unknown_0x00             = self.water_unknown_0x00
        params.unknown_0x04             = self.water_unknown_0x04
        params.tc_scale                 = self.tc_scale
        params.unknown_0x0C             = self.water_unknown_0x0C
        params.ocean_depth_scale        = self.ocean_depth_scale
        params.disturbance_camera_scale = self.disturbance_camera_scale
        params.disturbance_depth_scale  = self.disturbance_depth_scale
        params.scattering_camera_scale  = self.scattering_camera_scale
        params.disturbance_tolerance    = self.distortion_threshold
        params.foam_distance            = self.foam_distance
        params.caustics_tolerance       = self.caustics_tolerance
        params.unknown_0x2C             = self.water_unknown_0x2C
        params.texture_anim_speed       = self.texture_anim_speed
        params.unknown_0x34             = self.water_unknown_0x34
        return params
    
    def draw_V2_water_params(self, layout):
        self.water_flags.draw(layout)
        layout.prop(self, "water_unknown_0x00")
        layout.prop(self, "water_unknown_0x04")
        layout.prop(self, "tc_scale")
        layout.prop(self, "water_unknown_0x0C")
        layout.prop(self, "ocean_depth_scale")
        layout.prop(self, "disturbance_camera_scale")
        layout.prop(self, "disturbance_depth_scale")
        layout.prop(self, "scattering_camera_scale")
        layout.prop(self, "disturbance_tolerance")
        layout.prop(self, "foam_distance")
        layout.prop(self, "caustics_tolerance")
        layout.prop(self, "water_unknown_0x2C")
        layout.prop(self, "texture_anim_speed")
        layout.prop(self, "water_unknown_0x34")


class WaterFlags(bpy.types.PropertyGroup):
    influenced_by_sky:           bpy.props.BoolProperty(name="Influenced By Sky")
    has_water_reflection:        bpy.props.BoolProperty(name="Has Water Reflection")
    is_infinite:                 bpy.props.BoolProperty(name="Is Infinite")
    outline_attenuation_invalid: bpy.props.BoolProperty(name="Outline Attenuation Invalid")
    flag_4: bpy.props.BoolProperty(name="Flag 4")
    flag_5: bpy.props.BoolProperty(name="Flag 5")
    flag_6: bpy.props.BoolProperty(name="Flag 6")
    flag_7: bpy.props.BoolProperty(name="Flag 7")
    flag_8: bpy.props.BoolProperty(name="Flag 8")
    flag_9: bpy.props.BoolProperty(name="Flag 9")
    flag_10: bpy.props.BoolProperty(name="Flag 10")
    flag_11: bpy.props.BoolProperty(name="Flag 11")
    flag_12: bpy.props.BoolProperty(name="Flag 12")
    flag_13: bpy.props.BoolProperty(name="Flag 13")
    flag_14: bpy.props.BoolProperty(name="Flag 14")
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
        self.influenced_by_sky  = flags.influenced_by_sky
        self.has_water_reflection  = flags.has_water_reflection
        self.flag_2  = flags.flag_2
        self.flag_3  = flags.flag_3
        self.flag_4  = flags.flag_4
        self.flag_5  = flags.flag_5
        self.flag_6  = flags.flag_6
        self.flag_7  = flags.flag_7
        self.flag_8  = flags.flag_8
        self.flag_9  = flags.flag_9
        self.flag_10 = flags.flag_10
        self.flag_11 = flags.flag_11
        self.flag_12 = flags.flag_12
        self.flag_13 = flags.flag_13
        self.flag_14 = flags.flag_14
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
        flags = WaterShaderParametersFlags()
        flags.influenced_by_sky           = self.influenced_by_sky
        flags.has_water_reflection        = self.has_water_reflection
        flags.is_infinite                 = self.is_infinite
        flags.outline_attenuation_invalid = self.outline_attenuation_invalid
        flags.flag_4  = self.flag_4
        flags.flag_5  = self.flag_5
        flags.flag_6  = self.flag_6
        flags.flag_7  = self.flag_7
        flags.flag_8  = self.flag_8
        flags.flag_9  = self.flag_9
        flags.flag_10 = self.flag_10
        flags.flag_11 = self.flag_11
        flags.flag_12 = self.flag_12
        flags.flag_13 = self.flag_13
        flags.flag_14 = self.flag_14
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
        layout.prop(self, "influenced_by_sky")
        layout.prop(self, "has_water_reflection")
        layout.prop(self, "is_infinite")
        layout.prop(self, "outline_attenuation_invalid")
        layout.prop(self, "flag_4")
        layout.prop(self, "flag_5")
        layout.prop(self, "flag_6")
        layout.prop(self, "flag_7")
        layout.prop(self, "flag_8")
        layout.prop(self, "flag_9")
        layout.prop(self, "flag_10")
        layout.prop(self, "flag_11")
        layout.prop(self, "flag_12")
        layout.prop(self, "flag_13")
        layout.prop(self, "flag_14")
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
