from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format
from ...CommonStructures import ObjectName, BitVector
from ...CommonStructures.SizedObjArrayModule import SizedObjArray


class MeshFlags(BitVector):
    has_weights         = BitVector.DEF_FLAG(0x00)
    has_material        = BitVector.DEF_FLAG(0x01)
    has_indices         = BitVector.DEF_FLAG(0x02)
    has_bounding_box    = BitVector.DEF_FLAG(0x03)
    has_bounding_sphere = BitVector.DEF_FLAG(0x04)
    flag_5              = BitVector.DEF_FLAG(0x05)
    has_morphs          = BitVector.DEF_FLAG(0x06)
    flag_7              = BitVector.DEF_FLAG(0x07)
    flag_8              = BitVector.DEF_FLAG(0x08)
    flag_9              = BitVector.DEF_FLAG(0x09)
    flag_10             = BitVector.DEF_FLAG(0x0A)
    flag_11             = BitVector.DEF_FLAG(0x0B)
    has_unknown_floats  = BitVector.DEF_FLAG(0x0C)
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


class VertexFormat(BitVector):
    flag_0            = BitVector.DEF_FLAG(0x00)
    has_positions     = BitVector.DEF_FLAG(0x01)
    flag_2            = BitVector.DEF_FLAG(0x02)
    flag_3            = BitVector.DEF_FLAG(0x03)
    has_normals       = BitVector.DEF_FLAG(0x04)
    flag_5            = BitVector.DEF_FLAG(0x05)
    has_color1        = BitVector.DEF_FLAG(0x06)
    flag_7            = BitVector.DEF_FLAG(0x07)
    has_texcoord_0    = BitVector.DEF_FLAG(0x08)
    has_texcoord_1    = BitVector.DEF_FLAG(0x09)
    has_texcoord_2    = BitVector.DEF_FLAG(0x0A)
    has_texcoord_3    = BitVector.DEF_FLAG(0x0B)
    has_texcoord_4    = BitVector.DEF_FLAG(0x0C)
    has_texcoord_5    = BitVector.DEF_FLAG(0x0D)
    has_texcoord_6    = BitVector.DEF_FLAG(0x0E)
    has_texcoord_7    = BitVector.DEF_FLAG(0x0F)
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
    has_tangents      = BitVector.DEF_FLAG(0x1C)
    has_binormals     = BitVector.DEF_FLAG(0x1D)
    has_color2        = BitVector.DEF_FLAG(0x1E)
    flag_31           = BitVector.DEF_FLAG(0x1F)
    
    
