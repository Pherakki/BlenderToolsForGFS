from ....ObjectNameModule import ObjectName
from ..Common import EPLEmbeddedFile, EPLLeafCommonData, EPLLeafCommonData2, ParticleEmitter


class EPLLeafParticle:
    def __init__(self):
        self.type = None
        self.unknown_0x04 = None
        self.particle_emitter = ParticleEmitter()
        self.embedded_file    = EPLEmbeddedFile()
        
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Leaf::Particle] {self.particle_type} {self.unknown_0x04}"
    
    def exbip_rw(self, rw, version):
        self.type         = rw.rw_uint32(self.type)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        rw.rw_obj(self.particle_emitter, version, self.type)
        rw.rw_obj(self.embedded_file, version)
