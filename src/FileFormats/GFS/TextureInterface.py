from .GFSBinary.TextureBinary import TextureBinary


class TextureInterface:
    def __init__(self):
        self.name = None
        self.image_data = None
        
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        
        instance.name = binary.name
        instance.image_data = binary.data
        
        return instance
    
    def to_binary(self):
        binary = TextureBinary()
        
        binary.name = self.name
        if self.image_data[:4] == b"DDS ":
            binary.pixel_format = 1
        else:
            raise NotImplementedError
        binary.data_size = len(self.image_data)
        binary.data = self.image_data
        
        return binary
