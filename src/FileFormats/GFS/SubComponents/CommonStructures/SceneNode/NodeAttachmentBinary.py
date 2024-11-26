from . import Mesh
from . import Morph
from . import Camera
from . import Light
from . import EPL
from . import EPLLeaf


class AttachmentLUT:
    ATTACHMENT_LOOKUP = {
        4: Mesh.MeshBinary,
        5: Camera.CameraBinary,
        6: Light.LightBinary,
        7: EPL.EPLBinary,
        8: EPLLeaf.EPLLeafBinary,
        9: Morph.MorphBinary
    }

    def __class_getitem__(cls, index):
        res = cls.ATTACHMENT_LOOKUP.get(index)
        if res is None:
            raise NotImplementedError(f"Unrecognised NodeAttachment type: '{index}'")
        return res


class NodeAttachmentBinary:    
    def __init__(self):
        self.type = None
        self.data = None
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment] {self.type}"
        
    def exbip_rw(self, rw, node_type, version):
        self.type = rw.rw_uint32(self.type)
        self.data = rw.rw_dynamic_obj(self.data, AttachmentLUT[self.type], version)
