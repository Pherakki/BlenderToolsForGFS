import bpy
from ....FileFormats.GFS.SubComponents.Materials.Binary.ShaderParameters.Compatibility import CompatibilityParameterSet
from .Utils import copy_list


class V1Support:
    def from_V1_params(self, params):
        copy_list(self.ambient_color,  params.ambient,  4)
        copy_list(self.diffuse_color,  params.diffuse,  4)
        copy_list(self.emissive_color, params.emissive, 4)
        copy_list(self.specular_color, params.specular, 4)
        self.reflectivity  = params.reflectivity
        self.outline_index = params.outline_idx
    
    def to_V1_params(self):
        params = CompatibilityParameterSet()
        params.ambient       = self.ambient_color
        params.diffuse       = self.diffuse_color
        params.emissive      = self.emissive_color
        params.specular      = self.specular_color
        params.reflectivity  = self.reflectivity
        params.outline_idx = self.outline_index
        return params
    
    def draw_V1_params(self, layout, material_props):
        layout.prop(self, "ambient_color")
        layout.prop(self, "diffuse_color")
        if material_props.enable_emissive:
            layout.prop(self, "emissive_color")
        if material_props.enable_specular:
            layout.prop(self, "specular_color")
        layout.prop(self, "reflectivity")
        layout.prop(self, "outline_index")
