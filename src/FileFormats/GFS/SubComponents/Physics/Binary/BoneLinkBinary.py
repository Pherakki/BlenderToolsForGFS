class PhysicsBoneLinkBinary:
    def __init__(self):
        self.mass = None
        self.unknown_0x04 = None
        self.radius = None
        self.parent_physics_bone = None
        self.child_physics_bone = None
        
    def __repr__(self):
        return f"[GFS::Physics::BoneLink] {self.mass} {self.unknown_0x04} {self.radius} {self.parent_physics_bone} {self.child_physics_bone}"
        
    def exbip_rw(self, rw, version):
        self.mass = rw.rw_float32(self.mass)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.rw_radius(rw, version)
        self.parent_physics_bone = rw.rw_uint16(self.parent_physics_bone)
        self.child_physics_bone = rw.rw_uint16(self.child_physics_bone)
        
    def rw_radius(self, rw, version):
        if version > 0x01104130:
            self.radius = rw.rw_float32(self.radius)
