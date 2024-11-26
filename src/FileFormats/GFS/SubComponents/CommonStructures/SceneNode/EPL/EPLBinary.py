from .......serialization.formatters import HEX32_formatter
from ....CommonStructures.BitVectorModule  import BitVector0x20
from .EPLAnimationBinary import EPLAnimationBinary
from .. import NodeBinary


class EPLFlags(BitVector0x20):
    pass


class EPLBinary:
    def __init__(self):
        self.flags = EPLFlags()
        self.root_node = NodeBinary.SceneNodeBinary()
        self.animation = EPLAnimationBinary()
        self.unknown = 0
        self.unknown_vec_1 = [0., 0., 0., 0.]
        self.unknown_vec_2 = [0., 0., 0., 0.]
        
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL {HEX32_formatter(self.flags._value)}]"
            
    def exbip_rw(self, rw, version):
        rw.rw_obj(self.flags)
        rw.rw_obj(self.root_node, version)
        rw.rw_obj(self.animation, version)
        if version >  0x01105060:
            self.unknown = rw.rw_uint16(self.unknown)
        # # Seems spurious... this screws up EPL file reads
        # if version >= 0x02110208 and self.flags.flag_9:
        #     self.unknown_vec_1 = rw.rw_float32s(self.unknown_vec_1, 4)
        #     self.unknown_vec_2 = rw.rw_float32s(self.unknown_vec_2, 4)
