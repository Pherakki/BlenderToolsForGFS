from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format
from ...CommonStructures import ObjectName, SizedObjArray


class MeshBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = 0
        self.vertex_format = 0
        self.tri_count = 0
        self.index_type  = None
        self.vertex_count = None
        self.unknown_0x12 = None
        self.vertices = None
        self.__morph_data = MorphDataBinary()
        self.indices = None
        self.material_name = ObjectName()
        self.bounding_box_max_dims = None
        self.bounding_box_min_dims = None
        self.bounding_sphere_centre = None
        self.bounding_sphere_radius = None
        self.unknown_float_1 = None
        self.unknown_float_2 = None
        
    @property
    def morph_data(self):
        """Read-only property so that the user doesn't override the object"""
        return self.__morph_data
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment::Mesh] {safe_format(self.flags, hex32_format)} {safe_format(self.vertex_format, hex32_format)}"
    
    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        self.vertex_format = rw.rw_uint32(self.vertex_format)
        
        if self.flags & 0x00000004: # Triangles
            self.tri_count  = rw.rw_uint32(self.tri_count)
            self.index_type = rw.rw_uint16(self.index_type)
            
        self.vertex_count = rw.rw_uint32(self.vertex_count)
        self.unknown_0x12 = rw.rw_uint32(self.unknown_0x12)
        
        rw_funcs = []
        if self.vertex_format & 0x00000002: rw_funcs.append(VertexAttributes.rw_position)
        if self.vertex_format & 0x00000010: rw_funcs.append(VertexAttributes.rw_normal)
        if self.vertex_format & 0x10000000: rw_funcs.append(VertexAttributes.rw_tangent)
        if self.vertex_format & 0x20000000: rw_funcs.append(VertexAttributes.rw_binormal)
        if self.vertex_format & 0x00000040: rw_funcs.append(VertexAttributes.rw_color1)
        if self.vertex_format & 0x00000100: rw_funcs.append(VertexAttributes.rw_texcoord0)
        if self.vertex_format & 0x00000200: rw_funcs.append(VertexAttributes.rw_texcoord1)
        if self.vertex_format & 0x00000400: rw_funcs.append(VertexAttributes.rw_texcoord2)
        if self.vertex_format & 0x00000800: rw_funcs.append(VertexAttributes.rw_texcoord3)
        if self.vertex_format & 0x00001000: rw_funcs.append(VertexAttributes.rw_texcoord4)
        if self.vertex_format & 0x00002000: rw_funcs.append(VertexAttributes.rw_texcoord5)
        if self.vertex_format & 0x00004000: rw_funcs.append(VertexAttributes.rw_texcoord6)
        if self.vertex_format & 0x00008000: rw_funcs.append(VertexAttributes.rw_texcoord7)
        if self.vertex_format & 0x40000000: rw_funcs.append(VertexAttributes.rw_color2)
        if self.flags         & 0x00000001: rw_funcs.append(VertexAttributes.rw_weights)
        
        self.vertices = rw.rw_obj_array(self.vertices, VertexBinary, self.vertex_count, rw_funcs)
        
        # Do morphs
        if self.flags & 0x00000040:
            raise NotImplementedError("Mesh morphs are not currently supported")
            rw.rw_obj(self.morph_data) # Can allow this line to be reached once some models with morphs are found
        
        # Do indices
        if self.flags & 0x00000004:
            if self.index_type == 1:
                self.indices = rw.rw_uint16s(self.indices, self.tri_count*3)
            elif self.index_type == 2:
                self.indices = rw.rw_uint32s(self.indices, self.tri_count*3)
            else:
                raise NotImplementedError(f"Unknown Index Type '{self.index_type}'")
                
        # Do materials
        if self.flags & 0x00000002:
            rw.rw_obj(self.material_name)
            
        # Bounding box / sphere
        if self.flags & 0x00000008:
            self.bounding_box_max_dims = rw.rw_float32s(self.bounding_box_max_dims, 3)
            self.bounding_box_min_dims = rw.rw_float32s(self.bounding_box_min_dims, 3)

        if self.flags & 0x00000010:
            self.bounding_sphere_centre = rw.rw_float32s(self.bounding_sphere_centre, 3)
            self.bounding_sphere_radius = rw.rw_float32(self.bounding_sphere_radius)
            
        # Unknown floats
        if self.flags & 0x00001000:
            self.unknown_float_1 = rw.rw_float32(self.unknown_float_1)
            self.unknown_float_2 = rw.rw_float32(self.unknown_float_2)


