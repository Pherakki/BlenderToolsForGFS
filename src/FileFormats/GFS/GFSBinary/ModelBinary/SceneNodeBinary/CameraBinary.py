from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format


class CameraBinary(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.view_matrix = None
        self.zNear = None
        self.zFar = None
        self.fov = None
        self.aspect_ratio = None
        self.unknown_0x50 = None
                   
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment::Camera] {safe_format(self.transform, list)}" \
            f"{self.zNear} {self.zFar} {self.fov} {self.aspect_ratio} {self.unknown_0x50}"
    
    def read_write(self, rw):
        self.view_matrix  = rw.rw_float32s(self.view_matrix, 16)
        self.zNear        = rw.rw_float32(self.zNear)
        self.zFar         = rw.rw_float32(self.zFar)
        self.fov          = rw.rw_float32(self.fov)
        self.aspect_ratio = rw.rw_float32(self.aspect_ratio)
        self.unknown_0x50 = rw.rw_float32(self.unknown_0x50)
