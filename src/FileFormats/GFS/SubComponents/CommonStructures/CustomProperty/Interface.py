from .Binary import PropertyBinary


def _decode_name(name, encoding, errors='strict'):
    try:
        out = name.decode(encoding, errors=errors)
    except UnicodeDecodeError as e:
        if name[-28:] == b'DirectX \xe3\x83\x9e\xe3\x83\x8d\xe3\x83\xbc\xe3\x82\xb8\xe3\x83\xa3.\x97L\x8c\xf8':
            out = name[:-4].decode("utf-8") + name[-4:].decode("shift-jis")
        else:
            raise Exception(f"Unable to decode '{name}' with encoding '{encoding}': {e}")
    return out


def _encode_name(name, encoding, errors='strict'):
    if name[-16:] == "DirectX マネージャ.有効":
        return name[:-2].encode("utf-8") + name[-2:].encode('shift-jis')
    else:
        return name.encode(encoding, errors)


class GFSProperty:
    def __init__(self):
        self.name_bytes = None
        self.type = None
        self.data = None
    
    @property
    def name(self):
        return _decode_name(self.name_bytes, "utf8")

    @name.setter
    def name(self, value):
        self.name_bytes = _encode_name(value, "utf8")

    @property
    def name_safe(self):
        return _decode_name(self.name_bytes, "utf8", 'replace')
        
    @name_safe.setter
    def name_safe(self, value):
        self.name_bytes = _encode_name(value, "utf8", 'replace')
    
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        instance.name_bytes = binary.name.string
        instance.type = binary.type
        instance.data = binary.data
        return instance
    
    def to_binary(self):
        binary = PropertyBinary()
        binary.name = binary.name.from_bytestring(self.name_bytes)
        binary.type = self.type
        binary.data = self.data
        
        # Move these checks into the binary..?
        if binary.type == 1:
            if type(binary.data) != int:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.data)}: expected int")
            binary.size = 4
            
        elif binary.type == 2:
            if type(binary.data) != int and type(binary.data) != float:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.data)}: expected int or float")
            binary.size = 4
            
        elif binary.type == 3:
            if type(binary.data) != int:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.data)}: expected int")
            binary.size = 1
            
        elif binary.type == 4:
            if type(binary.data) is not bytes:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.data)}: expected bytes")
            binary.size = len(binary.data) + 1
            
        elif binary.type == 5:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.data)}: expected an iterable object")
            if not len(binary.data) == 3:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.data)}: expected 3")
            if not all([type(t) is int for t in self.data]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.data]}: expected all ints")
                
            binary.size = 3
        
        elif binary.type == 6:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.data)}: expected an iterable object")
            if not len(binary.data) == 4:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.data)}: expected 4")
            if not all([type(t) is int for t in self.data]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.data]}: expected all ints")
                
            binary.size = 4
        
        elif binary.type == 7:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.data)}: expected an iterable object")
            if not len(binary.data) == 3:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.data)}: expected 3")
            if not all([(type(t) is int or type(t) is float) for t in self.data]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.data]}: expected all ints or floats")
                
            binary.size = 9
        
        elif binary.type == 8:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.data)}: expected an iterable object")
            if not len(binary.data) == 4:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.data)}: expected 4")
            if not all([(type(t) is int or type(t) is float)  for t in self.data]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.data]}: expected all ints or floats")
                
            binary.size = 12
                    
        elif binary.type == 9:
            if type(binary.data) is not bytes:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.data)}: expected bytes")
            binary.size = len(binary.data)
            
        else:
            raise NotImplementedError(f"Unknown property type '{self.type}'")
        return binary
