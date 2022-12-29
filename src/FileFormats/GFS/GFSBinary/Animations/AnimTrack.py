from .....serialization.Serializable import Serializable
from .....serialization.utils import safe_format, hex32_format


class AnimationTrackBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.keyframe_type = None
        self.keyframe_count = None
        self.data = None
        
        self.frames = []
        self.values = []
        
        self.base_position = [1., 1., 1.]
        self.base_scale    = [1., 1., 1.]
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track {safe_format(self.keyframe_type, hex32_format)}] Keyframes: {self.keyframe_count}"

    def read_write(self, rw, version):
        self.keyframe_type  = rw.rw_uint32(self.keyframe_type)
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
        elif self.keyframe_type == 4:
            kf_type = KeyframeType4
        elif self.keyframe_type == 5:
            kf_type = KeyframeType5
        elif self.keyframe_type == 6:
            kf_type = KeyframeType6
        elif self.keyframe_type == 7:
            kf_type = KeyframeType7
        elif self.keyframe_type == 8:
            kf_type = KeyframeType8
        elif self.keyframe_type == 9:
            kf_type = KeyframeType9
        elif self.keyframe_type == 10:
            kf_type = KeyframeType10
        elif self.keyframe_type == 11:
            kf_type = KeyframeType11
        elif self.keyframe_type == 12:
            kf_type = KeyframeType12
        elif self.keyframe_type == 13:
            kf_type = KeyframeType13
        elif self.keyframe_type == 14:
            kf_type = KeyframeType14
        elif self.keyframe_type == 15:
            kf_type = KeyframeType15
        elif self.keyframe_type == 16:
            kf_type = KeyframeType16
        elif self.keyframe_type == 17:
            kf_type = KeyframeType17
        elif self.keyframe_type == 18:
            kf_type = KeyframeType18
        elif self.keyframe_type == 19:
            kf_type = KeyframeType19
        elif self.keyframe_type == 20:
            kf_type = KeyframeType20
        elif self.keyframe_type == 21:
            kf_type = KeyframeType21
        elif self.keyframe_type == 22:
            kf_type = KeyframeType22
        elif self.keyframe_type == 23:
            kf_type = KeyframeType23
        elif self.keyframe_type == 24:
            kf_type = KeyframeType24
        elif self.keyframe_type == 25:
            kf_type = KeyframeType25
        elif self.keyframe_type == 26:
            kf_type = KeyframeType26
        elif self.keyframe_type == 27:
            kf_type = KeyframeType27
        elif self.keyframe_type == 28:
            kf_type = KeyframeType28
        elif self.keyframe_type == 29:
            kf_type = KeyframeType29
        elif self.keyframe_type == 30:
            kf_type = KeyframeType30
        elif self.keyframe_type == 31:
            kf_type = KeyframeType31
        elif self.keyframe_type == 32:
            kf_type = KeyframeType32
        elif self.keyframe_type == 33:
            kf_type = KeyframeType33
        elif self.keyframe_type == 34:
            kf_type = KeyframeType34
        elif self.keyframe_type == 35:
            kf_type = KeyframeType35
        elif self.keyframe_type == 36:
            kf_type = KeyframeType36
        else:
            raise NotImplementedError(f"Unknown Keyframe type: '{self.keyframe_type}'")
            
        self.values = rw.rw_obj_array(self.values, kf_type, self.keyframe_count)
        
        # Flag instead?!
        if self.keyframe_type in [26, 27, 28, 31, 32, 33, 34, 35]:
            self.base_position = rw.rw_float32s(self.base_position, 3)
            if self.keyframe_type != 31:
                self.base_scale = rw.rw_float32s(self.base_scale, 3)


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
        
class KeyframeType4(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.rotation = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType4] {self.rotation}"
        
    def read_write(self, rw):
        self.rotation = rw.rw_float32s(self.unknown, 4)
        
class KeyframeType5(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType5] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
        
class KeyframeType6(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType6] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 3)
        
class KeyframeType7(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType7] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 3)
        
class KeyframeType8(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType8] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 3)
                
