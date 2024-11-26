from .Binary import TextureBinary


class TextureInterface:
    def __init__(self):
        self.name_bytes = None
        self.image_data = None
        self.unknown_1 = None
        self.unknown_2 = None
        self.unknown_3 = None
        self.unknown_4 = None
    
    @property
    def name(self):
        return self.name_bytes.decode('shift-jis')
    @name.setter
    def name(self, value):
        self.name_bytes = value.encode('shift-jis')
    
    @property
    def name_safe(self):
        return self.name_bytes.decode('shift-jis', errors="replace")
    @name_safe.setter
    def name_safe(self, value):
        self.name_bytes = value.encode('shift-jis', errors="replace")
        
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        
        instance.name_bytes = binary.name
        instance.image_data = binary.data
        instance.unknown_1 = binary.unknown_1
        instance.unknown_2 = binary.unknown_2
        instance.unknown_3 = binary.unknown_3
        instance.unknown_4 = binary.unknown_4
        
        
        return instance
    
    def to_binary(self):
        binary = TextureBinary()
        
        binary.name = self.name_bytes
        if self.image_data[:4] == b"DDS ":
            binary.pixel_format = 1
            binary.filetype     = 1
        elif len(self.image_data) == 0:
            binary.pixel_format = 0
            binary.filetype     = 0
        else:
            raise NotImplementedError(f"Unimplemented filetype {self.image_data[:4]}")
        binary.data_size = len(self.image_data)
        binary.data      = self.image_data
        binary.unknown_1 = self.unknown_1
        binary.unknown_2 = self.unknown_2
        binary.unknown_3 = self.unknown_3
        binary.unknown_4 = self.unknown_4
        
        return binary
