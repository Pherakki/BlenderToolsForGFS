from ....serialization.Serializable import Serializable
from ....serialization.utils import safe_format, hex32_format
from ..Utils.StringHashing import gfs_string_hash


class ObjectName(Serializable):
    ENCODING = 'utf8'
    
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.string_size = None
        self.string      = None
        self.string_hash = None
    
    @classmethod
    def from_name(cls, name):
        instance = cls()
        
        name_bytestring = name.encode(cls.ENCODING)
        instance.string = name
        instance.string_size = len(name_bytestring)
        instance.string_hash = gfs_string_hash(name_bytestring)
        
        return instance
    
    def __repr__(self):
        return f"[GFS::ObjName] {safe_format(self.string_hash, hex32_format)} {self.string}"
    
    def read_write(self, rw, version):
        # TODO: Replace if statement with something more self-documenting
        self.string_size = rw.rw_uint16(self.string_size)
        self.string      = rw.rw_str(self.string, self.string_size, encoding=self.ENCODING)
        if version > 0x01080010:
            self.rw_hash(rw)

    def rw_hash(self, rw):
        if self.string_size > 0:
            self.string_hash = rw.rw_uint32(self.string_hash)
            string_hash = gfs_string_hash(self.string.encode(self.ENCODING))

class SizedObjArray(Serializable):
    def __init__(self, member_type, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.__member_type = member_type
        self.count = 0
        self.data = []
        
    def __repr__(self):
        return f"[GFS::Array] {self.count} {self.__member_type}"
    
    def __len__(self):
        return len(self.data)
    
    def __iter__(self):
        for obj in self.data:
            yield obj
            
    def __getitem__(self, idx):
        return self.data[idx]
    
    def __setitem__(self, idx, value):
        assert type(value) == self.__member_type
        self.data[idx] = value
        
    def clear(self):
        self.count = 0
        self.data = []
        
    def append(self, item):
        assert type(item) == self.__member_type
        self.data.append(item)
        self.count += 1
        
    def insert(self, idx, item):
        assert type(item) == self.__member_type
        self.data.insert(idx, item)
        self.count += 1
    
    def read_write(self, rw, version):
        self.count = rw.rw_uint32(self.count)
        if rw.mode() != "read" and len(self.data):
            self.__member_type = type(self.data[0])
        self.data = rw.rw_obj_array(self.data, self.__member_type, self.count, version)

class Blob(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.data = b''
        
    def __repr__(self):
        return f"[GFS::Blob] {len(self.data)}"
    
    def read_write(self, rw, version, size):
        self.data = rw.rw_bytestring(self.data, size)


class PropertyBinary(Serializable):
    ENCODING = "utf8"
    
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.name = ObjectName(endianness)
        self.size = None
        
        self.data = None
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Property] {self.name} {self.type} {self.size} {self.data}"
    
    def read_write(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        self.name = rw.rw_obj(self.name, version)
        self.size = rw.rw_uint32(self.size)
        
        if self.type == 1:
            self.data = rw.rw_uint32(self.data)
        elif self.type == 2:
            self.data = rw.rw_float32(self.data)
        elif self.type == 3:
            self.data = rw.rw_uint8(self.data)
        elif self.type == 4:
            self.data = rw.rw_str(self.data, self.size - 1, encoding=self.ENCODING)
        elif self.type == 5:
            self.data = rw.rw_uint8s(self.data, 3)
        elif self.type == 6:
            self.data = rw.rw_uint8s(self.data, 4)
        elif self.type == 7:
            self.data = rw.rw_float32s(self.data, 3)
        elif self.type == 8:
            self.data = rw.rw_float32s(self.data, 4)
        elif self.type == 9:
            self.data = rw.rw_bytestring(self.data, self.size)
        else:
            raise NotImplementedError(f"Unknown Property Type '{self.type}'")


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

    @staticmethod
    def DEF_FLAG(bit):
        return property(lambda self: self.get_bit(bit), lambda self, x: self.set_bit(bit, x))
