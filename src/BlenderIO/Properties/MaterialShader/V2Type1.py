import bpy
from ....FileFormats.GFS.SubComponents.Materials.Binary.ShaderParameters.Type1 import ShaderParametersType1
from .Utils import copy_list


class V2Type1Support:
    def from_V2_type1_params(self, params):
        copy_list(self.ambient_color,  params.ambient_color,  4)
        copy_list(self.diffuse_color,  params.diffuse_color,  4)
        copy_list(self.emissive_color, params.emissive_color, 4)
        copy_list(self.specular_color, params.specular_color, 4)
        self.reflectivity    = params.reflectivity
        self.lerp_blend_rate = params.lerp_blend_rate
    
    def to_V2_type1_params(self, params):
        params = ShaderParametersType1()
        params.ambient_color   = self.ambient_color
        params.diffuse_color   = self.diffuse_color
        params.emissive_color  = self.emissive_color
        params.specular_color  = self.specular_color
        params.reflectivity    = self.reflectivity
        params.lerp_blend_rate = self.lerp_blend_rate
        return params
    
    def draw_V2_type1_params(self, layout):
        layout.prop(self, "ambient_color")
        layout.prop(self, "diffuse_color")
        layout.prop(self, "emissive_color")
        layout.prop(self, "specular_color")
        layout.prop(self, "reflectivity")
        layout.prop(self, "lerp_blend_rate")
