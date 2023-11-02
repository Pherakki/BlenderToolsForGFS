from .......serialization.Serializable import Serializable
from ....CommonStructures import ObjectName
from .Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafParticle(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.unknown_0x04 = None
        self.particle_emitter = ParticleEmitter(endianness)
        self.embedded_file = EPLEmbeddedFile(endianness)
        
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Leaf::Particle] {self.particle_type} {self.unknown_0x04}"
    
    def read_write(self, rw, version):
        self.type         = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        rw.rw_obj(self.particle_emitter, version, self.type)
        rw.rw_obj(self.embedded_file, version)
