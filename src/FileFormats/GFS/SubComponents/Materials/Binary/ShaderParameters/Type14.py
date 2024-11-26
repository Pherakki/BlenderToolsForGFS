class ShaderParametersType14:
    def __init__(self):
        self.unknown_0x00 = [1., 1., 1., 1.]
        self.unknown_0x10 = 0.
    
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 4)
        self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
