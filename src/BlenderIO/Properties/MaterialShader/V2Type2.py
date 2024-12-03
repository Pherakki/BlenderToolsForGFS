import bpy
from ....FileFormats.GFS.SubComponents.Materials.Binary.ShaderParameters.Type2 import ShaderParametersType2, ShaderParametersType2Flags
from .Utils import copy_list


class V2Type2Support:
    def from_V2_type2_params(self, params):
        self.type2_flags.from_flags(params.flags)
        copy_list(self.base_color,      params.base_color,     4)
        copy_list(self.shadow_color,    params.shadow_color,   4)
        copy_list(self.edge_color,      params.edge_color,     4)
        copy_list(self.emissive_color,  params.emissive_color, 4)
        copy_list(self.specular_color3, params.specular_color, 3)
        self.specular_power   = params.specular_power
        self.metallic         = params.metallic
        self.edge_threshold   = params.edge_threshold
        self.edge_factor      = params.edge_factor
        self.shadow_threshold = params.shadow_threshold
        self.shadow_factor    = params.shadow_factor
        self.type2_flags.from_flags(params.flags)
        self.type2_unknown_0x6C = params.unknown_0x6C
        copy_list(self.type2_unknown_0x70, params.unknown_0x70, 3)
        self.bloom_intensity    = params.bloom_intensity
        self.specular_threshold = params.specular_threshold
        self.edge_remove_y_axis_factor = params.edge_remove_y_axis_factor
        self.type2_unknown_0x78 = params.unknown_0x78
        self.type2_unknown_0x7C = params.unknown_0x7C
        self.type2_unknown_0x80 = params.unknown_0x80
        self.type2_unknown_0x84 = params.unknown_0x84
        self.roughness          = params.roughness
        self.fitting_tile       = params.fitting_tile
        self.multi_fitting_tile = params.multi_fitting_tile
    
    def to_V2_type2_params(self):
        params = ShaderParametersType2()
        params.base_color                = self.base_color
        params.shadow_color              = self.shadow_color
        params.edge_color                = self.edge_color
        params.emissive_color            = self.emissive_color
        params.specular_color            = self.specular_color3
        params.specular_power            = self.specular_power
        params.metallic                  = self.metallic
        params.edge_threshold            = self.edge_threshold
        params.edge_factor               = self.edge_factor
        params.shadow_threshold          = self.shadow_threshold
        params.shadow_factor             = self.shadow_factor
        params.flags                     = self.type2_flags.to_flags()
        params.unknown_0x6C              = self.type2_unknown_0x6C
        params.unknown_0x70              = self.type2_unknown_0x70
        params.bloom_intensity           = self.bloom_intensity
        params.specular_threshold        = self.specular_threshold
        params.edge_remove_y_axis_factor = self.edge_remove_y_axis_factor
        params.unknown_0x78              = self.type2_unknown_0x78
        params.unknown_0x7C              = self.type2_unknown_0x7C
        params.unknown_0x80              = self.type2_unknown_0x80
        params.unknown_0x84              = self.type2_unknown_0x84
        params.roughness                 = self.roughness
        params.fitting_tile              = self.fitting_tile
        params.multi_fitting_tile        = self.multi_fitting_tile
        return params
    
    def draw_V2_type2_params(self, layout):
        self.type2_flags.draw(layout)
        layout.prop(self, "base_color")
        layout.prop(self, "shadow_color")
        layout.prop(self, "edge_color")
        layout.prop(self, "emissive_color")
        layout.prop(self, "specular_color3")
        
        layout.prop(self, "specular_power")
        layout.prop(self, "metallic")
        layout.prop(self, "edge_threshold")
        layout.prop(self, "edge_factor")
        layout.prop(self, "shadow_threshold")
        layout.prop(self, "shadow_factor")
        layout.prop(self, "type2_unknown_0x6C")
        layout.prop(self, "type2_unknown_0x70")
        layout.prop(self, "bloom_intensity")
        layout.prop(self, "specular_threshold")
        layout.prop(self, "edge_remove_y_axis_factor")
        layout.prop(self, "type2_unknown_0x78")
        layout.prop(self, "type2_unknown_0x7C")
        layout.prop(self, "type2_unknown_0x80")
        layout.prop(self, "type2_unknown_0x84")
        layout.prop(self, "roughness")
        layout.prop(self, "fitting_tile")
        layout.prop(self, "multi_fitting_tile")


class Type2Flags(bpy.types.PropertyGroup):
    flag_0:  bpy.props.BoolProperty(name="Flag 0")
    flag_1:  bpy.props.BoolProperty(name="Flag 1")
    flag_2:  bpy.props.BoolProperty(name="Flag 2")
    flag_3:  bpy.props.BoolProperty(name="Flag 3")
    flag_4:  bpy.props.BoolProperty(name="Flag 4")
    flag_5:  bpy.props.BoolProperty(name="Flag 5")
    flag_6:  bpy.props.BoolProperty(name="Flag 6")
    flag_7:  bpy.props.BoolProperty(name="Flag 7")
    flag_8:  bpy.props.BoolProperty(name="Flag 8")
    flag_9:  bpy.props.BoolProperty(name="Flag 9")
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
        self.flag_0  = flags.flag_0
        self.flag_1  = flags.flag_1
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
        flags = ShaderParametersType2Flags()
        flags.flag_0  = self.flag_0
        flags.flag_1  = self.flag_1
        flags.flag_2  = self.flag_2
        flags.flag_3  = self.flag_3
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
        layout.prop(self, "flag_0")
        layout.prop(self, "flag_1")
        layout.prop(self, "flag_2")
        layout.prop(self, "flag_3")
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