class MeshBinary(Serializable):
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = MeshFlags(endianness)
        self.vertex_format = VertexFormat(endianness)
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
        return f"[GFD::SceneContainer::SceneNode::Attachment::Mesh] {safe_format(self.flags._value, hex32_format)} {safe_format(self.vertex_format._value, hex32_format)}"
    
    def read_write(self, rw, version):
        self.flags         = rw.rw_obj(self.flags)
        self.vertex_format = rw.rw_obj(self.vertex_format)
        
        if self.flags.has_indices: # Triangles
            self.tri_count  = rw.rw_uint32(self.tri_count)
            self.index_type = rw.rw_uint16(self.index_type)
        
        self.vertex_count = rw.rw_uint32(self.vertex_count)
        self.unknown_0x12 = rw.rw_uint32(self.unknown_0x12)
        
        rw_funcs = []
        if self.vertex_format.has_positions:  rw_funcs.append(VertexAttributes.rw_position)
        if self.vertex_format.has_normals:    rw_funcs.append(VertexAttributes.rw_normal)
        if self.vertex_format.has_tangents:   rw_funcs.append(VertexAttributes.rw_tangent)
        if self.vertex_format.has_binormals:  rw_funcs.append(VertexAttributes.rw_binormal)
        if self.vertex_format.has_color1:     rw_funcs.append(VertexAttributes.rw_color1)
        if self.vertex_format.has_texcoord_0: rw_funcs.append(VertexAttributes.rw_texcoord0)
        if self.vertex_format.has_texcoord_1: rw_funcs.append(VertexAttributes.rw_texcoord1)
        if self.vertex_format.has_texcoord_2: rw_funcs.append(VertexAttributes.rw_texcoord2)
        if self.vertex_format.has_texcoord_3: rw_funcs.append(VertexAttributes.rw_texcoord3)
        if self.vertex_format.has_texcoord_4: rw_funcs.append(VertexAttributes.rw_texcoord4)
        if self.vertex_format.has_texcoord_5: rw_funcs.append(VertexAttributes.rw_texcoord5)
        if self.vertex_format.has_texcoord_6: rw_funcs.append(VertexAttributes.rw_texcoord6)
        if self.vertex_format.has_texcoord_7: rw_funcs.append(VertexAttributes.rw_texcoord7)
        if self.vertex_format.has_color2:     rw_funcs.append(VertexAttributes.rw_color2)
        if self.flags.has_weights:            rw_funcs.append(VertexAttributes.rw_weights)
        
        self.vertices = rw.rw_obj_array(self.vertices, VertexBinary, self.vertex_count, rw_funcs)
        
        # Do morphs
        if self.flags.has_morphs:
            rw.rw_obj(self.morph_data)
        
        # Do indices
        if self.flags.has_indices:
            if self.index_type == 1:
                self.indices = rw.rw_uint16s(self.indices, self.tri_count*3)
            elif self.index_type == 2:
                self.indices = rw.rw_uint32s(self.indices, self.tri_count*3)
            else:
                raise NotImplementedError(f"Unknown Index Type '{self.index_type}'")
                
        # Do materials
        if self.flags.has_material:
            rw.rw_obj(self.material_name, version)
        
        # Bounding box / sphere
        if self.flags.has_bounding_box:
            self.bounding_box_max_dims = rw.rw_float32s(self.bounding_box_max_dims, 3)
            self.bounding_box_min_dims = rw.rw_float32s(self.bounding_box_min_dims, 3)
        
        if self.flags.has_bounding_sphere:
            self.bounding_sphere_centre = rw.rw_float32s(self.bounding_sphere_centre, 3)
            self.bounding_sphere_radius = rw.rw_float32(self.bounding_sphere_radius)
        
        # Unknown floats
        if self.flags.has_unknown_floats:
            self.unknown_float_1 = rw.rw_float32(self.unknown_float_1)
            self.unknown_float_2 = rw.rw_float32(self.unknown_float_2)

    def calc_bounding_box(self):
        if not len(self.vertices):
            min_dims = [0, 0, 0]
            max_dims = [0, 0, 0]
        elif self.vertices[0].position is None:
            min_dims = [0, 0, 0]
            max_dims = [0, 0, 0]
        else:
            max_dims = [*self.vertices[0].position]
            min_dims = [*self.vertices[0].position]
                    
            for v in self.vertices:
                pos = v.position
                for i in range(3):
                    max_dims[i] = max(max_dims[i], pos[i])
                    min_dims[i] = min(min_dims[i], pos[i])
        
        return min_dims, max_dims
    
    def calc_bounding_sphere(self):
        if not len(self.vertices):
            center = [0, 0, 0]
            radius = 0
        elif self.vertices[0].position is None:
            center = [0, 0, 0]
            radius = 0
        else:
            # This isn't *exactly* right, but close enough in most cases
            center = [sum(v.position[i] for v in self.vertices)/len(self.vertices) for i in range(3)]
            radius = 0.
            for v in self.vertices:
                pos = v.position
                dist = (p-c for p, c in zip(pos, center))
                radius = max(sum(d*d for d in dist), radius)
            radius = radius**.5
        
        return center, radius
    
    def autocalc_bounding_box(self):
        self.bounding_box_min_dims, self.bounding_box_max_dims   = self.calc_bounding_box()
    
    def autocalc_bounding_sphere(self):
        self.bounding_sphere_centre, self.bounding_sphere_radius = self.calc_bounding_sphere()


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
        
        self.flags = 2
        self.count = 0
        self.targets = []
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment::Mesh::MorphData] {safe_format(self.flags, hex32_format)}"
    
    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        self.count = rw.rw_uint32(self.count)
        self.targets = rw.rw_obj_array(self.targets, MorphTarget, self.count)
        
    def add_target(self, flags, position_deltas):
        target = MorphTarget(self.context.endianness)
        target.flags = 2
        target.count = len(position_deltas)
        target.position_deltas = position_deltas
        self.targets.append(target)
        self.count += 1
        return target

class MorphTarget(Serializable):
    def __init__(self, endianness=">"):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags = 2
        self.count = 0
        self.position_deltas = []
           
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment::Mesh::MorphData::Target] {safe_format(self.flags, hex32_format)} {self.count}"
    
    def read_write(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        self.count = rw.rw_uint32(self.count)
        self.position_deltas = rw.rw_float32s(self.position_deltas, (self.count, 3))
