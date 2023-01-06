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
