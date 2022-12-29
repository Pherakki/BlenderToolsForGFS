from .....serialization.Serializable import Serializable
from .....serialization.utils import safe_format, hex32_format
from ..CommonStructures import ObjectName, PropertyBinary, SizedObjArray, BitVector
from .AnimController import AnimationControllerBinary
from .AnimTrack import AnimationTrackBinary


class ParticlesError(Exception):
    pass


class AnimationPackFlags(BitVector):
    flag_0            = BitVector.DEF_FLAG(0x00)
    flag_1            = BitVector.DEF_FLAG(0x01)
    has_unknown_chunk = BitVector.DEF_FLAG(0x02)
    flag_3            = BitVector.DEF_FLAG(0x03)
    flag_4            = BitVector.DEF_FLAG(0x04)
    flag_5            = BitVector.DEF_FLAG(0x05)
    flag_6            = BitVector.DEF_FLAG(0x06)
    flag_7            = BitVector.DEF_FLAG(0x07)
    flag_8            = BitVector.DEF_FLAG(0x08)
    flag_9            = BitVector.DEF_FLAG(0x09)
    flag_10           = BitVector.DEF_FLAG(0x0A)
    flag_11           = BitVector.DEF_FLAG(0x0B)
    flag_12           = BitVector.DEF_FLAG(0x0C)
    flag_13           = BitVector.DEF_FLAG(0x0D)
    flag_14           = BitVector.DEF_FLAG(0x0E)
    flag_15           = BitVector.DEF_FLAG(0x0F)
    flag_16           = BitVector.DEF_FLAG(0x10)
    flag_17           = BitVector.DEF_FLAG(0x11)
    flag_18           = BitVector.DEF_FLAG(0x12)
    flag_19           = BitVector.DEF_FLAG(0x13)
    flag_20           = BitVector.DEF_FLAG(0x14)
    flag_21           = BitVector.DEF_FLAG(0x15)
    flag_22           = BitVector.DEF_FLAG(0x16)
    flag_23           = BitVector.DEF_FLAG(0x17)
    flag_24           = BitVector.DEF_FLAG(0x18)
    flag_25           = BitVector.DEF_FLAG(0x19)
    flag_26           = BitVector.DEF_FLAG(0x1A)
    flag_27           = BitVector.DEF_FLAG(0x1B)
    flag_28           = BitVector.DEF_FLAG(0x1C)
    flag_29           = BitVector.DEF_FLAG(0x1D)
    flag_30           = BitVector.DEF_FLAG(0x1E)
    flag_31           = BitVector.DEF_FLAG(0x1F)


class AnimationDataBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags              = AnimationPackFlags()
        self.animations         = SizedObjArray(AnimationBinary)
        self.blend_animations   = SizedObjArray(AnimationBinary)
        self.unknown_anim_chunk = None
        
    def __repr__(self):
        return f"[GFDBinary::AnimationData {safe_format(self.flags._value, hex32_format)}] Anims: {self.anim_count} Blend Anims: {self.blend_anim_count} Extra: {safe_format(self.flags, lambda x: bool(x.has_unknown_chunk))}"

    def read_write(self, rw, version):
        self.flags = rw.rw_obj(self.flags)
        rw.rw_obj(self.animations, version)
        rw.rw_obj(self.blend_animations, version)
        
        if self.flags.has_unknown_chunk:
            self.unknown_anim_chunk = rw.rw_new_obj(self.unknown_anim_chunk, UnknownAnimationChunk, version)


