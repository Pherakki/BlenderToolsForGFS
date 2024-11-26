from ....CommonStructures import BitVector0x20


class ShaderParametersType10Flags(BitVector0x20):
    pass


class ShaderParametersType10:
    def __init__(self):
        self.unknown_0x00 = [1.,1.,1.,1.]
        self.unknown_0x10 = 0.
        self.unknown_0x14 = 0
        self.flags        = ShaderParametersType10Flags()
    
    def exbip_rw(self, rw, version):
        self.unknown_0x00     = rw.rw_float32s(self.unknown_0x00, 4)
        if version >= 0x02110091:
            self.unknown_0x10 = rw.rw_float32(self.unknown_0x10)
        self.unknown_0x14     = rw.rw_float32(self.unknown_0x14)
        if version >= 0x02110100:
            self.flags        = rw.rw_obj(self.flags)
        
    def tex1Name(self):
        return "Base Map"
    
    def tex5Name(self):
        return "Multiply Map"
