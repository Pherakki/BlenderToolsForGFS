from ....CommonStructures import BitVector0x20


class ShaderParametersType9Flags(BitVector0x20):
    pass


class ShaderParametersType9:
    def __init__(self):
        self.unknown_0x00 = 0.
        self.unknown_0x04 = 0.
        self.unknown_0x08 = 0.
        self.unknown_0x0C = 0.
        
        self.unknown_0x10 = [1.,1.,1.,1.]
        self.unknown_0x20 = [1.,1.,1.,1.]
        self.unknown_0x30 = [1.,1.,1.,1.]
        self.unknown_0x40 = [1.,1.,1.,1.]
        self.unknown_0x50 = [1.,1.,1.]    # Probably Specular Color
        self.unknown_0x5C = 0.
        
        self.unknown_0x60 = 0.
        self.unknown_0x64 = 0.
        self.unknown_0x68 = 0.
        self.unknown_0x6C = 0.
        
        self.unknown_0x70 = 0.
        self.unknown_0x74 = 0.
        self.unknown_0x78 = 0.
        self.flags        = ShaderParametersType9Flags()
    
    def exbip_rw(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
        
        self.unknown_0x10 = rw.rw_float32s(self.unknown_0x10, 4)
        self.unknown_0x20 = rw.rw_float32s(self.unknown_0x20, 4)
        self.unknown_0x30 = rw.rw_float32s(self.unknown_0x30, 4)
        self.unknown_0x40 = rw.rw_float32s(self.unknown_0x40, 4)
        self.unknown_0x50 = rw.rw_float32s(self.unknown_0x50, 3)
        self.unknown_0x5C = rw.rw_float32(self.unknown_0x5C)
        
        self.unknown_0x60 = rw.rw_float32(self.unknown_0x60)
        self.unknown_0x64 = rw.rw_float32(self.unknown_0x64)
        self.unknown_0x68 = rw.rw_float32(self.unknown_0x68)
        self.unknown_0x6C = rw.rw_float32(self.unknown_0x6C)
        
        self.unknown_0x70 = rw.rw_float32(self.unknown_0x70)
        self.unknown_0x74 = rw.rw_float32(self.unknown_0x74)
        self.unknown_0x78 = rw.rw_float32(self.unknown_0x78)
        
        self.flags        = rw.rw_obj(self.flags)
