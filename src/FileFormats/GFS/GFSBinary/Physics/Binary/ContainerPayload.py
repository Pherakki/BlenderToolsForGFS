from ......serialization.Serializable import Serializable

from .PhysicsBoneBinary import PhysicsBoneBinary
from .ColliderBinary import ColliderBinary
from .BoneLinkBinary import PhysicsBoneLinkBinary


class PhysicsPayload(Serializable):
    TYPECODE = 0x000100F9
    
    APPROVED_VERSIONS = set([
        #0x01104920,
        #0x01105000,
        #0x01105010,
        #0x01105020,
        #0x01105030,
        #0x01105040,
        #0x01105060,
        #0x01105070,
        #0x01105080,
        #0x01105090,
        0x01105100
        ])
    
    
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
        
    def read_write(self, rw, version):
        self.unknown_0x00            = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04            = rw.rw_float32(self.unknown_0x04)
        self.unknown_0x08            = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C            = rw.rw_float32(self.unknown_0x0C)
        self.unknown_0x10            = rw.rw_float32(self.unknown_0x10)
        self.physics_bone_count      = rw.rw_uint32(self.physics_bone_count)
        self.collider_count          = rw.rw_uint32(self.collider_count)
        self.physics_bone_link_count = rw.rw_uint32(self.physics_bone_link_count)
        
        self.physics_bones      = rw.rw_obj_array(self.physics_bones,      PhysicsBoneBinary,     self.physics_bone_count,      version)
        self.colliders          = rw.rw_obj_array(self.colliders,          ColliderBinary,        self.collider_count,          version)
        self.physics_bone_links = rw.rw_obj_array(self.physics_bone_links, PhysicsBoneLinkBinary, self.physics_bone_link_count, version)
        

