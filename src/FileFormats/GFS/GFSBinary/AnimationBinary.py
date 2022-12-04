from ....serialization.Serializable import Serializable
from ....serialization.utils import safe_format, hex32_format
from .CommonStructures import ObjectName, PropertyBinary

class ParticlesError(Exception):
    pass

class LayerError(Exception):
    pass

class AnimationDataBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.anim_count = None
        self.blend_anim_count = None
        
        self.animations = None
        self.blend_animations = None
        self.unknown_anim_chunk = None
        
    def __repr__(self):
        return f"[GFDBinary::AnimationData {safe_format(self.flags, hex32_format)}] Anims: {self.anim_count} Blend Anims: {self.blend_anim_count} Extra: {safe_format(self.flags, lambda x: bool((x >> 2) & 1))}"

    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        self.anim_count = rw.rw_uint32(self.anim_count)
        self.animations = rw.rw_obj_array(self.animations, AnimationBinary, self.anim_count)
        self.blend_anim_count = rw.rw_uint32(self.blend_anim_count)
        self.blend_animations = rw.rw_obj_array(self.blend_animations, AnimationBinary, self.blend_anim_count)
        if (self.flags & 4):
            if rw.mode() == "read":
                self.unknown_anim_chunk = UnknownAnimationChunk(self.context.endianness)
            rw.rw_obj(self.unknown_anim_chunk)

class AnimationBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.duration = None
        self.controller_count = None
        self.controllers = []
        
        #self.particle_count = None
        #self.particle_data = ParticleData()
        self.unknown_anim_chunk = None
        self.animation_layer = AnimationLayer()
        # Bounding boxes should probably go into a custom datatype
        self.bounding_box_max_dims = None
        self.bounding_box_min_dims = None
        self.speed = None
        self.property_count = None
        self.properties = []
        
        
    def __repr__(self):
        return f"[GFDBinary::Animation {safe_format(self.flags, hex32_format)}] {self.duration}"

    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        self.duration = rw.rw_float32(self.duration)
        self.controller_count = rw.rw_uint32(self.controller_count)
        self.controllers = rw.rw_obj_array(self.controllers, AnimationControllerBinary, self.controller_count)
        
        # Only certain flags used for certain chunk versions..?
        if self.flags & 0x10000000:
            raise ParticlesError()
        if self.flags & 0x20000000:
            if rw.mode() == "read":
                self.unknown_anim_chunk = UnknownAnimationChunk(self.context.endianness)
            rw.rw_obj(self.unknown_anim_chunk)
        if self.flags & 0x80000000:
            rw.rw_obj(self.animation_layer)
        if self.flags & 0x40000000:
            self.bounding_box_max_dims = rw.rw_float32s(self.bounding_box_max_dims, 3)
            self.bounding_box_min_dims = rw.rw_float32s(self.bounding_box_min_dims, 3)
        if self.flags & 0x02000000:
            self.speed = rw.rw_float32(self.speed)
        if self.flags & 0x00800000:
            self.property_count = rw.rw_uint32(self.property_count)
            self.properties = rw.rw_obj_array(self.properties, PropertyBinary, self.property_count)
            
        # Catch other flags being set?

class AnimationControllerBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.type = None
        self.target_id = None
        self.target_name = ObjectName(endianness)
        self.track_count = None
        
        self.tracks = []
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller {safe_format(self.type, hex32_format)}]"

    def read_write(self, rw):
        self.type = rw.rw_uint32(self.type)
        self.target_id = rw.rw_uint16(self.target_id)
        self.target_name = rw.rw_obj(self.target_name)
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
        if self.keyframe_type == 1:
            kf_type = KeyframeType1
        elif self.keyframe_type == 2:
            kf_type = KeyframeType2
        elif self.keyframe_type == 3:
            kf_type = KeyframeType3
        elif self.keyframe_type == 12:
            kf_type = KeyframeType12
        elif self.keyframe_type == 14:
            kf_type = KeyframeType14
        elif self.keyframe_type == 23:
            kf_type = KeyframeType23
        elif self.keyframe_type == 24:
            kf_type = KeyframeType24
        elif self.keyframe_type == 26:
            kf_type = KeyframeType26
        elif self.keyframe_type == 27:
            kf_type = KeyframeType27
        elif self.keyframe_type == 28:
            kf_type = KeyframeType28
        elif self.keyframe_type == 29:
            kf_type = KeyframeType29
        elif self.keyframe_type == 31:
            kf_type = KeyframeType31
        elif self.keyframe_type == 32:
            kf_type = KeyframeType32
        elif self.keyframe_type == 33:
            kf_type = KeyframeType33
        elif self.keyframe_type == 35:
            kf_type = KeyframeType35
        else:
            raise NotImplementedError(f"Unknown Animation Track type: '{self.keyframe_type}'")
            
        self.values = rw.rw_obj_array(self.values, kf_type, self.keyframe_count)
        
        if self.keyframe_type in [26, 27, 28, 31, 32, 33, 34, 35]:
            self.base_position = rw.rw_float32s(self.base_position, 3)
            if self.keyframe_type != 31:
                self.base_scale = rw.rw_float32s(self.base_scale, 3)

