from .....serialization.Serializable import Serializable


class BitVector(Serializable):
    __slots__ = ("_value")
    
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

    @staticmethod
    def DEF_FLAG(bit):
        return property(lambda self: self.get_bit(bit), lambda self, x: self.set_bit(bit, x))
