from ....serialization.Serializable import Serializable
from ....serialization.utils import safe_format, hex32_format


class ObjectName(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.name_size = None
        self.name      = None
        self.name_hash = None
        
    def __repr__(self):
        return f"[GFS::ObjName] {safe_format(self.name_hash, hex32_format)} {self.name}"
    
    def read_write(self, rw):
        self.name_size = rw.rw_uint16(self.name_size)
        self.name      = rw.rw_str(self.name, self.name_size, encoding="utf8")
        if self.name_size > 0:
            self.name_hash = rw.rw_uint32(self.name_hash)

class SizedObjArray(Serializable):
    def __init__(self, member_type, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.__member_type = member_type
        self.count = None
        self.data = []
        
    def __repr__(self):
        return f"[GFS::Array] {self.count}"
    
    def read_write(self, rw):
        self.count = rw.rw_uint32(self.count)
        if rw.mode() != "read" and len(self.data):
            self.__member_type = type(self.data[0])
        self.data = rw.rw_obj_array(self.data, self.__member_type, self.count)

class Blob(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.data = b''
        
    def __repr__(self):
        return f"[GFS::Blob] {len(self.data)}"
    
    def read_write(self, rw, size):
        self.data = rw.rw_bytestring(self.data, size)

class PropertyBinary(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.name = ObjectName(endianness)
        self.size = None
        
        self.data = None
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Property] {self.name} {self.type} {self.size} {self.data}"
    
    def read_write(self, rw):
        self.type = rw.rw_uint32(self.type)
        self.name = rw.rw_obj(self.name)
        self.size = rw.rw_uint32(self.size)
        
        if self.type == 1:
            self.data = rw.rw_uint32(self.data)
        elif self.type == 2:
            self.data = rw.rw_float32(self.data)
        elif self.type == 3:
            self.data = rw.rw_uint8(self.data)
        elif self.type == 4:
            self.data = rw.rw_str(self.data, self.size - 1)
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
