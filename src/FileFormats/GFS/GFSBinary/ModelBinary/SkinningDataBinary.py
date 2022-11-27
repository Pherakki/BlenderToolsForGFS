from .....serialization.Serializable import Serializable


class SkinningDataBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.bone_count     = None
        self.ibpms          = None
        self.matrix_palette = None
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SkinningData] Bones: {self.bone_count}"
    
    def read_write(self, rw):
        self.bone_count     = rw.rw_uint32(self.bone_count)
        self.ibpms          = rw.rw_float32s(self.ibpms, (self.bone_count, 16))
        self.matrix_palette = rw.rw_uint16s(self.matrix_palette, self.bone_count)
