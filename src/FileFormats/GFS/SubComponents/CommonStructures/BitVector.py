from .....serialization.Serializable import Serializable


class BitVector(Serializable):
    __slots__ = ("_value")
    
    MAXFLAGS = 0x20
    
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self._value = 0
        
    def read_write(self, rw):
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
    
    def read_write(self, rw):
        self._value = rw.rw_uint16(self._value)

class BitVector0x20(BitVector):
    MAXFLAGS = 0x20
    
    def read_write(self, rw):
        self._value = rw.rw_uint32(self._value)


class BitChunkVector(Serializable):
    __slots__ = ("_value")
    
    MAXCHUNKS = 0x20
    CHUNKSIZE = 1
    MASK      = 1
    DEFAULT   = 0
    
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self._value = self.DEFAULT
        
    def read_write(self, rw):
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

