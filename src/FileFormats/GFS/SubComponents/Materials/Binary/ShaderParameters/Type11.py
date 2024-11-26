class ShaderParametersType11:
    def __init__(self):
        self.unknown_0x00 = [1., 1., 1., 1.]
        self.unknown_0x10 = 0.
        
    def exbip_rw(self, rw, version):
        self.unknown_0x00     = rw.rw_float32s(self.unknown_0x00, 4)
        if version >= 0x02108001:
            self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
    
    def tex2Name(self):
        return "Normal Map"
    
    def tex5Name(self):
        return "Multiply Map"
    
    def tex6Name(self):
        return "Emissive Map"
    
    def tex8Name(self):
        return "Toon Params Map"
