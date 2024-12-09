import bpy
from .V1 import V1Support
from .V2Type0 import V2Type0Support, Type0Flags
from .V2Type1 import V2Type1Support
from .V2Type2 import V2Type2Support, Type2Flags
from .V2Type4 import V2Type4Support, Type4Flags
from .V2Water import V2WaterSupport, WaterFlags
from .V2Type6 import V2Type6Support, Type6Flags
from .V2Type7 import V2Type7Support, Type7Flags
from .V2Type8 import V2Type8Support
from .V2Type9 import V2Type9Support, Type9Flags
from .V2Type10 import V2Type10Support, Type10Flags
from .V2Type11 import V2Type11Support
from .V2Type12 import V2Type12Support, Type12Flags
from .V2Type14 import V2Type14Support
from .V2Type15 import V2Type15Support, Type15Flags
from .V2Type16 import V2Type16Support


def defn_color(name, size=4):
    return bpy.props.FloatVectorProperty(name=name, default=[1. for _ in range(size)], size=size, subtype="COLOR", soft_min=0., soft_max=1.)


class GFSToolsMaterialShaderPropsProperties(V1Support, 
                                            V2Type0Support, 
                                            V2Type1Support, 
                                            V2Type2Support, 
                                            V2Type4Support, 
                                            V2WaterSupport, 
                                            V2Type6Support, 
                                            V2Type7Support, 
                                            V2Type8Support,
                                            V2Type9Support,
                                            V2Type10Support,
                                            V2Type11Support,
                                            V2Type12Support,
                                            V2Type14Support,
                                            V2Type15Support,
                                            V2Type16Support,
                                            bpy.types.PropertyGroup):
    type0_flags:    bpy.props.PointerProperty(type=Type0Flags, name="Flags")
    type2_flags:    bpy.props.PointerProperty(type=Type2Flags, name="Flags")
    type4_flags:    bpy.props.PointerProperty(type=Type4Flags, name="Flags")
    water_flags:    bpy.props.PointerProperty(type=WaterFlags, name="Flags")
    type6_flags:    bpy.props.PointerProperty(type=Type6Flags, name="Flags")
    type7_flags:    bpy.props.PointerProperty(type=Type7Flags, name="Flags")
    type9_flags:    bpy.props.PointerProperty(type=Type9Flags, name="Flags")
    type10_flags:   bpy.props.PointerProperty(type=Type10Flags, name="Flags")
    type12_flags:   bpy.props.PointerProperty(type=Type12Flags, name="Flags")
    
    ambient_color:   defn_color("Ambient Color")
    diffuse_color:   defn_color("Diffuse Color")
    emissive_color:  defn_color("Emissive Color")
    specular_color:  defn_color("Specular Color")
    base_color:      defn_color("Base Color")
    shadow_color:    defn_color("Shadow Color")
    edge_color:      defn_color("Edge Color")
    specular_color3: defn_color("Specular Color", size=3)
    
    reflectivity:  bpy.props.FloatProperty(name="Reflectivity",  default=0)
    outline_index: bpy.props.FloatProperty(name="Outline Index", default=0)
    lerp_blend_rate: bpy.props.FloatProperty(name="Lerp Blend Rate", default=0)
    
    # Lighting / Texture Modifiers
    specular_power:     bpy.props.FloatProperty(name="Specular Power",     default=0)
    specular_threshold: bpy.props.FloatProperty(name="Specular Threshold", default=0.5)
    emissive_strength:  bpy.props.FloatProperty(name="Emissive Strength",  default=0)
    edge_threshold:     bpy.props.FloatProperty(name="Edge Threshold",     default=0)
    edge_factor:        bpy.props.FloatProperty(name="Edge Factor",        default=0)
    shadow_threshold:   bpy.props.FloatProperty(name="Shadow Threshold",   default=0)
    shadow_factor:      bpy.props.FloatProperty(name="Shadow Factor",      default=0)
    bloom_intensity:    bpy.props.FloatProperty(name="Bloom Intensity",    default=0.5)
    distortion_power:     bpy.props.FloatProperty(name="Distortion Power",   default=0)
    distortion_threshold: bpy.props.FloatProperty(name="Distortion Threshold", default=0)
    
    # PBR-y stuff??
    metallic:           bpy.props.FloatProperty(name="Metallic",           default=0)
    multi_alpha:        bpy.props.FloatProperty(name="Multi Alpha",        default=1)
    edge_remove_y_axis_factor: bpy.props.FloatProperty(name="Edge Remove Y Axis Factor", default=3)
    fitting_tile:         bpy.props.FloatProperty(name="Fitting Tile",       default=0)
    multi_fitting_tile:   bpy.props.FloatProperty(name="Multi Fitting Tile", default=0)
    ramp_alpha:           bpy.props.FloatProperty(name="Ramp Alpha")
    
    # Layer 0 PBR stuff
    emissive:      bpy.props.FloatProperty(name="Emissive")
    roughness:     bpy.props.FloatProperty(name="Roughness", default=0)
    type6_unknown: bpy.props.FloatProperty(name="Unknown")
    
    # Layer 1 PBR stuff
    layer1_base_color:      defn_color("Layer 1 Base Color", 4)
    layer1_emissive:        bpy.props.FloatProperty(name="Layer 1 Emissive")
    layer1_roughness:       bpy.props.FloatProperty(name="Layer 1 Roughness")
    layer1_bloom_intensity: bpy.props.FloatProperty(name="Layer 1 Bloom Intensity")
    type6_layer1_unknown:   bpy.props.FloatProperty(name="Layer 1 Unknown")

    # Water Parameters
    water_unknown_0x00:       bpy.props.FloatProperty(name="Unknown 0x00")
    water_unknown_0x04:       bpy.props.FloatProperty(name="Unknown 0x04")
    tc_scale:                 bpy.props.FloatProperty(name="TC Scale")
    water_unknown_0x0C:       bpy.props.FloatProperty(name="Unknown 0x0C")
    ocean_depth_scale:        bpy.props.FloatProperty(name="Ocean Depth Scale")
    disturbance_camera_scale: bpy.props.FloatProperty(name="Disturbance Camera Scale")
    disturbance_depth_scale:  bpy.props.FloatProperty(name="Disturbance Depth Scale")
    scattering_camera_scale:  bpy.props.FloatProperty(name="Scattering Camera Scale")
    disturbance_tolerance:    bpy.props.FloatProperty(name="Disturbance Tolerance")
    foam_distance:            bpy.props.FloatProperty(name="Foam Distance")
    caustics_tolerance:       bpy.props.FloatProperty(name="Caustics Tolerance")
    water_unknown_0x2C:       bpy.props.FloatProperty(name="Unknown 0x2C")
    texture_anim_speed:       bpy.props.FloatProperty(name="Texture Anim Speed")
    water_unknown_0x34:       bpy.props.FloatProperty(name="Unknown 0x34")
    
    # Unidentified / Unmerged parameters
    type0_unused:       bpy.props.FloatProperty(name="Unused Parameter", default=0)
    type2_unknown_0x6C: bpy.props.FloatProperty(name="Unknown 0x6C",     default=0)
    type2_unknown_0x70: bpy.props.FloatVectorProperty(name="Unknown 0x70", default=[0,0,0], size=3)
    type2_unknown_0x78: bpy.props.FloatProperty(name="Unknown 0x78",     default=1)
    type2_unknown_0x7C: bpy.props.FloatProperty(name="Unknown 0x7C",     default=-1)
    type2_unknown_0x80: bpy.props.FloatProperty(name="Unknown 0x80",     default=1)
    type2_unknown_0x84: bpy.props.FloatProperty(name="Unknown 0x84",     default=0.1)
    type4_unknown_0x28: bpy.props.FloatProperty(name="Unknown 0x20",     default=0)
    type4_unknown_0x34: bpy.props.FloatProperty(name="Unknown 0x34",     default=1)
    type4_unknown_0x38: bpy.props.FloatProperty(name="Unknown 0x38",     default=0)
    type6_unknown_0x40: bpy.props.FloatProperty(name="Unknown 0x40",     default=0)
    type6_unknown_0x44: bpy.props.FloatProperty(name="Unknown 0x44",     default=0)
    type6_unknown_0x48: bpy.props.FloatProperty(name="Unknown 0x48",     default=0)
    type6_unknown_0x4C: bpy.props.FloatProperty(name="Unknown 0x4C",     default=0)
    type7_layer0_unknown_0: bpy.props.FloatProperty(name="Layer 0 Unknown 0")
    type7_layer0_unknown_1: bpy.props.FloatProperty(name="Layer 0 Unknown 1")
    type7_layer0_unknown_2: bpy.props.FloatProperty(name="Layer 0 Unknown 2")
    type7_layer0_unknown_3: bpy.props.FloatProperty(name="Layer 0 Unknown 3")
    type7_layer0_unknown_4: bpy.props.FloatProperty(name="Layer 0 Unknown 4")
    type7_layer0_unknown_5: bpy.props.FloatProperty(name="Layer 0 Unknown 5")
    type7_layer1_unknown_0: bpy.props.FloatProperty(name="Layer 1 Unknown 0")
    type7_layer1_unknown_1: bpy.props.FloatProperty(name="Layer 1 Unknown 1")
    type7_layer1_unknown_2: bpy.props.FloatProperty(name="Layer 1 Unknown 2")
    type7_layer1_unknown_3: bpy.props.FloatProperty(name="Layer 1 Unknown 3")
    type7_layer1_unknown_4: bpy.props.FloatProperty(name="Layer 1 Unknown 4")
    type7_layer1_unknown_5: bpy.props.FloatProperty(name="Layer 1 Unknown 5")
    type7_layer2_unknown_0: bpy.props.FloatProperty(name="Layer 2 Unknown 0")
    type7_layer2_unknown_1: bpy.props.FloatProperty(name="Layer 2 Unknown 1")
    type7_layer2_unknown_2: bpy.props.FloatProperty(name="Layer 2 Unknown 2")
    type7_layer2_unknown_3: bpy.props.FloatProperty(name="Layer 2 Unknown 3")
    type7_layer2_unknown_4: bpy.props.FloatProperty(name="Layer 2 Unknown 4")
    type7_layer2_unknown_5: bpy.props.FloatProperty(name="Layer 2 Unknown 5")
    type7_layer3_unknown_0: bpy.props.FloatProperty(name="Layer 3 Unknown 0")
    type7_layer3_unknown_1: bpy.props.FloatProperty(name="Layer 3 Unknown 1")
    type7_layer3_unknown_2: bpy.props.FloatProperty(name="Layer 3 Unknown 2")
    type7_layer3_unknown_3: bpy.props.FloatProperty(name="Layer 3 Unknown 3")
    type7_layer3_unknown_4: bpy.props.FloatProperty(name="Layer 3 Unknown 4")
    type7_layer3_unknown_5: bpy.props.FloatProperty(name="Layer 3 Unknown 5")
    type7_unknown_0x60:     bpy.props.FloatProperty(name="Unknown 0x60")
    type8_unknown_0x00:     bpy.props.FloatProperty(name="Unknown 0x00")
    type8_unknown_0x04:     bpy.props.FloatProperty(name="Unknown 0x04")
    type8_unknown_0x08:     bpy.props.FloatProperty(name="Unknown 0x08")
    type8_unknown_0x0C:     bpy.props.FloatProperty(name="Unknown 0x0C")
    type8_unknown_0x10:     defn_color("Unknown 0x10")
    type8_unknown_0x20:     bpy.props.FloatProperty(name="Unknown 0x20")
    type8_unknown_0x24:     bpy.props.FloatProperty(name="Unknown 0x24")
    type8_unknown_0x28:     bpy.props.FloatProperty(name="Unknown 0x28")
    type8_unknown_0x2C:     bpy.props.FloatProperty(name="Unknown 0x2C")
    type9_unknown_0x00:     bpy.props.FloatProperty(name="Unknown 0x00")
    type9_unknown_0x04:     bpy.props.FloatProperty(name="Unknown 0x04")
    type9_unknown_0x08:     bpy.props.FloatProperty(name="Unknown 0x08")
    type9_unknown_0x0C:     bpy.props.FloatProperty(name="Unknown 0x0C")
    type9_unknown_0x10:     defn_color("Unknown 0x10")
    type9_unknown_0x20:     defn_color("Unknown 0x20")
    type9_unknown_0x30:     defn_color("Unknown 0x30")
    type9_unknown_0x40:     defn_color("Unknown 0x40")
    type9_unknown_0x50:     defn_color("Unknown 0x50", 3)
    type9_unknown_0x5C:     bpy.props.FloatProperty(name="Unknown_0x5C")
    type9_unknown_0x60:     bpy.props.FloatProperty(name="Unknown 0x60")
    type9_unknown_0x64:     bpy.props.FloatProperty(name="Unknown 0x64")
    type9_unknown_0x68:     bpy.props.FloatProperty(name="Unknown 0x68")
    type9_unknown_0x6C:     bpy.props.FloatProperty(name="Unknown 0x6C")
    type9_unknown_0x70:     bpy.props.FloatProperty(name="Unknown 0x70")
    type9_unknown_0x74:     bpy.props.FloatProperty(name="Unknown 0x74")
    type9_unknown_0x78:     bpy.props.FloatProperty(name="Unknown 0x78")
    type10_unknown_0x00:    defn_color("Unknown 0x00")
    type10_unknown_0x10:    bpy.props.FloatProperty(name="Unknown 0x10")
    type10_unknown_0x14:    bpy.props.FloatProperty(name="Unknown 0x14")
    type11_unknown_0x00:    defn_color("Unknown 0x00")
    type11_unknown_0x10:    bpy.props.FloatProperty(name="Unknown 0x10")
    type12_unknown_0x40:    bpy.props.FloatProperty(name="Unknown 0x40")
    type12_unknown_0x44:    defn_color("Unknown 0x44", 3)
    type12_unknown_0x50:    bpy.props.FloatProperty(name="Unknown 0x50")
    type12_unknown_0x58:    bpy.props.FloatProperty(name="Unknown 0x58")
    type12_unknown_0x5C:    bpy.props.FloatProperty(name="Unknown 0x5C")
    type12_unknown_0x60:    bpy.props.FloatProperty(name="Unknown 0x60")
    type12_unknown_0x64:    bpy.props.FloatProperty(name="Unknown 0x64")
    type12_unknown_0x40:    bpy.props.FloatProperty(name="Unknown 0x40")
    type14_unknown_0x00:    defn_color("Unknown 0x00")
    type14_unknown_0x10:    bpy.props.FloatProperty(name="Unknown 0x10")
    
    def draw(self, layout, material_props):
        param_type = material_props.shader_type
        if param_type == "V1":
            self.draw_V1_params(layout, material_props)
        elif param_type == "V2Type0":
            self.draw_V2_type0_params(layout)
        elif param_type == "V2Type1":
            self.draw_V2_type1_params(layout)
        elif param_type in ("V2Type2", "V2Type3", "V2Type13"):
            self.draw_V2_type2_params(layout)
        elif param_type == "V2Type4":
            self.draw_V2_type4_params(layout)
        elif param_type == "V2Water":
            self.draw_V2_water_params(layout)
        elif param_type == "V2Type6":
            self.draw_V2_type6_params(layout)
        elif param_type == "V2Type7":
            self.draw_V2_type7_params(layout)
        elif param_type == "V2Type8":
            self.draw_V2_type8_params(layout)
        elif param_type == "V2Type9":
            self.draw_V2_type9_params(layout)
        elif param_type == "V2Type10":
            self.draw_V2_type10_params(layout)
        elif param_type == "V2Type11":
            self.draw_V2_type11_params(layout)
        elif param_type == "V2Type12":
            self.draw_V2_type12_params(layout)
        elif param_type == "V2Type14":
            self.draw_V2_type14_params(layout)
        elif param_type == "V2Type15":
            self.draw_V2_type15_params(layout)
        elif param_type == "V2Type16":
            self.draw_V2_type16_params()
        else:
            raise ValueError(f"Invalid param type '{param_type}'")

    def from_params(self, params, material_props):
        param_type = material_props.shader_type
        if param_type == "V1":
            self.from_V1_params(params)
        elif param_type == "V2Type0":
            self.from_V2_type0_params(params)
        elif param_type == "V2Type1":
            self.from_V2_type1_params(params)
        elif param_type in ("V2Type2", "V2Type3", "V2Type13"):
            self.from_V2_type2_params(params)
        elif param_type == "V2Type4":
            self.from_V2_type4_params(params)
        elif param_type == "V2Water":
            self.from_V2_water_params(params)
        elif param_type == "V2Type6":
            self.from_V2_type6_params(params)
        elif param_type == "V2Type7":
            self.from_V2_type7_params(params)
        elif param_type == "V2Type8":
            self.from_V2_type8_params(params)
        elif param_type == "V2Type9":
            self.from_V2_type9_params(params)
        elif param_type == "V2Type10":
            self.from_V2_type10_params(params)
        elif param_type == "V2Type11":
            self.from_V2_type11_params(params)
        elif param_type == "V2Type12":
            self.from_V2_type12_params(params)
        elif param_type == "V2Type14":
            self.from_V2_type14_params(params)
        elif param_type == "V2Type15":
            self.from_V2_type15_params(params)
        elif param_type == "V2Type16":
            self.from_V2_type16_params(params)
        else:
            raise ValueError("Invalid param type '{param_type}'")

    def to_params(self, material_props):
        param_type = material_props.shader_type
        if param_type == "V1":
            return self.to_V1_params()
        elif param_type == "V2Type0":
            return self.to_V2_type0_params()
        elif param_type == "V2Type1":
            return self.to_V2_type1_params()
        elif param_type in ("V2Type2", "V2Type3", "V2Type13"):
            return self.to_V2_type2_params()
        elif param_type == "V2Type4":
            return self.to_V2_type4_params()
        elif param_type == "V2Water":
            return self.to_V2_water_params()
        elif param_type == "V2Type6":
            return self.to_V2_type6_params()
        elif param_type == "V2Type7":
            return self.to_V2_type7_params()
        elif param_type == "V2Type8":
            return self.to_V2_type8_params()
        elif param_type == "V2Type9":
            return self.to_V2_type9_params()
        elif param_type == "V2Type10":
            return self.to_V2_type10_params()
        elif param_type == "V2Type11":
            return self.to_V2_type11_params()
        elif param_type == "V2Type12":
            return self.to_V2_type12_params()
        elif param_type == "V2Type14":
            return self.to_V2_type14_params()
        elif param_type == "V2Type15":
            return self.to_V2_type15_params()
        elif param_type == "V2Type16":
            return self.to_V2_type16_params()
        else:
            raise ValueError("Invalid param type '{param_type}'")
