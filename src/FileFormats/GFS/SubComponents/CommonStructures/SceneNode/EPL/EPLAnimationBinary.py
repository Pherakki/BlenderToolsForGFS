from ....CommonStructures.BitVectorModule  import BitVector0x20
from ....CommonStructures.SizedObjArrayModule import SizedObjArray
from ....Animations.Binary.AnimationBinary import AnimationBinary


class EPLAnimationFlags(BitVector0x20):
    pass


class EPLAnimationBinary:
    def __init__(self):
        self.flags = EPLAnimationFlags()
        self.unknown_0x04 = None
        self.animation = AnimationBinary()
        self.epl_controllers = SizedObjArray(EPLAnimationController)
                   
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Animation]"
            
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.flags)
        self.unknown_0x04 = rw.rw_float32(self.unknown_0x04)
        rw.rw_obj(self.animation, version)
        rw.rw_obj(self.epl_controllers, version)

class EPLAnimationController:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.controller_idx = None
        self.unknown_0x0C = None
        
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Animation::Controller] {self.unknown_0x00} {self.unknown_0x04} {self.controller_idx} {self.unknown_0x0C}"
    
    def exbip_rw(self, rw, version):
        self.unknown_0x00   = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04   = rw.rw_float32(self.unknown_0x04)
        self.controller_idx = rw.rw_int32(self.controller_idx)
        self.unknown_0x0C   = rw.rw_int32(self.unknown_0x0C)
