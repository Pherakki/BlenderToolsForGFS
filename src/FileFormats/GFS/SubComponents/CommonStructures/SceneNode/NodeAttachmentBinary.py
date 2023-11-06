from ......serialization.Serializable import Serializable
from . import Mesh
from . import Morph
from . import Camera
from . import Light
from . import EPL
from . import EPLLeaf


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
            if   self.type == 4: dtype = Mesh.MeshBinary
            elif self.type == 5: dtype = Camera.CameraBinary 
            elif self.type == 6: dtype = Light.LightBinary
            elif self.type == 7: dtype = EPL.EPLBinary
            elif self.type == 8: dtype = EPLLeaf.EPLLeafBinary
            elif self.type == 9: dtype = Morph.MorphBinary
            else: raise NotImplementedError(f"Unrecognised NodeAttachment type: '{self.type}'")
            self.data = dtype()
            
        rw.rw_obj(self.data, version)
