from .....serialization.Serializable import Serializable
from ..CommonStructures import ObjectName


class ColliderBinaryBase(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.collider_type = None
        self.capsule_radius = None
        self.capsule_height = None
        self.unknown_0x0A = None
        self.has_name = None
        self.name = ObjectName()
        
    def __repr__(self):
        if self.has_name:
            return f"[GFS::Physics::Collider] {self.name.string} {self.capsule_radius} {self.capsule_height} {self.unknown_0x0A}"
        else:
            return f"[GFS::Physics::Collider] <Nameless> {self.capsule_radius} {self.capsule_height} {self.unknown_0x0A}"
    
    def read_write(self, rw):
        self.collider_type = rw.rw_uint16(self.collider_type)
        if self.collider_type == 0:
            self.capsule_radius = rw.rw_float32(self.capsule_radius)
        elif self.collider_type == 1:
            self.capsule_radius = rw.rw_float32(self.capsule_radius)
            self.capsule_height = rw.rw_float32(self.capsule_height)
        else:
            raise NotImplementedError(f"Unknown Collider Type: {self.collider_type}")
        
        self.unknown_0x0A = rw.rw_float32s(self.unknown_0x0A, 16)
        self.has_name = rw.rw_uint8(self.has_name)
        if self.has_name:
            rw.rw_obj(self.name)
