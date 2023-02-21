from .....serialization.Serializable import Serializable


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