class AnimationFlags(BitVector):
    flag_0            = BitVector.DEF_FLAG(0x00)
    flag_1            = BitVector.DEF_FLAG(0x01)
    flag_2            = BitVector.DEF_FLAG(0x02)
    flag_3            = BitVector.DEF_FLAG(0x03)
    flag_4            = BitVector.DEF_FLAG(0x04)
    flag_5            = BitVector.DEF_FLAG(0x05)
    flag_6            = BitVector.DEF_FLAG(0x06)
    flag_7            = BitVector.DEF_FLAG(0x07)
    flag_8            = BitVector.DEF_FLAG(0x08)
    flag_9            = BitVector.DEF_FLAG(0x09)
    flag_10           = BitVector.DEF_FLAG(0x0A)
    flag_11           = BitVector.DEF_FLAG(0x0B)
    flag_12           = BitVector.DEF_FLAG(0x0C)
    flag_13           = BitVector.DEF_FLAG(0x0D)
    flag_14           = BitVector.DEF_FLAG(0x0E)
    flag_15           = BitVector.DEF_FLAG(0x0F)
    flag_16           = BitVector.DEF_FLAG(0x10)
    flag_17           = BitVector.DEF_FLAG(0x11)
    flag_18           = BitVector.DEF_FLAG(0x12)
    flag_19           = BitVector.DEF_FLAG(0x12)
    flag_20           = BitVector.DEF_FLAG(0x14)
    flag_21           = BitVector.DEF_FLAG(0x15)
    flag_22           = BitVector.DEF_FLAG(0x16)
    has_properties    = BitVector.DEF_FLAG(0x17)
    flag_24           = BitVector.DEF_FLAG(0x18)
    has_speed         = BitVector.DEF_FLAG(0x19)
    flag_26           = BitVector.DEF_FLAG(0x1A)
    flag_27           = BitVector.DEF_FLAG(0x1B)
    has_particles     = BitVector.DEF_FLAG(0x1C)
    has_unknown_chunk = BitVector.DEF_FLAG(0x1D)
    has_bounding_box  = BitVector.DEF_FLAG(0x1E)
    has_extra_data    = BitVector.DEF_FLAG(0x1F)


class AnimationBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags       = AnimationFlags()
        self.duration    = None
        self.controllers = SizedObjArray(AnimationControllerBinary)
        
        #self.particle_count = None
        #self.particle_data = ParticleData()
        self.unknown_anim_chunk = None
        self.extra_track_data   = ExtraTrackData()
        # Bounding boxes should probably go into a custom datatype
        self.bounding_box_max_dims = None
        self.bounding_box_min_dims = None
        self.speed = None
        self.properties = SizedObjArray(PropertyBinary)
        
        
    def __repr__(self):
        return f"[GFDBinary::Animation {safe_format(self.flags, hex32_format)}] {self.duration}"

    def read_write(self, rw, version):
        self.flags       = rw.rw_obj(self.flags)
        self.duration    = rw.rw_float32(self.duration)
        self.controllers = rw.rw_obj(self.controllers, version)
        
        # Only certain flags used for certain chunk versions..?
        if self.flags.has_particles:
            # self.particle_count = rw.rw_uint32(self.particle_count)
            # print(self.particle_count)
            # rw.rw_obj(self.particle_data)
            raise ParticlesError()
        if self.flags.has_unknown_chunk:
            self.unknown_anim_chunk = rw.rw_new_obj(self.unknown_anim_chunk, UnknownAnimationChunk, version)
        if self.flags.has_extra_data:
            rw.rw_obj(self.extra_track_data, version)
        if self.flags.has_bounding_box:
            self.bounding_box_max_dims = rw.rw_float32s(self.bounding_box_max_dims, 3)
            self.bounding_box_min_dims = rw.rw_float32s(self.bounding_box_min_dims, 3)
        if self.flags.has_speed:
            self.speed = rw.rw_float32(self.speed)
        if self.flags.has_properties:
            rw.rw_obj(self.properties, version)


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
        return f"[GFDBinary::Animation::UnknownAnimationChunk] {self.unknown_1} {self.unknown_2} {self.unknown_3} {self.unknown_4}"
        
    def read_write(self, rw, version):
        rw.rw_obj(self.anim_1, version)
        self.unknown_1 = rw.rw_float32(self.unknown_1)
        rw.rw_obj(self.anim_2, version)
        self.unknown_2 = rw.rw_float32(self.unknown_2)
        rw.rw_obj(self.anim_3, version)
        self.unknown_3 = rw.rw_float32(self.unknown_3)
        rw.rw_obj(self.anim_4, version)
        self.unknown_4 = rw.rw_float32(self.unknown_4)
        
        
class ExtraTrackData(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.name = ObjectName(endianness)
        self.track = AnimationTrackBinary()
        
    def __repr__(self, version):
        return f"[GFDBinary::Animation::ExtraTrackData {safe_format(self.flags, hex32_format)}] {self.name}"
        
    def read_write(self, rw, version):
        self.flags = rw.rw_uint32(self.flags)
        rw.rw_obj(self.name, version)
        rw.rw_obj(self.track, version)
