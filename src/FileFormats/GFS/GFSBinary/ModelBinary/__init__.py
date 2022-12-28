from .....serialization.Serializable import Serializable
from .....serialization.utils import safe_format, hex32_format
from .SkinningDataBinary import SkinningDataBinary
from .SceneNodeBinary import SceneNodeBinary

class ModelBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags           = None
        self.skinning_data   = SkinningDataBinary(endianness)
        self.bounding_box_max_dims = None
        self.bounding_box_min_dims = None
        self.bounding_sphere_centre = None
        self.bounding_sphere_radius = None
        self.root_node = SceneNodeBinary()
        
    def __repr__(self):
        return f"[GFD::SceneContainer] {safe_format(self.flags, hex32_format)}"

    def read_write(self, rw, version):
        self.flags = rw.rw_uint32(self.flags)
        
        if self.flags & 0x00000004:
            rw.rw_obj(self.skinning_data)
        if self.flags & 0x00000001:
            self.bounding_box_max_dims = rw.rw_float32s(self.bounding_box_max_dims, 3)
            self.bounding_box_min_dims = rw.rw_float32s(self.bounding_box_min_dims, 3)
        if self.flags & 0x00000002:
            self.bounding_sphere_centre = rw.rw_float32s(self.bounding_sphere_centre, 3)
            self.bounding_sphere_radius = rw.rw_float32(self.bounding_sphere_radius)
            
        rw.rw_obj(self.root_node, version)
