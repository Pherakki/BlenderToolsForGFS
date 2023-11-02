from ......serialization.Serializable import Serializable
from .EPL.EPLBinary import EPLBinary
from .Mesh.MeshBinary        import MeshBinary
from .Morph.MorphBinary      import MorphBinary
from .Camera.CameraBinary    import CameraBinary
from .Light.LightBinary      import LightBinary
from .EPL.Leaf.EPLLeafBinary import EPLLeafBinary


class HasParticleDataError(Exception):
    pass

class HasType9Error(Exception):
    pass

class NodeAttachmentBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.data = None
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment] {self.type}"
        
    def read_write(self, rw, node_type, version):
        self.type = rw.rw_uint32(self.type)
        
        if rw.mode() == "read":
            if self.type == 4:
                dtype = MeshBinary
            elif self.type == 5:
                dtype = CameraBinary 
            elif self.type == 6:
                dtype = LightBinary
            elif self.type == 7:
                #raise HasParticleDataError
                dtype = EPLBinary
            elif self.type == 8:
                dtype = EPLLeafBinary
            elif self.type == 9:
                dtype = MorphBinary
            else:
                raise NotImplementedError(f"Unrecognised NodeAttachment type: '{self.type}'")
            self.data = dtype()
            
        rw.rw_obj(self.data, version)
