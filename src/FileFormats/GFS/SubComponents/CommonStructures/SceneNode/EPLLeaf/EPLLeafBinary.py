from .......serialization.formatters import HEX32_formatter
from ....CommonStructures.ObjectNameModule import ObjectName
from ....CommonStructures.BitVectorModule  import BitVector0x20
from .Types.Particle             import EPLLeafParticle
from .Types.FlashPolygon         import EPLLeafFlashPolygon
from .Types.CirclePolygon        import EPLLeafCirclePolygon
from .Types.LightningPolygon     import EPLLeafLightningPolygon
from .Types.TrajectoryPolygon    import EPLLeafTrajectoryPolygon, EPLLeafTrajectoryPolygon2
from .Types.WindPolygon          import EPLLeafWindPolygon
from .Types.Model                import EPLLeafModel
from .Types.BoardPolygon         import EPLLeafBoardPolygon
from .Types.ObjectParticles      import EPLLeafObjectParticles
from .Types.GlitterPolygon       import EPLLeafGlitterPolygon, EPLLeafGlitterPolygon2
from .Types.DirectionalParticles import EPLLeafDirectionalParticles
from .Types.Camera               import EPLLeafCamera
from .Types.Light                import EPLLeafLight
from .Types.PostEffect           import EPLLeafPostEffect
from .Types.Helper               import EPLLeafHelper


class EPLLeafFlags(BitVector0x20):
    pass

class EPLLeafBinary:
    def __init__(self):
        self.unknown_0x00 = None
        self.unknown_0x08 = None
        self.flags = EPLLeafFlags()
        self.name = ObjectName()
        self.type = None
        self.unknown_0x1C = None
        
        self.payload = None
        
    def __repr__(self):
        return f"[GFSBinary::Scene::Node::EPL::Leaf {HEX32_formatter(self.flags._value)}] {self.name.string} {self.type} {self.unknown_0x1C}"
    
    def exbip_rw(self, rw, version):
        if version > 0x02110060:
            self.unknown_0x00 = rw.rw_float32s(self.unknown_0x00, 2)
            self.unknown_0x08 = rw.rw_float32s(self.unknown_0x08, 2)
        rw.rw_obj(self.flags)
        rw.rw_obj(self.name, version)
        self.type = rw.rw_uint32(self.type)
        self.unknown_0x1C = rw.rw_uint32(self.unknown_0x1C)
        
        if   self.type == 0:  return
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
        
        self.payload = rw.rw_dynamic_obj(self.payload, PayloadType, version)

