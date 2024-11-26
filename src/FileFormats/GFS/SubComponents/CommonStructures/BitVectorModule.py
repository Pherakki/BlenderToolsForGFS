class BitVector:
    __slots__ = ("_value")
    
    MAXFLAGS = 0x20
    
    def __init__(self):
        self._value = 0
        
    def exbip_rw(self, rw):
        self._value = rw.rw_uint32(self._value)
        
    def set_bit(self, bit, value):
        value = bool(value)
        self._value &= ~(1 << bit)
        self._value |= (value << bit)
    
    def get_bit(self, bit):
        return (self._value & (1 << bit)) > 0
    
    def __and__(self, value):
        return self._value & value
    
    def __iand__(self, value):
        self._value &= value
        return self
        
    def __or__(self, value):
        return self._value | value
    
    def __ior__(self, value):
        self._value |= value
        return self
    
    def __getitem__(self, idx):
        return self.get_bit(idx)
    
    def __setitem__(self, idx, value):
        self.set_bit(idx, value)

    @classmethod
    def DEF_FLAG(cls, bit):
        if bit >= cls.MAXFLAGS:
            raise TypeError(f"Attempted to define flag {bit} on {type(cls).__name__}, which has a maximum of {cls.MAXFLAGS} flags")
        return property(lambda self: self.get_bit(bit), lambda self, x: self.set_bit(bit, x))


class BitVector0x10(BitVector):
    MAXFLAGS = 0x10
    
    flag_0  = BitVector.DEF_FLAG(0x00)
    flag_1  = BitVector.DEF_FLAG(0x01)
    flag_2  = BitVector.DEF_FLAG(0x02)
    flag_3  = BitVector.DEF_FLAG(0x03)
    flag_4  = BitVector.DEF_FLAG(0x04)
    flag_5  = BitVector.DEF_FLAG(0x05)
    flag_6  = BitVector.DEF_FLAG(0x06)
    flag_7  = BitVector.DEF_FLAG(0x07)
    flag_8  = BitVector.DEF_FLAG(0x08)
    flag_9  = BitVector.DEF_FLAG(0x09)
    flag_10 = BitVector.DEF_FLAG(0x0A)
    flag_11 = BitVector.DEF_FLAG(0x0B)
    flag_12 = BitVector.DEF_FLAG(0x0C)
    flag_13 = BitVector.DEF_FLAG(0x0D)
    flag_14 = BitVector.DEF_FLAG(0x0E)
    flag_15 = BitVector.DEF_FLAG(0x0F)
    
    def exbip_rw(self, rw):
        self._value = rw.rw_uint16(self._value)


class BitVector0x20(BitVector):
    MAXFLAGS = 0x20
    
    flag_0  = BitVector.DEF_FLAG(0x00)
    flag_1  = BitVector.DEF_FLAG(0x01)
    flag_2  = BitVector.DEF_FLAG(0x02)
    flag_3  = BitVector.DEF_FLAG(0x03)
    flag_4  = BitVector.DEF_FLAG(0x04)
    flag_5  = BitVector.DEF_FLAG(0x05)
    flag_6  = BitVector.DEF_FLAG(0x06)
    flag_7  = BitVector.DEF_FLAG(0x07)
    flag_8  = BitVector.DEF_FLAG(0x08)
    flag_9  = BitVector.DEF_FLAG(0x09)
    flag_10 = BitVector.DEF_FLAG(0x0A)
    flag_11 = BitVector.DEF_FLAG(0x0B)
    flag_12 = BitVector.DEF_FLAG(0x0C)
    flag_13 = BitVector.DEF_FLAG(0x0D)
    flag_14 = BitVector.DEF_FLAG(0x0E)
    flag_15 = BitVector.DEF_FLAG(0x0F)
    flag_16 = BitVector.DEF_FLAG(0x10)
    flag_17 = BitVector.DEF_FLAG(0x11)
    flag_18 = BitVector.DEF_FLAG(0x12)
    flag_19 = BitVector.DEF_FLAG(0x13)
    flag_20 = BitVector.DEF_FLAG(0x14)
    flag_21 = BitVector.DEF_FLAG(0x15)
    flag_22 = BitVector.DEF_FLAG(0x16)
    flag_23 = BitVector.DEF_FLAG(0x17)
    flag_24 = BitVector.DEF_FLAG(0x18)
    flag_25 = BitVector.DEF_FLAG(0x19)
    flag_26 = BitVector.DEF_FLAG(0x1A)
    flag_27 = BitVector.DEF_FLAG(0x1B)
    flag_28 = BitVector.DEF_FLAG(0x1C)
    flag_29 = BitVector.DEF_FLAG(0x1D)
    flag_30 = BitVector.DEF_FLAG(0x1E)
    flag_31 = BitVector.DEF_FLAG(0x1F)
    
    def exbip_rw(self, rw):
        self._value = rw.rw_uint32(self._value)


class BitChunkVector:
    __slots__ = ("_value")
    
    MAXCHUNKS = 0x20
    CHUNKSIZE = 1
    MASK      = 1
    DEFAULT   = 0
    
    def __init__(self):
        self._value = self.DEFAULT
        
    def exbip_rw(self, rw):
        self._value = rw.rw_uint32(self._value)
        
    def set_chunk(self, idx, value):
        value = value & self.MASK
        shift = self.CHUNKSIZE*idx
        self._value &= ~(self.MASK << shift)
        self._value |= (value << shift)
    
    def get_chunk(self, idx):
        shift = self.CHUNKSIZE * idx
        return (self._value & (self.MASK << shift)) >> shift

    def __getitem__(self, idx):
        return self.get_chunk(idx)
    
    def __setitem__(self, idx, value):
        self.set_chunk(idx, value)

    @classmethod
    def CALC_MASK(cls, chunksize):
        return (1 << chunksize) - 1

    @classmethod
    def DEF_CHUNK(cls, idx):
        if idx >= cls.MAXCHUNKS:
            raise TypeError(f"Attempted to define chunk {idx} on {type(cls).__name__}, which has a maximum of {cls.MAXCHUNKS} flags")
        return property(lambda self: self.get_chunk(idx), lambda self, x: self.set_chunk(idx, x))

