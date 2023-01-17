from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format
from ...CommonStructures import ObjectName


class PhysicsBoneBinary(Serializable):
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
        
    def __repr__(self):
        if self.has_name:
            return f"[GFS::Physics::Bone] {self.name.string} {self.unknown_0x00} {self.unknown_0x04} {self.unknown_0x08} {self.unknown_0x0C}"
        else:
            return f"[GFS::Physics::Bone] <Nameless> {self.unknown_0x00} {self.unknown_0x04} {self.unknown_0x08} {self.unknown_0x0C} {safe_format(self.unknown_0x14, list)}"
    
    def read_write(self, rw, version):
        self.unknown_0x00 = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        self.rw_unknowns(rw, version)
        self.has_name = rw.rw_uint8(self.has_name)
        if self.has_name:
            rw.rw_obj(self.name, version)
        else:
            # Appears to require a scale
            self.unknown_0x14 = rw.rw_int16s(self.unknown_0x14, 6) # Should be float16: CHARACTER/0009/C0009_173_00.GMD has a value of \xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff though
    
    def rw_unknowns(self, rw, version):
        if version > 0x1104130:
            self.unknown_0x08 = rw.rw_float32(self.unknown_0x08)
            self.unknown_0x0C = rw.rw_float32(self.unknown_0x0C)
