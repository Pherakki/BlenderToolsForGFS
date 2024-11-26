class ShaderParametersType8:
    def __init__(self):
        self.unknown_0x00 = 0
        self.unknown_0x04 = 0
        self.unknown_0x08 = 0
        self.unknown_0x0C = 0
        self.unknown_0x10 = [1., 1., 1., 1.]
        self.unknown_0x20 = 0
        self.unknown_0x24 = 0
        self.unknown_0x28 = 0
        self.unknown_0x2C = 0
    
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 4)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_float32(self.unknown_0x28)
        self.unknown_0x2C = rw.rw_float32(self.unknown_0x2C)
