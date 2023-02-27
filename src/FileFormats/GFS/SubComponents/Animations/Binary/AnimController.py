from ......serialization.Serializable import Serializable
from ...CommonStructures import ObjectName
from ...CommonStructures.SizedObjArrayModule import SizedObjArray
from .AnimTrack import AnimationTrackBinary


class AnimationControllerBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.target_id = None
        self.target_name = ObjectName(endianness)
        self.tracks = SizedObjArray(AnimationTrackBinary)
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller {self.type}]"

    def read_write(self, rw, version):
        self.type = rw.rw_uint16(self.type) # 1 - Node, 2 - Material, 3 - Camera, 4 - Morph, 5 - ???
        self.target_id = rw.rw_uint32(self.target_id)
        self.target_name = rw.rw_obj(self.target_name, version)
        rw.rw_obj(self.tracks, version)
