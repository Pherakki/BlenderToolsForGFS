from ...serialization.Serializable import Serializable
from .SubComponents.GFS0ContainerBinary import GFS0ContainerBinary
from .SubComponents.Textures.Binary import TexturePayload
from .SubComponents.Materials.Binary import MaterialPayload
from .SubComponents.Model.Binary import ModelPayload
from .SubComponents.Animations.Binary import AnimationPayload
from .SubComponents.Physics.Binary import PhysicsPayload
from .SubComponents.CommonStructures.SceneNode.EPL.EPLBinary import EPLBinary as EPLObjBinary

class GFSBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.magic = b'GFS0'
        self.containers = []
        
    def __repr__(self):
        return f"[GFS] Has {len(self.containers)} container{'' if len(self.containers) == 1 else 's'}"
        
    def read_write(self, rw):
        self.magic      = rw.rw_bytestring(self.magic, 4)
        rw.assert_equal(self.magic, b'GFS0')
        
        if rw.mode() == "read":
            finished = False
            while not finished:
                # Validation variable
                start_offset = rw.tell()
                
                # Read the data
                ctr = GFS0ContainerBinary()
                self.containers.append(ctr)
                rw.rw_obj(ctr)
                
                # Validate container size
                if ctr.size:
                    rw.assert_equal(ctr.size, rw.tell() - start_offset)
                
                # Check if final container
                if rw.peek_bytestring(1) == b'':
                    finished = True
                    
            # Check there's no more data
            rw.assert_at_eof()
                
        else:
            for ctr in self.containers:
                rw.rw_obj(ctr)


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
    

class EPLBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.magic = b'GFS0'
        self.start_block = GFS0ContainerBinary(endianness)
        self.epl = None
        
        
    def __repr__(self):
        return f"[EPL]"
        
    def read_write(self, rw):
        self.magic      = rw.rw_bytestring(self.magic, 4)
        rw.assert_equal(self.magic, b'GFS0')
        rw.rw_obj(self.start_block)
        self.epl = rw.rw_new_obj(self.epl, lambda: EPLObjBinary(self.context.endianness), self.start_block.version)
        