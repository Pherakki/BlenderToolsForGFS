from ....CommonStructures import BitVector0x20


class WaterShaderParametersFlags(BitVector0x20):
    influenced_by_sky           = BitVector0x20.DEF_FLAG(0x00)
    has_water_reflection        = BitVector0x20.DEF_FLAG(0x01)
    is_infinite                 = BitVector0x20.DEF_FLAG(0x02)
    outline_attenuation_invalid = BitVector0x20.DEF_FLAG(0x03)


class WaterShaderParameters:
    def __init__(self):
        self.unknown_0x00             = 0
        self.unknown_0x04             = 0
        self.tc_scale                 = 0.
        self.unknown_0x0C             = 0.
        
        self.ocean_depth_scale        = 0.
        self.disturbance_camera_scale = 0.
        self.disturbance_depth_scale  = 0.
        self.scattering_camera_scale  = 0.
        
        self.disturbance_tolerance    = 0.
        self.foam_distance            = 0.
        self.caustics_tolerance       = 0.
        self.unknown_0x2C             = 0.
        self.texture_anim_speed       = 0.
        
        self.unknown_0x34             = 0.
        self.flags                    = WaterShaderParametersFlags()
    
    def exbip_rw(self, rw, version):
        self.unknown_0x00             = rw.rw_float32(self.unknown_0x00)
        self.unknown_0x04             = rw.rw_float32(self.unknown_0x04)
        self.tc_scale                 = rw.rw_float32(self.tc_scale)
        self.unknown_0x0C             = rw.rw_float32(self.unknown_0x0C)
        
        self.ocean_depth_scale        = rw.rw_float32(self.ocean_depth_scale)
        self.disturbance_camera_scale = rw.rw_float32(self.disturbance_camera_scale)
        self.disturbance_depth_scale = rw.rw_float32(self.disturbance_depth_scale)
        self.scattering_camera_scale  = rw.rw_float32(self.scattering_camera_scale)
        
        self.disturbance_tolerance    = rw.rw_float32(self.disturbance_tolerance)
        self.foam_distance            = rw.rw_float32(self.foam_distance)
        self.caustics_tolerance       = rw.rw_float32(self.caustics_tolerance)
        
        if version >= 0x02110182:
            self.unknown_0x2C         = rw.rw_float32(self.unknown_0x2C)
            self.texture_anim_speed   = rw.rw_float32(self.texture_anim_speed)
        if version >= 0x02110205:
            self.unknown_0x34         = rw.rw_float32(self.unknown_0x34)
        if version >= 0x02110188:
            self.flags                = rw.rw_obj(self.flags)
