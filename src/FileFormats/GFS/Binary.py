import struct
from ...serialization.serializable import GFSSerializable
from .SubComponents.GFS0ContainerBinary import GFS0ContainerBinary
from .SubComponents.Textures.Binary import TexturePayload
from .SubComponents.Materials.Binary import MaterialPayload
from .SubComponents.Model.Binary import ModelPayload
from .SubComponents.Animations.Binary import AnimationPayload
from .SubComponents.Physics.Binary import PhysicsPayload
from .SubComponents.CommonStructures.SceneNode.EPL.EPLBinary import EPLBinary as EPLObjBinary


class NotAGFSFileError(Exception):
    def __init__(self, magic):
        super().__init__(f"Not a GFS file - found incorrect magic value '{magic}'")

GFS_MAGIC_BE = struct.unpack('<I', b'GFS0')[0]
GFS_MAGIC_LE = struct.unpack('>I', b'GFS0')[0]

class RwContainers:
    def deserialize(rw, self, warnings):
        while rw.peek_bytestring(1) != b'':
            start_offset = rw.tell()
            
            ctr = GFS0ContainerBinary()
            self.containers.append(ctr)
            rw.rw_obj(ctr)
            
            if ctr.size:
                if warnings is None:
                    remainder = ctr.size - (rw.tell() - start_offset)
                    # if remainder > 0:
                    #     print(rw.peek_bytestring(remainder))
                    rw.assert_equal(ctr.size, rw.tell() - start_offset)
                elif ctr.size != rw.tell() - start_offset:
                    warnings.append(f"Size of container {hex(ctr.type)} is {rw.tell() - start_offset}, expected {ctr.size}")
    
    def serialize(rw, self, warnings):
        for ctr in self.containers:
            rw.rw_obj(ctr)
            
    def count(rw, self, warnings):
        for ctr in self.containers:
            rw.rw_obj(ctr)


class GFSBinary(GFSSerializable):
    def __init__(self):
        super().__init__()
        
        self.magic = GFS_MAGIC_LE
        self.containers = []
        
    def __repr__(self):
        return f"[GFS] Has {len(self.containers)} container{'' if len(self.containers) == 1 else 's'}"
        
    def exbip_rw(self, rw, endianness=None, warnings=None):
        # Use the magic value to check the file endianness.
        if endianness is None:
            with rw.as_littleendian():
                self.magic      = rw.rw_uint32(self.magic)
            if (self.magic == GFS_MAGIC_BE):
                endianness = ">"
            elif self.magic == GFS_MAGIC_LE:
                endianness = "<"
            else:
                raise NotAGFSFileError(struct.pack("I", self.magic))
        else:
            self.magic = rw.rw_uint32_e(self.magic, endianness)
        
        # Parse file body.
        with rw.as_endian(endianness):
            rw.rw_descriptor(RwContainers, self, warnings)

    def get_container(self, ctr_type):
        for ctr in self.containers:
            if ctr.type == ctr_type:
                return ctr
        return None
    
    def get_texture_block(self):    return self.get_container(TexturePayload.TYPECODE)
    def get_material_block(self):   return self.get_container(MaterialPayload.TYPECODE)
    def get_model_block(self):      return self.get_container(ModelPayload.TYPECODE)
    def get_animation_block(self):  return self.get_container(AnimationPayload.TYPECODE)
    def get_physics_block(self):    return self.get_container(PhysicsPayload.TYPECODE)
    def get_0x000100F8_block(self): return self.get_container(0x000100F8)
    

class EPLFileBinary(GFSSerializable):
    def __init__(self):
        self.magic = GFS_MAGIC_BE
        self.start_block = GFS0ContainerBinary()
        self.epl = None
    
    def __repr__(self):
        return f"[EPL]"
        
    def exbip_rw(self, rw):
        # Use the magic value to check the file endianness.
        with rw.as_littleendian():
            self.magic      = rw.rw_uint32(self.magic)
        if (self.magic == GFS_MAGIC_BE):
            endianness = ">"
        elif self.magic == GFS_MAGIC_LE:
            endianness = "<"
        else:
            raise NotAGFSFileError(struct.pack("I", self.magic))
        
        # Parse file body.
        with rw.as_endian(endianness):
            rw.rw_obj(self.start_block)
            self.epl = rw.rw_dynamic_obj(self.epl, EPLObjBinary, self.start_block.version)
            