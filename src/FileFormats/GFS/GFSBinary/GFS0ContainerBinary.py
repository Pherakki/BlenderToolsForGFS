from ....serialization.Serializable import Serializable
from ....serialization.utils import safe_format, hex32_format
from .Materials.Binary import MaterialBinary
from .ModelBinary import ModelBinary
from .TextureBinary import TextureBinary
from .AnimationBinary import AnimationDataBinary
from .CommonStructures import SizedObjArray, Blob

class HasAnimationsError(Exception):
    pass

class UnsupportedVersionError(Exception):
    pass

class GFS0ContainerBinary(Serializable):
    SIZE = 0x0C
    
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.version = None
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
        
        # Need to be extremely careful here...
        if self.version not in [0x01105100] and (rw.mode() == "read" or rw.mode() == "write"):
            raise UnsupportedVersionError(f"GFS file version '{safe_format(self.version, hex32_format)}' is not currently supported")

        args = []
        if self.type == 0x00000000:
            pass
        elif self.type == 0x00000001:
            pass
        elif self.type == 0x00010003: # Model
            dtype = ModelBinary
        elif self.type == 0x000100F8: # Unknown
            dtype = Blob
        elif self.type == 0x000100F9: # Unknown
            dtype = Blob
        elif self.type == 0x000100FB: # Materials
            dtype = lambda : SizedObjArray(MaterialBinary)
        elif self.type == 0x000100FC: # Textures
            dtype = lambda : SizedObjArray(TextureBinary)
        elif self.type == 0x000100FD: # Animations
            dtype = AnimationDataBinary
        else:
            raise NotImplementedError(f"Unrecognised GFS Container Type: '{safe_format(self.type, hex32_format)}'")
            

        if self.type == 0x00000001:
            return
        elif self.type in [0x000100F8, 0x000100F9]: # Can be removed later
            args = [self.size - 0x10]
        
        self.padding_0x0C = rw.rw_uint32(self.padding_0x0C)
        rw.assert_equal(self.padding_0x0C, 0) 
        
        if self.type == 0x00000000:
            return
        
        if rw.mode() == "read":
            self.data = dtype()
        assert type(self.data) == type(dtype()), f"{type(self.data)}, {type(dtype())}"
        rw.rw_obj(self.data, *args) # Can remove *args when Blob can be removed
