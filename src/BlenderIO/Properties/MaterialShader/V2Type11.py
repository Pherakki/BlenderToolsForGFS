import bpy
from ....FileFormats.GFS.SubComponents.Materials.Binary.ShaderParameters.Type11 import ShaderParametersType11
from .Utils import copy_list


class V2Type11Support:
    def from_V2_type11_params(self, params):
        copy_list(self.type11_unknown_0x00, params.unknown_0x00, 4)
        self.type11_unknown_0x10 = params.unknown_0x10
    
    def to_V2_type11_params(self):
        params = ShaderParametersType11()
        params.unknown_0x00 = self.type11_unknown_0x00
        params.unknown_0x10 = self.type11_unknown_0x10

    def draw_V2_type11_params(self, layout):
        layout.prop(self, "type11_unknown_0x00")
        layout.prop(self, "type11_unknown_0x10")