# Should probably come up with a different way to organise the r/w of these data..?!
class KeyframeType1(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = None
        self.rotation = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType1] {self.position} {self.rotation}"
        
    def read_write(self, rw):
        self.position = rw.rw_float32s(self.position, 3)
        self.rotation = rw.rw_float32s(self.rotation, 4)

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

class KeyframeType3(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType3] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 3)
        
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

class KeyframeType23(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.camera_fov = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType23] {self.camera_fov}"
    
    def read_write(self, rw):
        self.camera_fov = rw.rw_float32(self.camera_fov)

class KeyframeType24(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_float = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType24] {self.unknown_float}"
    
    def read_write(self, rw):
        self.unknown_float = rw.rw_float32(self.unknown_float)
        
class KeyframeType26(Serializable): # What is different about this one and 28?!
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = None
        self.rotation = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType26] {self.position} {self.rotation}"
        
    def read_write(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
        self.rotation = rw.rw_float16s(self.rotation, 4)
        
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
        self.unknown = rw.rw_float32(self.unknown)
                       
class KeyframeType31(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType31] {self.position}"
        
    def read_write(self, rw):
        self.position = rw.rw_float16s(self.position, 3)

           
class KeyframeType32(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.rotation = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType32] {self.rotation}"
        
    def read_write(self, rw):
        self.rotation = rw.rw_float16s(self.rotation, 4)

         
class KeyframeType33(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.scale = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType33] {self.scale}"
        
    def read_write(self, rw):
        self.scale = rw.rw_float16s(self.scale, 3)

         
class KeyframeType35(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.rotation = None
        self.scale = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType35] {self.rotation} {self.scale}"
        
    def read_write(self, rw):
        self.rotation = rw.rw_float16s(self.rotation, 4)
        self.scale = rw.rw_float16s(self.scale, 3)

        
        
class UnknownAnimationChunk(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.anim_1 = AnimationBinary(endianness)
        self.unknown_1 = None
        self.anim_2 = AnimationBinary(endianness)
        self.unknown_2 = None
        self.anim_3 = AnimationBinary(endianness)
        self.unknown_3 = None
        self.anim_4 = AnimationBinary(endianness)
        self.unknown_4 = None
        
    def __repr__(self):
        return f"[GFDBinary::UnknownAnimationChunk] {self.unknown_1} {self.unknown_2} {self.unknown_3} {self.unknown_4}"
        
    def read_write(self, rw):
        rw.rw_obj(self.anim_1)
        self.unknown_1 = rw.rw_float32(self.unknown_1)
        rw.rw_obj(self.anim_2)
        self.unknown_2 = rw.rw_float32(self.unknown_2)
        rw.rw_obj(self.anim_3)
        self.unknown_3 = rw.rw_float32(self.unknown_3)
        rw.rw_obj(self.anim_4)
        self.unknown_4 = rw.rw_float32(self.unknown_4)
        
        
class AnimationLayer(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.name = ObjectName(endianness)
        self.track = AnimationTrackBinary()
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Layer {safe_format(self.flags, hex32_format)}] {self.name}"
        
    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        rw.rw_obj(self.name)
        rw.rw_obj(self.track)

