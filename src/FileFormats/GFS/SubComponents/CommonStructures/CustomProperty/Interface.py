from .Binary import PropertyBinary


class PropertyInterface:
    def __init__(self):
        self.name = None
        self.type = None
        self.contents = None
        
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        instance.name = binary.name.string
        instance.type = binary.type
        instance.contents = binary.contents
        return instance
    
    def to_binary(self):
        binary = PropertyBinary()
        binary.name = binary.name.from_name(self.name)
        binary.type = self.type
        binary.data = self.contents
        
        # Move these checks into the binary..?
        if binary.type == 1:
            if type(binary.data) != int:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected int")
            binary.size = 4
            
        elif binary.type == 2:
            if type(binary.data) != int and type(binary.data) != float:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected int or float")
            binary.size = 4
            
        elif binary.type == 3:
            if type(binary.data) != int:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected int")
            binary.size = 1
            
        elif binary.type == 4:
            if type(binary.data) != str:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected str")
            binary.size = len(binary.data.encode(PropertyBinary.ENCODING)) - 1
            
        elif binary.type == 5:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected an iterable object")
            if not len(binary.data) == 3:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.contents)}: expected 3")
            if not all([type(t) is int for t in self.contents]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.contents]}: expected all ints")
                
            binary.size = 3
        
        elif binary.type == 6:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected an iterable object")
            if not len(binary.data) == 4:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.contents)}: expected 4")
            if not all([type(t) is int for t in self.contents]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.contents]}: expected all ints")
                
            binary.size = 4
        
        elif binary.type == 7:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected an iterable object")
            if not len(binary.data) == 3:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.contents)}: expected 3")
            if not all([type(t) is int for t in self.contents]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.contents]}: expected all ints or floats")
                
            binary.size = 9
        
        elif binary.type == 8:
            if not hasattr(binary.data, "__len__"):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected an iterable object")
            if not len(binary.data) == 4:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents has length {len(self.contents)}: expected 4")
            if not all([type(t) is int for t in self.contents]):
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents have types {[type(t) for t in self.contents]}: expected all ints or floats")
                
            binary.size = 12
                    
        elif binary.type == 9:
            if type(binary.data) != bytes:
                raise ValueError(f"Attempted to convert a 'type {self.type}' PropertyInterface, but the contents are of type {type(self.contents)}: expected bytes")
            binary.size = len(binary.data)
            
        else:
            raise NotImplementedError(f"Unknown property type '{self.type}'")
