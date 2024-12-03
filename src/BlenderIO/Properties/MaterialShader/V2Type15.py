import bpy
from ....FileFormats.GFS.SubComponents.Materials.Binary.ShaderParameters.Type15 import ShaderParametersType15, ShaderParametersType15Layer, ShaderParametersType15Flags
from .Utils import copy_list


class V2Type15Layer(bpy.types.PropertyGroup):
    unknown_0x00: bpy.props.FloatProperty(name="Unknown 0x00")
    unknown_0x04: bpy.props.FloatProperty(name="Unknown 0x04")
    unknown_0x08: bpy.props.FloatProperty(name="Unknown 0x08")
    unknown_0x0C: bpy.props.FloatProperty(name="Unknown 0x0C")
    unknown_0x10: bpy.props.FloatProperty(name="Unknown 0x10")
    unknown_0x14: bpy.props.FloatProperty(name="Unknown 0x14")
    unknown_0x18: bpy.props.FloatVectorProperty(name="Unknown 0x14", default=[1.,1.,1.], size=3)

    def from_layer(self, layer):
        self.unknown_0x00 = layer.unknown_0x00
        self.unknown_0x04 = layer.unknown_0x04
        self.unknown_0x08 = layer.unknown_0x08
        self.unknown_0x0C = layer.unknown_0x0C
        self.unknown_0x10 = layer.unknown_0x10
        self.unknown_0x14 = layer.unknown_0x14
        copy_list(self.unknown_0x18, layer.unknown_0x18, 3)
    
    def to_layer(self):
        layer = ShaderParametersType15Layer()
        layer.unknown_0x00 = self.unknown_0x00
        layer.unknown_0x04 = self.unknown_0x04
        layer.unknown_0x08 = self.unknown_0x08
        layer.unknown_0x0C = self.unknown_0x0C
        layer.unknown_0x10 = self.unknown_0x10
        layer.unknown_0x14 = self.unknown_0x14
        layer.unknown_0x18 = self.unknown_0x18
        return layer
    
    def draw(self, layout):
        layout.prop(self, "unknown_0x00")
        layout.prop(self, "unknown_0x04")
        layout.prop(self, "unknown_0x08")
        layout.prop(self, "unknown_0x0C")
        layout.prop(self, "unknown_0x10")
        layout.prop(self, "unknown_0x14")
        layout.prop(self, "unknown_0x18")

class Type15Flags(bpy.types.PropertyGroup):
    triplanar_mapping: bpy.props.BoolProperty(name="Triplanar Mapping")
    gbuffer_sky_flag:  bpy.props.BoolProperty(name="GBuffer Sky Flag")
    flag_2: bpy.props.BoolProperty(name="Flag 2")
    flag_3: bpy.props.BoolProperty(name="Flag 3")
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
        self.triplanar_mapping = flags.triplanar_mapping
        self.gbuffer_sky_flag  = flags.gbuffer_sky_flag
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
        flags = ShaderParametersType15Flags()
        flags.triplanar_mapping = self.triplanar_mapping
        flags.gbuffer_sky_flag  = self.gbuffer_sky_flag
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
        layout.prop(self, "triplanar_mapping")
        layout.prop(self, "gbuffer_sky_flag")
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

    
class V2Type15Support:
    type15_layer0: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer0")
    type15_layer1: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer1")
    type15_layer2: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer2")
    type15_layer3: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer3")
    type15_layer4: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer4")
    type15_layer5: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer5")
    type15_layer6: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer6")
    type15_layer7: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer7")
    type15_layer8: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer8")
    type15_layer9: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer9")
    type15_layer10: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer10")
    type15_layer11: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer11")
    type15_layer12: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer12")
    type15_layer13: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer13")
    type15_layer14: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer14")
    type15_layer15: bpy.props.PointerProperty(type=V2Type15Layer, name="Layer15")
    
    type15_layer_count:     bpy.props.IntProperty(name="Layer Count")
    type15_triplanar_scale: bpy.props.FloatProperty(name="Triplanar Scale")
    type15_flags:           bpy.props.PointerProperty(type=Type15Flags, name="Flags")
    
    def from_V2_type15_params(self, params):
        self.type15_layer0.from_layer(params.layer0)
        self.type15_layer1.from_layer(params.layer1)
        self.type15_layer2.from_layer(params.layer2)
        self.type15_layer3.from_layer(params.layer3)
        self.type15_layer4.from_layer(params.layer4)
        self.type15_layer5.from_layer(params.layer5)
        self.type15_layer6.from_layer(params.layer6)
        self.type15_layer7.from_layer(params.layer7)
        self.type15_layer8.from_layer(params.layer8)
        self.type15_layer9.from_layer(params.layer9)
        self.type15_layer10.from_layer(params.layer10)
        self.type15_layer11.from_layer(params.layer11)
        self.type15_layer12.from_layer(params.layer12)
        self.type15_layer13.from_layer(params.layer13)
        self.type15_layer14.from_layer(params.layer14)
        self.type15_layer15.from_layer(params.layer15)
        self.type15_layer_count = params.layer_count
        self.type15_triplanar_scale = params.triplanar_scale
        self.type15_flags.from_flags(params.flags)
    
    def to_V2_type15_params(self):
        params = ShaderParametersType15()
        params.layer0 = self.type15_layer0.to_layer()
        params.layer1 = self.type15_layer1.to_layer()
        params.layer2 = self.type15_layer2.to_layer()
        params.layer3 = self.type15_layer3.to_layer()
        params.layer4 = self.type15_layer4.to_layer()
        params.layer5 = self.type15_layer5.to_layer()
        params.layer6 = self.type15_layer6.to_layer()
        params.layer7 = self.type15_layer7.to_layer()
        params.layer8 = self.type15_layer8.to_layer()
        params.layer9 = self.type15_layer9.to_layer()
        params.layer10 = self.type15_layer10.to_layer()
        params.layer11 = self.type15_layer11.to_layer()
        params.layer12 = self.type15_layer12.to_layer()
        params.layer13 = self.type15_layer13.to_layer()
        params.layer14 = self.type15_layer14.to_layer()
        params.layer15 = self.type15_layer15.to_layer()
        params.layer_count = self.type15_layer_count
        params.triplanar_scale = self.type15_triplanar_scale
        params.flags = self.type15_flags.to_flags()
        return params
    
    def draw_V2_type15_params(self, layout):
        self.type15_flags.draw(layout)
        layout.prop(self, "type15_layer_count")
        layout.prop(self, "type15_triplanar_scale")
        self.type15_layer0.draw(layout)
        self.type15_layer1.draw(layout)
        self.type15_layer2.draw(layout)
        self.type15_layer3.draw(layout)
        self.type15_layer4.draw(layout)
        self.type15_layer5.draw(layout)
        self.type15_layer6.draw(layout)
        self.type15_layer7.draw(layout)
        self.type15_layer8.draw(layout)
        self.type15_layer9.draw(layout)
        self.type15_layer10.draw(layout)
        self.type15_layer11.draw(layout)
        self.type15_layer12.draw(layout)
        self.type15_layer13.draw(layout)
        self.type15_layer14.draw(layout)
        self.type15_layer15.draw(layout)
        
        
