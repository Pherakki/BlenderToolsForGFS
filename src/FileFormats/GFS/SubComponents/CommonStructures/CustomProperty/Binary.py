from ......serialization.Serializable import Serializable
from ..ObjectName import ObjectName


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
        return f"[GFD::SceneContainer::SceneNode::Property {self.type}] {self.name.string} {self.size} {self.data}"
    
    def read_write(self, rw, version):
        self.type = rw.rw_uint32(self.type)
        self.name = rw.rw_obj(self.name, version)
        self.size = rw.rw_uint32(self.size)
        
        if self.type == 1:
            self.data = rw.rw_int32(self.data)
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
