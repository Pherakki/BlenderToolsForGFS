from ....serialization.Serializable import Serializable
from ....serialization.utils import safe_format, hex32_format


class AnimationDataBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.anim_count = None
        self.blend_anim_count = None
        
        self.animations = None
        self.blend_animations = None
        self.extra_data = None
        
    def __repr__(self):
        return f"[GFDBinary::AnimationData {safe_format(self.flags, hex32_format)}] Anims: {self.anim_count} Blend Anims: {self.blend_anim_count} Extra: {bool((self.flags >> 2) & 1)}"

    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        self.anim_count = rw.rw_uint32(self.anim_count)
        self.animations = rw.rw_obj_array(self.animations, AnimationBinary, self.anim_count)
        # self.blend_anim_count = rw.rw_uint32(self.blend_anim_count)
        # if (self.flags & 4):
        #     pass

class AnimationBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.duration = None
        self.controller_count = None
        
        self.controllers = []
        
    def __repr__(self):
        return f"[GFDBinary::Animation {safe_format(self.flags, hex32_format)}] {self.duration}"

    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        self.duration = rw.rw_float32(self.duration)
        self.controller_count = rw.rw_uint32(self.controller_count)
        self.controllers = rw.rw_obj_array(self.controllers, AnimationControllerBinary, self.controller_count)
        
class AnimationControllerBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.target_id = None
        self.target_name = None
        self.target_name_hash = None
        self.track_count = None
        
        self.tracks = []
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller {safe_format(self.type, hex32_format)}]"

    def read_write(self, rw):
        self.type = rw.rw_uint32(self.type)
        self.target_id = rw.rw_uint16(self.target_id)
        self.target_name = rw.rw_uint16_sized_str(self.target_name)
        self.target_name_hash = rw.rw_uint32(self.target_name_hash)
        self.track_count = rw.rw_uint32(self.track_count)
        self.tracks = rw.rw_obj_array(self.tracks, AnimationTrackBinary, self.track_count)
        
class AnimationTrackBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.keyframe_type = None
        self.keyframe_count = None
        
        self.frames = []
        self.values = []
        
        self.base_position = None
        self.base_scale    = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track {safe_format(self.keyframe_type, hex32_format)}] Keyframes: {self.keyframe_count}"

    def read_write(self, rw):
        self.keyframe_type = rw.rw_uint32(self.keyframe_type)
        self.keyframe_count = rw.rw_uint32(self.keyframe_count)
        
        self.frames = rw.rw_float32s(self.frames, self.keyframe_count)
        
        # Should use this to decide which "keyframe attributes" to r/w?
        # Need to figure out all kf attributes first since many overlap..?
        if self.keyframe_type == 2:
            kf_type = KeyframeType2
        elif self.keyframe_type == 12:
            kf_type = KeyframeType12
        elif self.keyframe_type == 14:
            kf_type = KeyframeType14
        elif self.keyframe_type == 27:
            kf_type = KeyframeType27
        elif self.keyframe_type == 28:
            kf_type = KeyframeType28
        elif self.keyframe_type == 29:
            kf_type = KeyframeType29
        else:
            raise NotImplementedError(f"Unknown Animation Track type: '{self.keyframe_type}'")
            
        self.values = rw.rw_obj_array(self.values, kf_type, self.keyframe_count)
        
        if self.keyframe_type in [26, 27, 28, 31, 32, 33]:
            self.base_position = rw.rw_float32s(self.base_position, 3)
            self.base_scale = rw.rw_float32s(self.base_scale, 3)

# Should probably come up with a different way to organise the r/w of these data..?!
class KeyframeType2(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = None
        self.rotation = None
        self.scale = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType2] {self.position} {self.rotation} {self.scale}"
        
    def read_write(self, rw):
        self.position = rw.rw_float32s(self.position, 3)
        self.rotation = rw.rw_float32s(self.rotation, 4)
        self.scale    = rw.rw_float32s(self.scale, 3)

class KeyframeType12(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType12] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 1) # OK
        
class KeyframeType14(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.scale = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType14] {self.scale}"
        
    def read_write(self, rw):
        self.scale = rw.rw_float32s(self.scale, 3) # Unconfirmed, looks like a scale
        print(self)
        
class KeyframeType27(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = None
        self.rotation = None
        self.scale = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType27] {self.position} {self.rotation} {self.scale}"
        
    def read_write(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.rotation = rw.rw_float16s(self.rotation, 4)
        self.scale    = rw.rw_float16s(self.scale, 3)
        
class KeyframeType28(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = None
        self.rotation = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType28] {self.position} {self.rotation}"
        
    def read_write(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.rotation = rw.rw_float16s(self.rotation, 4)
        
class KeyframeType29(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType29] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float16s(self.unknown, 2) # Not sure, only seen 0s so far
        print(self)
