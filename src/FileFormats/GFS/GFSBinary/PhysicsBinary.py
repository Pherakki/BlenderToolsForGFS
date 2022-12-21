from ....serialization.Serializable import Serializable
from ....serialization.utils import safe_format, hex32_format
from .CommonStructures import ObjectName, PropertyBinary


################
# PHYSICS BONE #
################

class PhysicsBoneBase(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = 0
        self.unknown_0x0C = 1
        self.has_name = False
        self.name = ObjectName()
        self.unknown_0x14 = None
        self.unknown_0x18 = None
        self.unknown_0x1C = None
        
    def __repr__(self):
        if self.has_name:
            return f"[GFS::Physics::Bone] {self.name.string} {self.unknown_0x00} {self.unknown_0x04} {self.unknown_0x08} {self.unknown_0x0C}"
        else:
            return f"[GFS::Physics::Bone] <Nameless> {self.unknown_0x00} {self.unknown_0x04} {self.unknown_0x08} {self.unknown_0x0C} [{self.unknown_0x14} {self.unknown_0x18} {self.unknown_0x1C}]"
    
    def read_write(self, rw):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.RW_UNKNOWNS(rw, self.unknown_0x08, self.unknown_0x0C)
        self.has_name = rw.rw_uint8(self.has_name)
        if self.has_name:
            rw.rw_obj(self.name)
        else:
            # Position?
            self.unknown_0x14 = rw.rw_float32(self.unknown_0x14)
            self.unknown_0x18 = rw.rw_float32(self.unknown_0x18)
            self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
    
    def RW_UNKNOWNS(self, rw, unknown_0x08, unknown_0x0C):
        pass

class PhysicsBone_0x1104130(PhysicsBoneBase):
    def RW_UNKNOWNS(self, rw, unknown_0x08, unknown_0x0C):
        self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
        self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)

###################
# COLLIDER BINARY #
###################

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

############################
# PHYSICS BONE LINK BINARY #
############################

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
    
##################
# PHYSICS BINARY #
##################

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
    
PHYSICS_CONTAINER_MAP = {
    0x01105100: PhysicsBinary_0x1104130
}

def get_physics_container(version):
    if version not in PHYSICS_CONTAINER_MAP:
        raise NotImplementedError(f"Version {version:0>8X} does not have a PhysicsBinary type defined")
    return PHYSICS_CONTAINER_MAP[version]
