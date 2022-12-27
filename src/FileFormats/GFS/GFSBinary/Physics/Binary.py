from .....serialization.Serializable import Serializable

from .PhysicsBoneBinary import PhysicsBoneBase,      \
                               PhysicsBone_0x1104130
from .ColliderBinary import ColliderBinaryBase
from .BoneLinkBinary import PhysicsBoneLinkBinaryBase,      \
                            PhysicsBoneLinkBinary_0x1104130


class PhysicsBinaryBase(Serializable):
    PHYSICS_BONE_TYPE      = PhysicsBoneBase
    COLLIDER_TYPE          = ColliderBinaryBase
    PHYSICS_BONE_LINK_TYPE = PhysicsBoneLinkBinaryBase
    
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00       = None
        self.unknown_0x04       = None
        self.unknown_0x08       = None
        self.unknown_0x0C       = None
        self.unknown_0x10       = None
        self.physics_bone_count = None
        self.collider_count = None
        self.physics_bone_link_count = None
        
        self.physics_bones = []
        self.colliders = []
        self.physics_bone_links = []
        
    def __repr__(self):
        return f"[GFS::Physics] {self.physics_bone_count} Bones, {self.collider_count} Colliders, {self.physics_bone_link_count} Bone Links, {self.unknown_0x00} {self.unknown_0x04} {self.unknown_0x08} {self.unknown_0x0C} {self.unknown_0x10}"
        
    def read_write(self, rw):
        self.unknown_0x00            = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04            = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08            = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C            = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10            = rw.rw_float32(self.unknown_0x10)
        self.physics_bone_count      = rw.rw_uint32(self.physics_bone_count)
        self.collider_count          = rw.rw_uint32(self.collider_count)
        self.physics_bone_link_count = rw.rw_uint32(self.physics_bone_link_count)
        
        self.physics_bones      = rw.rw_obj_array(self.physics_bones,      self.PHYSICS_BONE_TYPE,      self.physics_bone_count)
        self.colliders          = rw.rw_obj_array(self.colliders,          self.COLLIDER_TYPE,          self.collider_count)
        self.physics_bone_links = rw.rw_obj_array(self.physics_bone_links, self.PHYSICS_BONE_LINK_TYPE, self.physics_bone_link_count)
        

class PhysicsBinary_0x1104130(PhysicsBinaryBase):
    PHYSICS_BONE_TYPE      = PhysicsBone_0x1104130
    PHYSICS_BONE_LINK_TYPE = PhysicsBoneLinkBinary_0x1104130
