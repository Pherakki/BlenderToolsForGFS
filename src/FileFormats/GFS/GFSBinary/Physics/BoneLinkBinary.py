from .....serialization.Serializable import Serializable


class PhysicsBoneLinkBinaryBase(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.mass = None
        self.unknown_0x04 = None
        self.radius = None
        self.parent_physics_bone = None
        self.child_physics_bone = None
        
    def __repr__(self):
        return f"[GFS::Physics::BoneLink] {self.mass} {self.unknown_0x04} {self.radius} {self.parent_physics_bone} {self.child_physics_bone}"
        
    def read_write(self, rw):
        self.mass = rw.rw_float32(self.mass)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.RW_RADIUS(rw, self.radius)
        self.parent_physics_bone = rw.rw_uint16(self.parent_physics_bone)
        self.child_physics_bone = rw.rw_uint16(self.child_physics_bone)
        
    def RW_RADIUS(self, rw, radius):
        pass

class PhysicsBoneLinkBinary_0x1104130(PhysicsBoneLinkBinaryBase):
    def RW_RADIUS(self, rw, radius):
        self.radius = rw.rw_float32(radius)
    