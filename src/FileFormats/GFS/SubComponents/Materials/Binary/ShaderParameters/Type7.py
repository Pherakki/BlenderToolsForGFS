from ....CommonStructures import BitVector0x20


class ShaderParametersType7Flags(BitVector0x20):
    pass


class ShaderParametersType7:
    def __init__(self):
        self.layer0_unknown_0 = 0.
        self.layer0_unknown_1 = 0.
        self.layer0_unknown_2 = 0.
        self.layer0_unknown_3 = 0.
        self.layer0_unknown_4 = 0.
        self.layer0_unknown_5 = 0.
        
        self.layer1_unknown_0 = 0.
        self.layer1_unknown_1 = 0.
        self.layer1_unknown_2 = 0.
        self.layer1_unknown_3 = 0.
        self.layer1_unknown_4 = 0.
        self.layer1_unknown_5 = 0.
        
        self.layer2_unknown_0 = 0.
        self.layer2_unknown_1 = 0.
        self.layer2_unknown_2 = 0.
        self.layer2_unknown_3 = 0.
        self.layer2_unknown_4 = 0.
        self.layer2_unknown_5 = 0.
        
        self.layer3_unknown_0 = 0.
        self.layer3_unknown_1 = 0.
        self.layer3_unknown_2 = 0.
        self.layer3_unknown_3 = 0.
        self.layer3_unknown_4 = 0.
        self.layer3_unknown_5 = 0.
        
        self.unknown_0x60      = 0.
        self.flags             = ShaderParametersType7Flags()
    
    def exbip_rw(self, rw, version):
        self.layer0_unknown_0 = rw.rw_float32(self.layer0_unknown_0)
        self.layer0_unknown_1 = rw.rw_float32(self.layer0_unknown_1)
        self.layer0_unknown_2 = rw.rw_float32(self.layer0_unknown_2)
        self.layer0_unknown_3 = rw.rw_float32(self.layer0_unknown_3)
        self.layer0_unknown_4 = rw.rw_float32(self.layer0_unknown_4)
        self.layer0_unknown_5 = rw.rw_float32(self.layer0_unknown_5)
        
        self.layer1_unknown_0 = rw.rw_float32(self.layer1_unknown_0)
        self.layer1_unknown_1 = rw.rw_float32(self.layer1_unknown_1)
        self.layer1_unknown_2 = rw.rw_float32(self.layer1_unknown_2)
        self.layer1_unknown_3 = rw.rw_float32(self.layer1_unknown_3)
        self.layer1_unknown_4 = rw.rw_float32(self.layer1_unknown_4)
        self.layer1_unknown_5 = rw.rw_float32(self.layer1_unknown_5)
        
        self.layer2_unknown_0 = rw.rw_float32(self.layer2_unknown_0)
        self.layer2_unknown_1 = rw.rw_float32(self.layer2_unknown_1)
        self.layer2_unknown_2 = rw.rw_float32(self.layer2_unknown_2)
        self.layer2_unknown_3 = rw.rw_float32(self.layer2_unknown_3)
        self.layer2_unknown_4 = rw.rw_float32(self.layer2_unknown_4)
        self.layer2_unknown_5 = rw.rw_float32(self.layer2_unknown_5)
        
        self.layer3_unknown_0 = rw.rw_float32(self.layer3_unknown_0)
        self.layer3_unknown_1 = rw.rw_float32(self.layer3_unknown_1)
        self.layer3_unknown_2 = rw.rw_float32(self.layer3_unknown_2)
        self.layer3_unknown_3 = rw.rw_float32(self.layer3_unknown_3)
        self.layer3_unknown_4 = rw.rw_float32(self.layer3_unknown_4)
        self.layer3_unknown_5 = rw.rw_float32(self.layer3_unknown_5)
        
        self.unknown_0x60      = rw.rw_float32(self.unknown_0x60)
        self.flags = rw.rw_obj(self.flags)
        
    def tex1Name(self):
        return "Layer 0 Base Map"
    
    def tex2Name(self):
        return "Layer 0 Normal Map"
    
    def tex3Name(self):
        return "Layer 1 Normal Map"
    
    def tex5Name(self):
        return "Blend Map"
    
    def tex6Name(self):
        return "Layer 1 Base Map"
    
    def tex7Name(self):
        return "Layer 2 Base Map"
    
    def tex8Name(self):
        return "Layer 2 Normal Map"
    
    def tex9Name(self):
        return "Layer 3 Base Map"
    
    def tex10Name(self):
        return "Layer 3 Normal Map"