class VertexAttributes:
    POSITION  = 0
    NORMAL    = 1
    TANGENT   = 2
    BINORMAL  = 3
    COLOR1    = 4
    COLOR2    = 5
    WEIGHTS   = 6
    INDICES   = 7
    TEXCOORD0 = 8
    TEXCOORD1 = 9
    TEXCOORD2 = 10
    TEXCOORD3 = 11
    TEXCOORD4 = 12
    TEXCOORD5 = 13
    TEXCOORD6 = 14
    TEXCOORD7 = 15
    
    @staticmethod
    def rw_position(rw, v):
        v[VertexAttributes.POSITION] = rw.rw_float32s(v[VertexAttributes.POSITION], 3)
    @staticmethod
    def rw_normal(rw, v):
        v[VertexAttributes.NORMAL] = rw.rw_float32s(v[VertexAttributes.NORMAL], 3)
    @staticmethod
    def rw_tangent(rw, v):
        v[VertexAttributes.TANGENT] = rw.rw_float32s(v[VertexAttributes.TANGENT], 3)
    @staticmethod
    def rw_binormal(rw, v):
        v[VertexAttributes.BINORMAL] = rw.rw_float32s(v[VertexAttributes.BINORMAL], 3)
    @staticmethod
    def rw_color1(rw, v):
        v[VertexAttributes.COLOR1] = rw.rw_uint8s(v[VertexAttributes.COLOR1], 4)
    @staticmethod
    def rw_color2(rw, v):
        v[VertexAttributes.COLOR2] = rw.rw_uint8s(v[VertexAttributes.COLOR2], 4)
    @staticmethod
    def rw_weights(rw, v):
        v[VertexAttributes.WEIGHTS] = rw.rw_float32s(v[VertexAttributes.WEIGHTS], 4)
        v[VertexAttributes.INDICES] = rw.rw_uint8s(v[VertexAttributes.INDICES], 4)
    @staticmethod
    def rw_texcoord0(rw, v):
        v[VertexAttributes.TEXCOORD0] = rw.rw_uv(v[VertexAttributes.TEXCOORD0])
    @staticmethod
    def rw_texcoord1(rw, v):
        v[VertexAttributes.TEXCOORD1] = rw.rw_uv(v[VertexAttributes.TEXCOORD1])
    @staticmethod
    def rw_texcoord2(rw, v):
        v[VertexAttributes.TEXCOORD2] = rw.rw_uv(v[VertexAttributes.TEXCOORD2])
    @staticmethod
    def rw_texcoord3(rw, v):
        v[VertexAttributes.TEXCOORD3] = rw.rw_uv(v[VertexAttributes.TEXCOORD3])
    @staticmethod
    def rw_texcoord4(rw, v):
        v[VertexAttributes.TEXCOORD4] = rw.rw_uv(v[VertexAttributes.TEXCOORD4])
    @staticmethod
    def rw_texcoord5(rw, v):
        v[VertexAttributes.TEXCOORD5] = rw.rw_uv(v[VertexAttributes.TEXCOORD5])
    @staticmethod
    def rw_texcoord6(rw, v):
        v[VertexAttributes.TEXCOORD6] = rw.rw_uv(v[VertexAttributes.TEXCOORD6])
    @staticmethod
    def rw_texcoord7(rw, v):
        v[VertexAttributes.TEXCOORD7] = rw.rw_uv(v[VertexAttributes.TEXCOORD7])
    
