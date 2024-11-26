class SizedObjArray:
    def __init__(self, member_type):
        self.__member_type = member_type
        self.count = 0
        self.data = []
        
    def __repr__(self):
        return f"SizedObjArray({self.__member_type}, {self.count})"
    
    def __len__(self):
        return len(self.data)
    
    def __iter__(self):
        for obj in self.data:
            yield obj
            
    def __getitem__(self, idx):
        return self.data[idx]
    
    def __setitem__(self, idx, value):
        if type(value) != self.__member_type:
            raise ValueError(f"Attempted to set object of the wrong type ('{type(value)}'), expected '{self.__member_type}'")
        self.data[idx] = value
        
    def clear(self):
        self.count = 0
        self.data = []
        
    def append(self, item):
        if type(item) != self.__member_type:
            raise ValueError(f"Attempted to append object of the wrong type ('{type(item)}'), expected '{self.__member_type}'")
        self.data.append(item)
        self.count += 1
        
    def insert(self, idx, item):
        if type(item) != self.__member_type:
            raise ValueError(f"Attempted to insert object of the wrong type ('{type(item)}'), expected '{self.__member_type}'")
        
        self.data.insert(idx, item)
        self.count += 1
    
    def exbip_rw(self, rw, version):
        self.count = rw.rw_uint32(self.count)
        if len(self.data):
            self.__member_type = type(self.data[0])
        self.data = rw.rw_dynamic_objs(self.data, self.__member_type, self.count, version)
