from .....serialization.Serializable import Serializable
from ..CommonStructures import ObjectNameBase, ObjectName_0x01080010, SizedObjArray
from .AnimTrack import AnimationTrackBinary


class AnimationControllerBinaryBase(Serializable):
    OBJ_NAME_TYPE = ObjectNameBase
    
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.target_id = None
        self.target_name = self.OBJ_NAME_TYPE(endianness)
        
        self.tracks = SizedObjArray(AnimationTrackBinary)
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller {self.type}]"

    def read_write(self, rw):
        self.type = rw.rw_uint16(self.type) # 1 - Node, 2 - Material, 3 - Camera, 4 - Morph
        self.target_id = rw.rw_uint32(self.target_id)
        self.target_name = rw.rw_obj(self.target_name)
        rw.rw_obj(self.tracks)
    
class AnimationControllerBinary_0x01080010:
    OBJ_NAME_TYPE = ObjectName_0x01080010
