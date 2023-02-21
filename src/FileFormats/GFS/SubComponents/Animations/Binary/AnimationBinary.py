from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format
from ...CommonStructures.SceneNode.EPL import EPLBinary
from ...CommonStructures import ObjectName, PropertyBinary, BitVector
from ...CommonStructures.SizedObjArrayModule import SizedObjArray
from .AnimController import AnimationControllerBinary
from .AnimTrack import AnimationTrackBinary


class ParticlesError(Exception):
    pass


class AnimationFlags(BitVector):
    has_node_anims     = BitVector.DEF_FLAG(0x00) # USED (Normal, Blend, Unk)
    has_material_anims = BitVector.DEF_FLAG(0x01) # USED (Normal, Blend, Unk)
    has_camera_anims   = BitVector.DEF_FLAG(0x02) # USED (Normal)
    has_morph_anims    = BitVector.DEF_FLAG(0x03) # USED (Normal, Blend)
    has_type_5_anims   = BitVector.DEF_FLAG(0x04) # USED
    flag_5             = BitVector.DEF_FLAG(0x05)
    flag_6             = BitVector.DEF_FLAG(0x06)
    flag_7             = BitVector.DEF_FLAG(0x07)
    flag_8             = BitVector.DEF_FLAG(0x08)
    flag_9             = BitVector.DEF_FLAG(0x09)
    flag_10            = BitVector.DEF_FLAG(0x0A)
    flag_11            = BitVector.DEF_FLAG(0x0B)
    flag_12            = BitVector.DEF_FLAG(0x0C)
    flag_13            = BitVector.DEF_FLAG(0x0D)
    flag_14            = BitVector.DEF_FLAG(0x0E)
    flag_15            = BitVector.DEF_FLAG(0x0F)
    flag_16            = BitVector.DEF_FLAG(0x10)
    flag_17            = BitVector.DEF_FLAG(0x11)
    flag_18            = BitVector.DEF_FLAG(0x12)
    flag_19            = BitVector.DEF_FLAG(0x12)
    flag_20            = BitVector.DEF_FLAG(0x14)
    flag_21            = BitVector.DEF_FLAG(0x15)
    flag_22            = BitVector.DEF_FLAG(0x16)
    has_properties     = BitVector.DEF_FLAG(0x17) # USED (Normal)
    flag_24            = BitVector.DEF_FLAG(0x18)
    has_speed          = BitVector.DEF_FLAG(0x19) # USED (Normal, Blend)
    flag_26            = BitVector.DEF_FLAG(0x1A) # USED (Blend)
    flag_27            = BitVector.DEF_FLAG(0x1B)
    has_particles      = BitVector.DEF_FLAG(0x1C)
    has_lookat_anims   = BitVector.DEF_FLAG(0x1D) # USED (Normal)
    has_bounding_box   = BitVector.DEF_FLAG(0x1E) # USED (Normal, Blend, Unk)
    has_extra_data     = BitVector.DEF_FLAG(0x1F) # USED (Normal)


class AnimationBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags       = AnimationFlags()
        self.duration    = None
        self.controllers = SizedObjArray(AnimationControllerBinary)
        
        self.particle_data = SizedObjArray(EPLEntry, endianness)
        self.lookat_animations = None
        self.extra_track_data   = None
        # Bounding boxes should probably go into a custom datatype
        self.bounding_box_max_dims = None
        self.bounding_box_min_dims = None
        self.speed = None
        self.properties = SizedObjArray(PropertyBinary)
        
        
    def __repr__(self):
        return f"[GFDBinary::Animation {safe_format(self.flags._value, hex32_format)}] {self.duration}"

    def read_write(self, rw, version):
        if version > 0x01104110:
            self.flags   = rw.rw_obj(self.flags)
        self.duration    = rw.rw_float32(self.duration)
        self.controllers = rw.rw_obj(self.controllers, version)
        # Only certain flags used for certain chunk versions..?
        if self.flags.has_particles:
            rw.rw_obj(self.particle_data, version)
        if self.flags.has_lookat_anims:
            self.lookat_animations = rw.rw_new_obj(self.lookat_animations, LookAtAnimationsBinary, version)
        if self.flags.has_extra_data:
            self.extra_track_data = rw.rw_new_obj(self.extra_track_data, ExtraTrackData, version)
        if self.flags.has_bounding_box:
            self.bounding_box_max_dims = rw.rw_float32s(self.bounding_box_max_dims, 3)
            self.bounding_box_min_dims = rw.rw_float32s(self.bounding_box_min_dims, 3)
        if self.flags.has_speed:
            self.speed = rw.rw_float32(self.speed)
        if self.flags.has_properties:
            rw.rw_obj(self.properties, version)


class EPLEntry(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.epl = EPLBinary.EPLBinary(endianness)
        self.name = ObjectName(endianness)
        
    def read_write(self, rw, version):
        rw.rw_obj(self.epl, version)
        rw.rw_obj(self.name, version)


class LookAtAnimationsBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.right        = AnimationBinary(endianness)
        self.right_factor = None
        self.left         = AnimationBinary(endianness)
        self.left_factor  = None
        self.up           = AnimationBinary(endianness)
        self.up_factor    = None
        self.down         = AnimationBinary(endianness)
        self.down_factor  = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::LookAtAnimationsBinary] {self.right_factor} {self.left_factor} {self.up_factor} {self.down_factor}"
        
    def read_write(self, rw, version):
        rw.rw_obj(self.right, version)
        self.right_factor = rw.rw_float32(self.right_factor)
        rw.rw_obj(self.left, version)
        self.left_factor  = rw.rw_float32(self.left_factor)
        rw.rw_obj(self.up, version)
        self.up_factor    = rw.rw_float32(self.up_factor)
        rw.rw_obj(self.down, version)
        self.down_factor  = rw.rw_float32(self.down_factor)
        
        
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

