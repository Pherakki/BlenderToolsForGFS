from ....serialization.Serializable import Serializable
from ....serialization.utils import safe_format, hex32_format
from .MaterialBinary import MaterialBinary
from .ModelBinary import ModelBinary
from .TextureBinary import TextureBinary

class GFS0ContainerBinary(Serializable):
    SIZE = 0x0C
    
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.version = 0x01105100
        self.type = None
        self.size = None
        self.padding_0x0C = 0
        self.count = None
        self.data = []
        
    def __repr__(self):
        return f"[GFS::Container] {safe_format(self.version, hex32_format)} {safe_format(self.type, hex32_format)} {self.size}"
        
    def read_write(self, rw):
        self.version      = rw.rw_uint32(self.version)
        self.type         = rw.rw_uint32(self.type)
        self.size         = rw.rw_uint32(self.size)
        rw.assert_equal(self.version, 0x01105100)
        
        # This is a really ugly bit of code that is difficult to read.
        # It's an extremely simple switch, nothing logically complicated...
        # Need to make this easier on the eyes.
        if self.type == 0x00000000:
            return
        elif self.type == 0x00000001:
            return
        elif self.type == 0x00010003: # Model
            self.padding_0x0C = rw.rw_uint32(self.padding_0x0C)
            if rw.mode() == "read":
                self.data = ModelBinary()
            rw.rw_obj(self.data)
        elif self.type == 0x000100F8: # Unknown
            self.data = rw.rw_bytestring(self.data, self.size - self.SIZE)
        elif self.type == 0x000100F9: # Unknown
            self.data = rw.rw_bytestring(self.data, self.size - self.SIZE)
        elif self.type == 0x000100FB: # Materials
            self.padding_0x0C = rw.rw_uint32(self.padding_0x0C)
            self.count = rw.rw_uint32(self.count)
            self.data = rw.rw_obj_array(self.data, MaterialBinary, self.count)
        elif self.type == 0x000100FC: # Textures
            self.padding_0x0C = rw.rw_uint32(self.padding_0x0C)
            self.count = rw.rw_uint32(self.count)
            self.data = rw.rw_obj_array(self.data, TextureBinary, self.count)
        elif self.type == 0x000100FD: # Animations
            self.data = rw.rw_bytestring(self.data, self.size - self.SIZE)
        else:
            raise NotImplementedError(f"Unrecognised GFS Container Type: '{safe_format(self.type, hex32_format)}'")