class KeyframeType9(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType9] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
        
class KeyframeType10(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.rotation = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType10] {self.rotation}"
        
    def read_write(self, rw):
        self.rotation = rw.rw_float32s(self.unknown, 4)
                        
class KeyframeType11(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType11] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
        
class KeyframeType12(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType12] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 1) # OK
                
class KeyframeType13(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType13] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 5)

class KeyframeType14(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType14] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 3) # Unconfirmed, looks like a scale
                
class KeyframeType15(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType15] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)
                
class KeyframeType16(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType16] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32(self.unknown)

class KeyframeType17(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = None
        self.rotation = None
        self.scale = None
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType17] {self.position} {self.rotation} {self.scale} {self.unknown}"
        
    def read_write(self, rw):
        self.position = rw.rw_float32s(self.position, 3)
        self.rotation = rw.rw_float32s(self.rotation, 4)
        self.scale    = rw.rw_float32s(self.scale, 3)
        self.unknown  = rw.rw_uint8(self.unknown)

class KeyframeType18(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_1 = None
        self.unknown_2 = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType18] {self.unknown_1} {self.unknown_2}"
        
    def read_write(self, rw):
        self.unknown_1 = rw.rw_float32s(self.unknown_1, 4)
        self.unknown_2  = rw.rw_uint8(self.unknown_2)

class KeyframeType19(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_1 = None
        self.unknown_2 = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType19] {self.unknown_1} {self.unknown_2}"
        
    def read_write(self, rw):
        self.unknown_1 = rw.rw_float32(self.unknown_1)
        self.unknown_2  = rw.rw_uint8(self.unknown_2)
                
class KeyframeType20(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType20] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 5)
                
class KeyframeType21(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType21] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 5)
                
class KeyframeType22(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_0x00 = None
        self.unknown_0x04 = None
        self.unknown_0x08 = None
        self.unknown_0x0A = None
        self.unknown_0x0E = None
        self.unknown_0x12 = None
        self.unknown_0x16 = None
        self.unknown_0x1A = None
        self.unknown_0x1C = None
        self.unknown_0x20 = None
        self.unknown_0x24 = None
        self.unknown_0x28 = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType22] {self.unknown_0x00}"
        
    def read_write(self, rw):
        self.unknown_0x00 = rw.rw_uint32(self.unknown_0x00)
        self.unknown_0x04 = rw.rw_uint32(self.unknown_0x04)
        self.unknown_0x08 = rw.rw_uint16(self.unknown_0x08)
        self.unknown_0x0A = rw.rw_float32(self.unknown_0x0A)
        self.unknown_0x0E = rw.rw_float32(self.unknown_0x0E)
        self.unknown_0x12 = rw.rw_float32(self.unknown_0x12)
        self.unknown_0x16 = rw.rw_uint32(self.unknown_0x16)
        self.unknown_0x1A = rw.rw_uint16(self.unknown_0x1A)
        self.unknown_0x1C = rw.rw_float32(self.unknown_0x1C)
        self.unknown_0x20 = rw.rw_float32(self.unknown_0x20)
        self.unknown_0x24 = rw.rw_float32(self.unknown_0x24)
        self.unknown_0x28 = rw.rw_uint8(self.unknown_0x28)

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
        
class KeyframeType25(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_float = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType25] {self.unknown_float}"
    
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
                  
class KeyframeType30(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown_float = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType30] {self.unknown_float}"
    
    def read_write(self, rw):
        self.unknown_float = rw.rw_float32(self.unknown_float)
        
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

             
class KeyframeType34(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.position = None
        self.scale = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType34] {self.position} {self.scale}"
        
    def read_write(self, rw):
        self.position = rw.rw_float16s(self.position, 3)
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
        
class KeyframeType36(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.unknown = None
        
    def __repr__(self):
        return f"[GFDBinary::Animation::Controller::Track::KeyframeType36] {self.unknown}"
        
    def read_write(self, rw):
        self.unknown = rw.rw_float32s(self.unknown, 5)
    