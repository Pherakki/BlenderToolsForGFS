class ShaderParametersType1:
    def __init__(self):
        self.ambient_color   = [1.,1.,1.,1.]
        self.diffuse_color   = [1.,1.,1.,1.]
        self.specular_color  = [1.,1.,1.,1.]
        self.emissive_color  = [1.,1.,1.,1.]
        self.reflectivity    = 0
        self.lerp_blend_rate = 0
    
    def exbip_rw(self, rw, version):
        self.ambient_color   = rw.rw_float32s(self.ambient_color, 4)
        self.diffuse_color   = rw.rw_float32s(self.diffuse_color, 4)
        self.specular_color  = rw.rw_float32s(self.specular_color, 4)
        self.emissive_color  = rw.rw_float32s(self.emissive_color, 4)
        self.reflectivity    = rw.rw_float32(self.reflectivity)
        self.lerp_blend_rate = rw.rw_float32(self.lerp_blend_rate)
        
    def tex2Name(self):
        return "Normal Map"
    
    def tex5Name(self):
        return "Multiply Map"
    
    def tex6Name(self):
        return "Emissive Map"
    
    def tex8Name(self):
        return "Toon Params Map"
