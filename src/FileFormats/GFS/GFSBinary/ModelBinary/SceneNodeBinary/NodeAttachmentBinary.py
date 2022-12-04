from ......serialization.Serializable import Serializable
from .MeshBinary import MeshBinary
from .CameraBinary import CameraBinary
from .LightBinary import LightBinary

class HasParticleDataError(Exception):
    pass

class NodeAttachmentBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.data = None
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment] {self.type}"
        
    def read_write(self, rw, node_type):
        self.type = rw.rw_uint32(self.type)
        
        if rw.mode() == "read":
            if self.type == 4:
                dtype = MeshBinary
            elif self.type == 5:
                dtype = CameraBinary 
            elif self.type == 6:
                dtype = LightBinary
            elif self.type == 7:
                raise HasParticleDataError
            # elif self.type == 9:
            #     assert 0
            else:
                raise NotImplementedError(f"Unrecognised NodeAttachment type: '{self.type}'")
            self.data = dtype()
            
        rw.rw_obj(self.data)