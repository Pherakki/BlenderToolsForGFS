class CompatibilityParameterSet:
    def __init__(self):
        self.ambient      = None
        self.diffuse      = None
        self.emissive     = None
        self.specular     = None
        self.reflectivity = 0
        self.outline_idx  = 0
    
    def exbip_rw(self, rw, version):
        self.ambient      = rw.rw_float32s(self.ambient,  4)
        self.diffuse      = rw.rw_float32s(self.diffuse,  4)
        self.emissive     = rw.rw_float32s(self.emissive, 4)
        self.specular     = rw.rw_float32s(self.specular, 4)
        self.reflectivity = rw.rw_float32(self.reflectivity)
        self.outline_idx  = rw.rw_float32(self.outline_idx)
