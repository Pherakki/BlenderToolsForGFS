import bpy
from ....FileFormats.GFS.SubComponents.Materials.Binary.ShaderParameters.Type7 import ShaderParametersType7, ShaderParametersType7Flags


class V2Type7Support:
    def from_V2_type7_params(self, params):
        self.type7_layer0_unknown_0 = params.layer0_unknown_0
        self.type7_layer0_unknown_1 = params.layer0_unknown_1
        self.type7_layer0_unknown_2 = params.layer0_unknown_2
        self.type7_layer0_unknown_3 = params.layer0_unknown_3
        self.type7_layer0_unknown_4 = params.layer0_unknown_4
        self.type7_layer0_unknown_5 = params.layer0_unknown_5
        self.type7_layer1_unknown_0 = params.layer1_unknown_0
        self.type7_layer1_unknown_1 = params.layer1_unknown_1
        self.type7_layer1_unknown_2 = params.layer1_unknown_2
        self.type7_layer1_unknown_3 = params.layer1_unknown_3
        self.type7_layer1_unknown_4 = params.layer1_unknown_4
        self.type7_layer1_unknown_5 = params.layer1_unknown_5
        self.type7_layer2_unknown_0 = params.layer2_unknown_0
        self.type7_layer2_unknown_1 = params.layer2_unknown_1
        self.type7_layer2_unknown_2 = params.layer2_unknown_2
        self.type7_layer2_unknown_3 = params.layer2_unknown_3
        self.type7_layer2_unknown_4 = params.layer2_unknown_4
        self.type7_layer2_unknown_5 = params.layer2_unknown_5
        self.type7_layer3_unknown_0 = params.layer3_unknown_0
        self.type7_layer3_unknown_1 = params.layer3_unknown_1
        self.type7_layer3_unknown_2 = params.layer3_unknown_2
        self.type7_layer3_unknown_3 = params.layer3_unknown_3
        self.type7_layer3_unknown_4 = params.layer3_unknown_4
        self.type7_layer3_unknown_5 = params.layer3_unknown_5
        self.type7_unknown_0x60 = params.unknown_0x60
        self.type7_flags.from_flags(params.flags)
    
    def to_V2_type7_params(self):
        params = ShaderParametersType7()
        params.layer0_unknown_0 = self.type7_layer0_unknown_0
        params.layer0_unknown_1 = self.type7_layer0_unknown_1
        params.layer0_unknown_2 = self.type7_layer0_unknown_2
        params.layer0_unknown_3 = self.type7_layer0_unknown_3
        params.layer0_unknown_4 = self.type7_layer0_unknown_4
        params.layer0_unknown_5 = self.type7_layer0_unknown_5
        params.layer1_unknown_0 = self.type7_layer1_unknown_0
        params.layer1_unknown_1 = self.type7_layer1_unknown_1
        params.layer1_unknown_2 = self.type7_layer1_unknown_2
        params.layer1_unknown_3 = self.type7_layer1_unknown_3
        params.layer1_unknown_4 = self.type7_layer1_unknown_4
        params.layer1_unknown_5 = self.type7_layer1_unknown_5
        params.layer2_unknown_0 = self.type7_layer2_unknown_0
        params.layer2_unknown_1 = self.type7_layer2_unknown_1
        params.layer2_unknown_2 = self.type7_layer2_unknown_2
        params.layer2_unknown_3 = self.type7_layer2_unknown_3
        params.layer2_unknown_4 = self.type7_layer2_unknown_4
        params.layer2_unknown_5 = self.type7_layer2_unknown_5
        params.layer3_unknown_0 = self.type7_layer3_unknown_0
        params.layer3_unknown_1 = self.type7_layer3_unknown_1
        params.layer3_unknown_2 = self.type7_layer3_unknown_2
        params.layer3_unknown_3 = self.type7_layer3_unknown_3
        params.layer3_unknown_4 = self.type7_layer3_unknown_4
        params.layer3_unknown_5 = self.type7_layer3_unknown_5
        params.unknown_0x60     = self.type7_unknown_0x60
        params.flags = self.type7_flags.to_flags()
        return params
    
    def draw_V2_type7_params(self, layout):
        layout.prop(self, "type7_layer0_unknown_0")
        layout.prop(self, "type7_layer0_unknown_1")
        layout.prop(self, "type7_layer0_unknown_2")
        layout.prop(self, "type7_layer0_unknown_3")
        layout.prop(self, "type7_layer0_unknown_4")
        layout.prop(self, "type7_layer0_unknown_5")
        layout.prop(self, "type7_layer1_unknown_0")
        layout.prop(self, "type7_layer1_unknown_1")
        layout.prop(self, "type7_layer1_unknown_2")
        layout.prop(self, "type7_layer1_unknown_3")
        layout.prop(self, "type7_layer1_unknown_4")
        layout.prop(self, "type7_layer1_unknown_5")
        layout.prop(self, "type7_layer2_unknown_0")
        layout.prop(self, "type7_layer2_unknown_1")
        layout.prop(self, "type7_layer2_unknown_2")
        layout.prop(self, "type7_layer2_unknown_3")
        layout.prop(self, "type7_layer2_unknown_4")
        layout.prop(self, "type7_layer2_unknown_5")
        layout.prop(self, "type7_layer3_unknown_0")
        layout.prop(self, "type7_layer3_unknown_1")
        layout.prop(self, "type7_layer3_unknown_2")
        layout.prop(self, "type7_layer3_unknown_3")
        layout.prop(self, "type7_layer3_unknown_4")
        layout.prop(self, "type7_layer3_unknown_5")
        layout.prop(self, "type7_unknown_0x60")
        self.type7_flags.draw(layout)


class Type7Flags(bpy.types.PropertyGroup):
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
    flag_10: bpy.props.BoolProperty(name="Flag 0")
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
        flags = ShaderParametersType7Flags()
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

