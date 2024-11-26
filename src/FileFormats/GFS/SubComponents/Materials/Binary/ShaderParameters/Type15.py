from ....CommonStructures import BitVector0x20


class ShaderParametersType15Flags(BitVector0x20):
    triplanar_mapping = BitVector0x20.DEF_FLAG(0)
    gbuffer_sky_flag  = BitVector0x20.DEF_FLAG(1)


class ShaderParametersType15Layer:
    def __init__(self):
        self.unknown_0x00 = 0.
        self.unknown_0x04 = 0.
        self.unknown_0x08 = 0.
        self.unknown_0x0C = 0.
        
        self.unknown_0x10 = 0.
        self.unknown_0x14 = 0.
        self.unknown_0x18 = [1., 1., 1.]
    
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
        self.unknown_0x18 = rw.rw_float32s(self.unknown_0x18, 3)

class ShaderParametersType15:
    def __init__(self):
        self.layer0  = ShaderParametersType15Layer()
        self.layer1  = ShaderParametersType15Layer()
        self.layer2  = ShaderParametersType15Layer()
        self.layer3  = ShaderParametersType15Layer()
        self.layer4  = ShaderParametersType15Layer()
        self.layer5  = ShaderParametersType15Layer()
        self.layer6  = ShaderParametersType15Layer()
        self.layer7  = ShaderParametersType15Layer()
        self.layer8  = ShaderParametersType15Layer()
        self.layer9  = ShaderParametersType15Layer()
        self.layer10 = ShaderParametersType15Layer()
        self.layer11 = ShaderParametersType15Layer()
        self.layer12 = ShaderParametersType15Layer()
        self.layer13 = ShaderParametersType15Layer()
        self.layer14 = ShaderParametersType15Layer()
        self.layer15 = ShaderParametersType15Layer()
        
        self.layer_count     = 0
        self.triplanar_scale = 0.
        self.flags           = ShaderParametersType15Flags()
    
    def exbip_rw(self, rw, version):
        self.layer0  = rw.rw_obj(self.layer0)
        self.layer1  = rw.rw_obj(self.layer1)
        self.layer2  = rw.rw_obj(self.layer2)
        self.layer3  = rw.rw_obj(self.layer3)
        self.layer4  = rw.rw_obj(self.layer4)
        self.layer5  = rw.rw_obj(self.layer5)
        self.layer6  = rw.rw_obj(self.layer6)
        self.layer7  = rw.rw_obj(self.layer7)
        self.layer8  = rw.rw_obj(self.layer8)
        self.layer9  = rw.rw_obj(self.layer9)
        self.layer10 = rw.rw_obj(self.layer10)
        self.layer11 = rw.rw_obj(self.layer11)
        self.layer12 = rw.rw_obj(self.layer12)
        self.layer13 = rw.rw_obj(self.layer13)
        self.layer14 = rw.rw_obj(self.layer14)
        self.layer15 = rw.rw_obj(self.layer15)
        
        self.layer_count     = rw.rw_uint32(self.layer_count)
        self.triplanar_scale = rw.rw_float32(self.triplanar_scale)
        self.flags           = rw.rw_obj(self.flags)
    
    def tex2Name(self):
        return "Normal Map"
    
    def tex3Name(self):
        return "Blend Map"
