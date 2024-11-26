import bpy
from ....FileFormats.GFS.SubComponents.Materials.Binary.ShaderParameters.Type8 import ShaderParametersType8
from .Utils import copy_list


class V2Type8Support:
    def from_V2_type8_params(self, params):
        self.type8_unknown_0x00 = params.unknown_0x00
        self.type8_unknown_0x04 = params.unknown_0x04
        self.type8_unknown_0x08 = params.unknown_0x08
        self.type8_unknown_0x0C = params.unknown_0x0C
        copy_list(self.type8_unknown_0x10, params.unknown_0x10, 4)
        self.type8_unknown_0x20 = params.unknown_0x20
        self.type8_unknown_0x24 = params.unknown_0x24
        self.type8_unknown_0x28 = params.unknown_0x28
        self.type8_unknown_0x2C = params.unknown_0x2C
    
    def to_V2_type8_params(self):
        params = ShaderParametersType8()
        params.unknown_0x00 = self.type8_unknown_0x00
        params.unknown_0x04 = self.type8_unknown_0x04
        params.unknown_0x08 = self.type8_unknown_0x08
        params.unknown_0x0C = self.type8_unknown_0x0C
        params.unknown_0x10 = self.type8_unknown_0x10
        params.unknown_0x20 = self.type8_unknown_0x20
        params.unknown_0x24 = self.type8_unknown_0x24
        params.unknown_0x28 = self.type8_unknown_0x28
        params.unknown_0x2C = self.type8_unknown_0x2C
        return params
    
    def draw_V2_type8_params(self, layout):
        layout.prop(self, "type8_unknown_0x00")
        layout.prop(self, "type8_unknown_0x04")
        layout.prop(self, "type8_unknown_0x08")
        layout.prop(self, "type8_unknown_0x0C")
        layout.prop(self, "type8_unknown_0x10")
        layout.prop(self, "type8_unknown_0x20")
        layout.prop(self, "type8_unknown_0x24")
        layout.prop(self, "type8_unknown_0x28")
        layout.prop(self, "type8_unknown_0x2C")