class VertexBinary(Serializable):
    __slots__ = ("buffer",)
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        self.buffer = [None]*16
        
    def read_write(self, rw, funcs):
        for f in funcs:
            f(rw, self)
            
    def __getitem__(self, idx):
        return self.buffer[idx]
    
    def __setitem__(self, idx, value):
        self.buffer[idx] = value
        
    @property
    def position(self):
        return self.buffer[VertexAttributes.POSITION]
    @position.setter
    def position(self, value):
        self.buffer[VertexAttributes.POSITION] = value
    
    @property
    def normal(self):
        return self.buffer[VertexAttributes.NORMAL]
    @normal.setter
    def normal(self, value):
        self.buffer[VertexAttributes.NORMAL] = value
    
    @property
    def tangent(self):
        return self.buffer[VertexAttributes.TANGENT]
    @tangent.setter
    def tangent(self, value):
        self.buffer[VertexAttributes.TANGENT] = value
    
    @property
    def binormal(self):
        return self.buffer[VertexAttributes.BINORMAL]
    @binormal.setter
    def binormal(self, value):
        self.buffer[VertexAttributes.BINORMAL] = value

    @property
    def color1(self):
        return self.buffer[VertexAttributes.COLOR1]
    @color1.setter
    def color1(self, value):
        self.buffer[VertexAttributes.COLOR1] = value
    
    @property
    def color2(self):
        return self.buffer[VertexAttributes.COLOR2]
    @color2.setter
    def color2(self, value):
        self.buffer[VertexAttributes.COLOR2] = value
    
    @property
    def weights(self):
        return self.buffer[VertexAttributes.WEIGHTS]
    @weights.setter
    def weights(self, value):
        self.buffer[VertexAttributes.WEIGHTS] = value
    
    @property
    def indices(self):
        return self.buffer[VertexAttributes.INDICES]
    @indices.setter
    def indices(self, value):
        self.buffer[VertexAttributes.INDICES] = value
    
    @property
    def texcoord0(self):
        return self.buffer[VertexAttributes.TEXCOORD0]
    @texcoord0.setter
    def texcoord0(self, value):
        self.buffer[VertexAttributes.TEXCOORD0] = value
    
    @property
    def texcoord1(self):
        return self.buffer[VertexAttributes.TEXCOORD1]
    @texcoord1.setter
    def texcoord1(self, value):
        self.buffer[VertexAttributes.TEXCOORD1] = value
    
    @property
    def texcoord2(self):
        return self.buffer[VertexAttributes.TEXCOORD2]
    @texcoord2.setter
    def texcoord2(self, value):
        self.buffer[VertexAttributes.TEXCOORD2] = value
    
    @property
    def texcoord3(self):
        return self.buffer[VertexAttributes.TEXCOORD3]
    @texcoord3.setter
    def texcoord3(self, value):
        self.buffer[VertexAttributes.TEXCOORD3] = value
    
    @property
    def texcoord4(self):
        return self.buffer[VertexAttributes.TEXCOORD4]
    @texcoord4.setter
    def texcoord4(self, value):
        self.buffer[VertexAttributes.TEXCOORD4] = value
    
    @property
    def texcoord5(self):
        return self.buffer[VertexAttributes.TEXCOORD5]
    @texcoord5.setter
    def texcoord5(self, value):
        self.buffer[VertexAttributes.TEXCOORD5] = value
    
    @property
    def texcoord6(self):
        return self.buffer[VertexAttributes.TEXCOORD6]
    @texcoord6.setter
    def texcoord6(self, value):
        self.buffer[VertexAttributes.TEXCOORD6] = value
    
    @property
    def texcoord7(self):
        return self.buffer[VertexAttributes.TEXCOORD7]
    @texcoord7.setter
    def texcoord7(self, value):
        self.buffer[VertexAttributes.TEXCOORD7] = value

class MorphDataBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.count = None
        self.targets = []
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment::Mesh::MorphData] {safe_format(self.flags, hex32_format)}"
    
    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        self.count = rw.rw_uint32(self.count)
        self.targets = rw.rw_obj_array(self.targets, MorphTarget, self.count)

def MorphTarget(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = None
        self.count = None
        self.position_deltas = []
           
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment::Mesh::MorphData::Target] {safe_format(self.flags, hex32_format)} {self.count}"
    
    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        self.count = rw.rw_uint32(self.count)
        self.position_deltas = rw.rw_float32s(self.position_deltas, (self.count, 3))