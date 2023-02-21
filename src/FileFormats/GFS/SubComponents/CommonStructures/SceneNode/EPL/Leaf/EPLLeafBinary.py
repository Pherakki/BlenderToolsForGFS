from ........serialization.Serializable import Serializable
from ........serialization.utils import safe_format, hex32_format
from .....CommonStructures import ObjectName, BitVector0x20
from .Particle             import EPLLeafParticle
from .FlashPolygon         import EPLLeafFlashPolygon
from .CirclePolygon        import EPLLeafCirclePolygon
from .LightningPolygon     import EPLLeafLightningPolygon
from .TrajectoryPolygon    import EPLLeafTrajectoryPolygon, EPLLeafTrajectoryPolygon2
from .WindPolygon          import EPLLeafWindPolygon
from .Model                import EPLLeafModel
from .BoardPolygon         import EPLLeafBoardPolygon
from .ObjectParticles      import EPLLeafObjectParticles
from .GlitterPolygon       import EPLLeafGlitterPolygon, EPLLeafGlitterPolygon2
from .DirectionalParticles import EPLLeafDirectionalParticles
from .Camera               import EPLLeafCamera
from .Light                import EPLLeafLight
from .PostEffect           import EPLLeafPostEffect
from .Helper               import EPLLeafHelper


class EPLLeafFlags(BitVector0x20):
    flag_0      = BitVector0x20.DEF_FLAG(0x00)
    flag_1      = BitVector0x20.DEF_FLAG(0x01)
    flag_2      = BitVector0x20.DEF_FLAG(0x02)
    flag_3      = BitVector0x20.DEF_FLAG(0x03)
    flag_4      = BitVector0x20.DEF_FLAG(0x04)
    flag_5      = BitVector0x20.DEF_FLAG(0x05)
    flag_6      = BitVector0x20.DEF_FLAG(0x06)
    flag_7      = BitVector0x20.DEF_FLAG(0x07)
    flag_8      = BitVector0x20.DEF_FLAG(0x08)
    flag_9      = BitVector0x20.DEF_FLAG(0x09)
    flag_10     = BitVector0x20.DEF_FLAG(0x0A)
    flag_11     = BitVector0x20.DEF_FLAG(0x0B)
    flag_12     = BitVector0x20.DEF_FLAG(0x0C)
    flag_13     = BitVector0x20.DEF_FLAG(0x0D)
    flag_14     = BitVector0x20.DEF_FLAG(0x0E)
    flag_15     = BitVector0x20.DEF_FLAG(0x0F)
    flag_16     = BitVector0x20.DEF_FLAG(0x10)
    flag_17     = BitVector0x20.DEF_FLAG(0x11)
    flag_18     = BitVector0x20.DEF_FLAG(0x12)
    flag_19     = BitVector0x20.DEF_FLAG(0x13)
    flag_20     = BitVector0x20.DEF_FLAG(0x14)
    flag_21     = BitVector0x20.DEF_FLAG(0x15)
    flag_22     = BitVector0x20.DEF_FLAG(0x16)
    flag_23     = BitVector0x20.DEF_FLAG(0x17)
    flag_24     = BitVector0x20.DEF_FLAG(0x18)
    flag_25     = BitVector0x20.DEF_FLAG(0x19)
    flag_26     = BitVector0x20.DEF_FLAG(0x1A)
    flag_27     = BitVector0x20.DEF_FLAG(0x1B)
    flag_28     = BitVector0x20.DEF_FLAG(0x1C)
    flag_29     = BitVector0x20.DEF_FLAG(0x1D)
    flag_30     = BitVector0x20.DEF_FLAG(0x1E)
    flag_31     = BitVector0x20.DEF_FLAG(0x1F)


class EPLLeafBinary(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = EPLLeafFlags()
        self.name = ObjectName(endianness)
        self.type = None
        self.unknown_0x0C = None
        
        self.payload = None
        
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Leaf {safe_format(self.flags._value, hex32_format)}] {self.name.string} {self.type} {self.unknown_0x0C}"
    
    def read_write(self, rw, version):
        rw.rw_obj(self.flags)
        rw.rw_obj(self.name, version)
        self.type = rw.rw_uint32(self.type)
        self.unknown_0x0C = rw.rw_uint32(self.unknown_0x0C)
        
        if self.type == 0: return
        elif self.type == 1:  PayloadType = EPLLeafParticle
        elif self.type == 2:  PayloadType = EPLLeafFlashPolygon
        elif self.type == 3:  PayloadType = EPLLeafCirclePolygon
        elif self.type == 4:  PayloadType = EPLLeafLightningPolygon
        elif self.type == 5:  PayloadType = EPLLeafTrajectoryPolygon
        elif self.type == 6:  PayloadType = EPLLeafWindPolygon
        elif self.type == 7:  PayloadType = EPLLeafModel
        elif self.type == 8:  PayloadType = EPLLeafTrajectoryPolygon2
        elif self.type == 9:  PayloadType = EPLLeafBoardPolygon
        elif self.type == 10: PayloadType = EPLLeafObjectParticles
        elif self.type == 11: PayloadType = EPLLeafGlitterPolygon
        elif self.type == 12: PayloadType = EPLLeafGlitterPolygon2
        elif self.type == 13: PayloadType = EPLLeafDirectionalParticles
        elif self.type == 14: PayloadType = EPLLeafCamera
        elif self.type == 15: PayloadType = EPLLeafLight
        elif self.type == 16: PayloadType = EPLLeafPostEffect
        elif self.type == 17: PayloadType = EPLLeafHelper
        else:
            raise NotImplementedError(f"Unknown EPLLeaf type '{self.type}'")
        
        self.payload = rw.rw_new_obj(self.payload, lambda: PayloadType(self.context.endianness), version)

