import bpy
from ....FileFormats.GFS.SubComponents.Materials.Binary.ShaderParameters.Type14 import ShaderParametersType14
from .Utils import copy_list


class V2Type14Support:
    def from_V2_type14_params(self, params):
        copy_list(self.type14_unknown_0x00, params.unknown_0x00, 4)
        self.type14_unknown_0x10 = params.unknown_0x10
        
    def to_V2_type14_params(self):
        params = ShaderParametersType14()
        params.unknown_0x00 = self.type14_unknown_0x00
        params.unknown_0x10 = self.type14_unknown_0x10
        
    def draw_V2_type14_params(self, layout):
        layout.prop(self, "type14_unknown_0x00")
        layout.prop(self, "type14_unknown_0x10")
