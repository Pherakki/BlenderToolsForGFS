from ....serialization.serializable import GFSSerializable
from ....serialization.formatters import HEX32_formatter
from .Materials.Binary import MaterialPayload
from .Model.Binary import ModelPayload
from .Textures.Binary import TexturePayload
from .Animations.Binary import AnimationPayload
from .Physics.Binary import PhysicsPayload
from .CommonStructures import Blob
from ....serialization.formatters import HEX32_formatter

class HasAnimationsError(Exception):
    pass

class UnsupportedVersionError(Exception):
    pass


class ValidatePayloadType:
    def deserialize(binary_parser, data, dtype, typecode):
        pass
    
    def serialize(binary_parser, data, dtype, typecode):
        if type(data) != dtype:
            raise ValueError(f"Container '{HEX32_formatter(typecode)}' has the wrong data type ('{type(data)}'), expected '{dtype}'")

    def count(binary_parser, data, dtype, typecode):
        pass


class GFS0ContainerBinary(GFSSerializable):
    SIZE = 0x0C
    
    def __init__(self):
        super().__init__()
        
        self.version = None
        self.type = None
        self.size = None
        self.padding_0x0C = 0
        self.count = None
        self.data  = None
        
    def __repr__(self):
        return f"GFS0ContainerBinary({HEX32_formatter(self.version)} {HEX32_formatter(self.type)} {self.size})"


    def exbip_rw(self, rw):
        self.version      = rw.rw_uint32(self.version)
        self.type         = rw.rw_uint32(self.type)
        self.size         = rw.rw_uint32(self.size)

        args = []
        if self.type == 0x00000000: # EOF
            self.padding_0x0C = rw.rw_uint32(self.padding_0x0C)
            rw.assert_equal(self.padding_0x0C, 0) 
            return
        elif self.type == 0x00000001: # Persona Start
            return
        elif self.type == 0x00000008: # ReFantazio Start
            return
        elif self.type == 0x00010003: # Model
            dtype = ModelPayload
        elif self.type == 0x000100F8: # Unknown
            dtype = Blob
            args = [self.size - 0x10]
        elif self.type == 0x000100F9: # Physics
            dtype = PhysicsPayload
        elif self.type == 0x000100FB: # Materials
            dtype = MaterialPayload
        elif self.type == 0x000100FC: # Textures
            dtype = TexturePayload
        elif self.type == 0x000100FD: # Animations
            dtype = AnimationPayload
        else:
            self.padding_0x0C = rw.rw_uint32(self.padding_0x0C)
            rw.assert_equal(self.padding_0x0C, 0)
            raise NotImplementedError(f"Unrecognised GFS Container Type: '{HEX32_formatter(self.type)}'")

        self.padding_0x0C = rw.rw_uint32(self.padding_0x0C)
        rw.assert_equal(self.padding_0x0C, 0) 

        rw.rw_descriptor(ValidatePayloadType, self.data, dtype, self.type)
        self.data = rw.rw_dynamic_obj(self.data, dtype, self.version, *args) # Can remove *args when Blob can be removed
