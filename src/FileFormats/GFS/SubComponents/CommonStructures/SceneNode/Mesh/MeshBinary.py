import array
import struct

from .......serialization.formatters import HEX32_formatter
from ....CommonStructures.BitVectorModule     import BitVector0x20
from ....CommonStructures.ObjectNameModule    import ObjectName
from ....CommonStructures.SizedObjArrayModule import SizedObjArray


class MeshFlags(BitVector0x20):
    has_weights         = BitVector0x20.DEF_FLAG(0x00)
    has_material        = BitVector0x20.DEF_FLAG(0x01)
    has_indices         = BitVector0x20.DEF_FLAG(0x02)
    has_bounding_box    = BitVector0x20.DEF_FLAG(0x03)
    has_bounding_sphere = BitVector0x20.DEF_FLAG(0x04)
    has_morphs          = BitVector0x20.DEF_FLAG(0x06)
    has_unknown_floats  = BitVector0x20.DEF_FLAG(0x0C)


class VertexFormat:
    def __init__(self):
        self.has_positions = False
        self.has_normals   = False
        self.has_tangents  = False
        self.has_binormals = False
        self.has_texcoord0 = False
        self.has_texcoord1 = False
        self.has_texcoord2 = False
        self.has_color0    = False
        self.has_color1    = False

    def exbip_rw(self, rw, version):
        rw.rw_descriptor(VertexFormatDescriptor, self, version)
        return self
    
    def from_uint(self, buf, version):
        self.has_positions  = (buf & 0x00000002) != 0
        self.has_normals    = (buf & 0x00000010) != 0
        self.has_tangents   = (buf & 0x10000000) != 0
        self.has_binormals  = (buf & 0x20000000) != 0
        self.has_texcoord0  = (buf & 0x00000100) != 0
        self.has_texcoord1  = (buf & 0x00000200) != 0
        self.has_texcoord2  = (buf & 0x00000400) != 0
        self.has_color0     = (buf & 0x00000040) != 0
        if version >= 0x02000000:
            self.has_color1 = (buf & 0x00000800) != 0
        else:
            self.has_color1 = (buf & 0x40000000) != 0
        
        if buf - self.as_uint(version) != 0:
            raise ValueError("Missed flags when constructing vertex format")
    
    def as_uint(self, version):
        buf = 0
        buf |= (self.has_positions  << 0x01)
        buf |= (self.has_normals    << 0x04)
        buf |= (self.has_tangents   << 0x1C)
        buf |= (self.has_binormals  << 0x1D)
        buf |= (self.has_texcoord0  << 0x08)
        buf |= (self.has_texcoord1  << 0x09)
        buf |= (self.has_texcoord2  << 0x0A)
        buf |= (self.has_color0     << 0x06)
        if version >= 0x02000000:    
            buf |= (self.has_color1 << 0x0B)
        else:
            buf |= (self.has_color1 << 0x1E)
        return buf

    
class MeshBinary:
    def __init__(self):
        self.flags = MeshFlags()
        self.vertex_format = VertexFormat()
        self.tri_count = 0
        self.index_type  = None
        self.vertex_count = None
        self.stride_type  = 3
        self.unknown_0x12 = 0
        self.weight_count = 0
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
        return f"[GFD::SceneContainer::SceneNode::Attachment::Mesh] {HEX32_formatter(self.flags._value)} {HEX32_formatter(self.vertex_format.as_uint())}"
    
    def exbip_rw(self, rw, version):
        self.flags         = rw.rw_obj(self.flags)
        self.vertex_format = rw.rw_obj(self.vertex_format, version)
        
        if self.flags.has_indices: # Triangles
            self.tri_count  = rw.rw_uint32(self.tri_count)
            self.index_type = rw.rw_uint16(self.index_type)
        
        self.vertex_count = rw.rw_uint32(self.vertex_count)
        if version > 0x02110205:
            self.stride_type = rw.rw_uint8(self.stride_type)
            
        if version > 0x01103020:
            self.unknown_0x12 = rw.rw_uint32(self.unknown_0x12)
        
        rw_funcs = []
        if version < 0x02000000:
            if self.vertex_format.has_positions: rw_funcs.append(VertexAttributes.rw_position)
            if self.vertex_format.has_normals:   rw_funcs.append(VertexAttributes.rw_normal)
            if self.vertex_format.has_tangents:  rw_funcs.append(VertexAttributes.rw_tangent)
            if self.vertex_format.has_binormals: rw_funcs.append(VertexAttributes.rw_binormal)
            if self.vertex_format.has_color0:    rw_funcs.append(VertexAttributes.rw_color0)
            if self.vertex_format.has_texcoord0: rw_funcs.append(VertexAttributes.rw_texcoord0_v1)
            if self.vertex_format.has_texcoord1: rw_funcs.append(VertexAttributes.rw_texcoord1_v1)
            if self.vertex_format.has_texcoord2: rw_funcs.append(VertexAttributes.rw_texcoord2_v1)
            if self.vertex_format.has_color1:    rw_funcs.append(VertexAttributes.rw_color1)
            if self.flags.has_weights:           rw_funcs.append(VertexAttributes.rw_weights_v1)
        else:
            if self.vertex_format.has_positions: rw_funcs.append(VertexAttributes.rw_position)
            if self.vertex_format.has_texcoord0: rw_funcs.append(VertexAttributes.rw_texcoord0_v2)
            if self.vertex_format.has_normals:   rw_funcs.append(VertexAttributes.rw_normal)
            if self.vertex_format.has_tangents:  rw_funcs.append(VertexAttributes.rw_tangent)
            if self.vertex_format.has_binormals: rw_funcs.append(VertexAttributes.rw_binormal)
            if self.vertex_format.has_texcoord1: rw_funcs.append(VertexAttributes.rw_texcoord1_v2)
            if self.vertex_format.has_texcoord2: rw_funcs.append(VertexAttributes.rw_texcoord2_v2)
            if self.vertex_format.has_color0:    rw_funcs.append(VertexAttributes.rw_color0)
            if self.vertex_format.has_color1:    rw_funcs.append(VertexAttributes.rw_color1)
            if self.flags.has_weights:           
                if    version <= 0x02040000:     rw_funcs.append(VertexAttributes.rw_weights_v1)
                else:                            rw_funcs.append(VertexAttributes.rw_weights_v2)
        self.vertices = rw.rw_dynamic_objs(self.vertices, VertexBinary, self.vertex_count, rw_funcs)

        # # Could speed things up, currently writes wrong values
        # self.vertices = rw.rw_descriptor(VerticesDescriptor, self.vertices, self.vertex_count, self.vertex_format, self.flags, version)
        
        if self.flags.has_weights and version >= 0x02110213:
            self.weight_count = rw.rw_uint8(self.weight_count)
        
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
            vs = [self.vertices[i] for i in self.indices]
            center = [sum(v.position[i] for v in vs)/len(vs) for i in range(3)]
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
    COLOR0    = 4
    COLOR1    = 5
    WEIGHTS   = 6
    INDICES   = 7
    TEXCOORD0 = 8
    TEXCOORD1 = 9
    TEXCOORD2 = 10
    
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
    def rw_color0(rw, v):
        v[VertexAttributes.COLOR0] = rw.rw_uint8s(v[VertexAttributes.COLOR0], 4)
    @staticmethod
    def rw_color1(rw, v):
        v[VertexAttributes.COLOR1] = rw.rw_uint8s(v[VertexAttributes.COLOR1], 4)
    @staticmethod
    def rw_weights_v1(rw, v):
        v[VertexAttributes.WEIGHTS] = rw.rw_padded_float32s(v[VertexAttributes.WEIGHTS], 4)
        v[VertexAttributes.INDICES] = rw.rw_uint8vector32(v[VertexAttributes.INDICES])
        # v[VertexAttributes.INDICES] = rw.rw_padded_uint8s(v[VertexAttributes.INDICES], 4)
    @staticmethod
    def rw_weights_v2(rw, v):
        v[VertexAttributes.WEIGHTS] = rw.rw_padded_unit_intervals16(v[VertexAttributes.WEIGHTS], 8)
        v[VertexAttributes.INDICES] = rw.rw_padded_uint16s(v[VertexAttributes.INDICES], 8)
    @staticmethod
    def rw_texcoord0_v1(rw, v):
        v[VertexAttributes.TEXCOORD0] = rw.rw_uv_v1(v[VertexAttributes.TEXCOORD0])
    @staticmethod
    def rw_texcoord1_v1(rw, v):
        v[VertexAttributes.TEXCOORD1] = rw.rw_uv_v1(v[VertexAttributes.TEXCOORD1])
    @staticmethod
    def rw_texcoord2_v1(rw, v):
        v[VertexAttributes.TEXCOORD2] = rw.rw_uv_v1(v[VertexAttributes.TEXCOORD2])
    @staticmethod
    def rw_texcoord0_v2(rw, v):
        v[VertexAttributes.TEXCOORD0] = rw.rw_uv_v2(v[VertexAttributes.TEXCOORD0])
    @staticmethod
    def rw_texcoord1_v2(rw, v):
        v[VertexAttributes.TEXCOORD1] = rw.rw_uv_v2(v[VertexAttributes.TEXCOORD1])
    @staticmethod
    def rw_texcoord2_v2(rw, v):
        v[VertexAttributes.TEXCOORD2] = rw.rw_uv_v2(v[VertexAttributes.TEXCOORD2])
    
class VertexBinary:
    __slots__ = ("buffer",)
    def __init__(self):
        self.buffer = [None]*16
        
    def exbip_rw(self, rw, funcs):
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
    def color0(self):
        return self.buffer[VertexAttributes.COLOR0]
    @color0.setter
    def color0(self, value):
        self.buffer[VertexAttributes.COLOR0] = value
    
    @property
    def color1(self):
        return self.buffer[VertexAttributes.COLOR1]
    @color1.setter
    def color1(self, value):
        self.buffer[VertexAttributes.COLOR1] = value
    
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


class MorphDataBinary:
    def __init__(self):
        self.flags = 2
        self.count = 0
        self.targets = []
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment::Mesh::MorphData] {HEX32_formatter(self.flags)}"
    
    def exbip_rw(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        rw.assert_equal(self.flags, 2)
        self.count = rw.rw_uint32(self.count)
        self.targets = rw.rw_dynamic_objs(self.targets, MorphTarget, self.count)
        
    def add_target(self, position_deltas):
        target = MorphTarget()
        target.flags = 2
        target.count = len(position_deltas)
        target.position_deltas = position_deltas
        self.targets.append(target)
        self.count += 1
        return target

class MorphTarget:
    def __init__(self):
        self.flags = 2
        self.count = 0
        self.position_deltas = []
           
        
    def __repr__(self):
        return f"[GFD::SceneContainer::SceneNode::Attachment::Mesh::MorphData::Target] {HEX32_formatter(self.flags)} {self.count}"
    
    def exbip_rw(self, rw):
        self.flags = rw.rw_uint32(self.flags)
        rw.assert_equal(self.flags, 2)
        self.count = rw.rw_uint32(self.count)
        self.position_deltas = rw.rw_float32s(self.position_deltas, (self.count, 3))



class VertexFormatDescriptor:
    def deserialize(rw, value, version):
        value.from_uint(rw.rw_uint32(None), version)
    
    def serialize(rw, value, version):
        rw.rw_uint32(value.as_uint(version))
    
    def count(rw, value, version):
        rw.advance_offset(4)

def calc_vertex_size(vertex_format, flags, version):
    vsize = 0
    if version < 0x02000000:
        if vertex_format.has_positions: vsize += 4*3
        if vertex_format.has_normals:   vsize += 4*3
        if vertex_format.has_tangents:  vsize += 4*3
        if vertex_format.has_binormals: vsize += 4*3
        if vertex_format.has_color0:    vsize += 4
        if vertex_format.has_texcoord0: vsize += 4*2
        if vertex_format.has_texcoord1: vsize += 4*2
        if vertex_format.has_texcoord2: vsize += 4*2
        if vertex_format.has_color1:    vsize += 4
        if flags.has_weights:      vsize += 5*4
    else:
        if vertex_format.has_positions: vsize += 4*3
        if vertex_format.has_texcoord0: vsize += 2*2
        if vertex_format.has_normals:   vsize += 4*3
        if vertex_format.has_tangents:  vsize += 4*3
        if vertex_format.has_binormals: vsize += 4*3
        if vertex_format.has_texcoord1: vsize += 2*2
        if vertex_format.has_texcoord2: vsize += 2*2
        if vertex_format.has_color0:    vsize += 4
        if vertex_format.has_color1:    vsize += 4
        if flags.has_weights:           
            if    version <= 0x02040000:     vsize += 5*4
            else:                            vsize += 8*4
    
    return vsize


unpack_vec3_le  = struct.Struct('<fff').unpack
unpack_uv_v1_le = struct.Struct('<ff').unpack
unpack_uv_v2_le = struct.Struct('<ee').unpack
unpack_color_le = struct.Struct('<BBBB').unpack
unpack_wgt_le   = struct.Struct('<HHHHHHHH').unpack

unpack_vec3_be  = struct.Struct('>fff').unpack
unpack_uv_v1_be = struct.Struct('>ff').unpack
unpack_uv_v2_be = struct.Struct('>ee').unpack
unpack_color_be = struct.Struct('>BBBB').unpack
unpack_wgt_be   = struct.Struct('>HHHHHHHH').unpack

pack_vec3_le  = struct.Struct('<fff').pack
pack_uv_v1_le = struct.Struct('<ff').pack
pack_uv_v2_le = struct.Struct('<ee').pack
pack_color_le = struct.Struct('<BBBB').pack
pack_wgt_le   = struct.Struct('<HHHHHHHH').pack

pack_vec3_be  = struct.Struct('>fff').pack
pack_uv_v1_be = struct.Struct('>ff').pack
pack_uv_v2_be = struct.Struct('>ee').pack
pack_color_be = struct.Struct('>BBBB').pack
pack_wgt_be   = struct.Struct('>HHHHHHHH').pack

class VerticesDescriptor:    
    def deserialize(rw, value, vertex_count, vertex_format, flags, version):
        if rw.endianness == ">":
            unpack_vec3  = unpack_vec3_be
            unpack_uv_v1 = unpack_uv_v1_be
            unpack_uv_v2 = unpack_uv_v2_be
            unpack_color = unpack_color_be
            unpack_wgt   = unpack_wgt_be
        elif rw.endianness == "<":
            unpack_vec3  = unpack_vec3_le
            unpack_uv_v1 = unpack_uv_v1_le
            unpack_uv_v2 = unpack_uv_v2_le
            unpack_color = unpack_color_le
            unpack_wgt   = unpack_wgt_le
        else:
            raise ValueError(f"Unknown endianness: {rw.endianness}")
        
        vsize = calc_vertex_size(vertex_format, flags, version)
        data  = rw.rw_bytestring(None, vsize*vertex_count)
        vertices = [VertexBinary() for _ in range(vertex_count)]
        offset = 0
        if version < 0x02000000:
            pass
        else:
            # Positions
            if vertex_format.has_positions:
                st = offset
                ed = offset + 12
                for v in vertices:
                    v.buffer[VertexAttributes.POSITION] = unpack_vec3(data[st:ed])
                    st += vsize
                    ed += vsize
                offset += 12
            
            # Texcoord 0
            if vertex_format.has_texcoord0:
                st = offset
                ed = offset + 4
                for v in vertices:
                    d = unpack_uv_v2(data[st:ed])
                    v[VertexAttributes.TEXCOORD0] = [d[0], 1-d[1]]
                    st += vsize
                    ed += vsize
                offset += 4
            
            # Normals
            if vertex_format.has_normals:
                st = offset
                ed = offset + 12
                for v in vertices:
                    v[VertexAttributes.NORMAL] = unpack_vec3(data[st:ed])
                    st += vsize
                    ed += vsize
                offset += 12
                
            # Tangents
            if vertex_format.has_tangents:
                st = offset
                ed = offset + 12
                for v in vertices:
                    v.tangent = unpack_vec3(data[st:ed])
                    st += vsize
                    ed += vsize
                offset += 12
                
            # Binormals
            if vertex_format.has_binormals:
                st = offset 
                ed = offset + 12
                for v in vertices:
                    v.binormal = unpack_vec3(data[st:ed])
                    st += vsize
                    ed += vsize
                offset += 12
                
            # Texcoord 1
            if vertex_format.has_texcoord1:
                st = offset
                ed = offset + 4
                for v in vertices:
                    d = unpack_uv_v2(data[st:ed])
                    v[VertexAttributes.TEXCOORD1] = [d[0], 1-d[1]]
                    st += vsize
                    ed += vsize
                offset += 4
                
            # Texcoord 2
            if vertex_format.has_texcoord2:
                st = offset
                ed = offset + 4
                for v in vertices:
                    d = unpack_uv_v2(data[st:ed])
                    v[VertexAttributes.TEXCOORD2] = [d[0], 1-d[1]]
                    st += vsize
                    ed += vsize
                offset += 4
            
            # Color 0
            if vertex_format.has_color0:
                st = offset
                ed = offset + 4
                for v in vertices:
                    v.color0 = unpack_color(data[st:ed])
                    st += vsize
                    ed += vsize
                offset += 4
            
            # Color 1
            if vertex_format.has_color1:
                st = offset
                ed = offset + 4
                for v in vertices:
                    v.color1 = unpack_color(data[st:ed])
                    st += vsize
                    ed += vsize
                offset += 4
        
            # Weights
            if flags.has_weights:
                p1 = offset
                p2 = offset + 16
                p3 = offset + 32
                for v in vertices:
                    v[VertexAttributes.WEIGHTS] = [e/65535 for e in unpack_wgt(data[p1:p2])]
                    v[VertexAttributes.INDICES] = unpack_wgt(data[p2:p3])
                    p1 += vsize
                    p2 += vsize
                    p3 += vsize
                offset += 32
        return vertices
    
    def serialize(rw, value, vertex_count, vertex_format, flags, version):
        if rw.endianness == ">":
            pack_vec3  = pack_vec3_be
            pack_uv_v1 = pack_uv_v1_be
            pack_uv_v2 = pack_uv_v2_be
            pack_color = pack_color_be
            pack_wgt   = pack_wgt_be
        elif rw.endianness == "<":
            pack_vec3  = pack_vec3_le
            pack_uv_v1 = pack_uv_v1_le
            pack_uv_v2 = pack_uv_v2_le
            pack_color = pack_color_le
            pack_wgt   = pack_wgt_le
        else:
            raise ValueError(f"Unknown endianness: {rw.endianness}")
        
        vertices = value
        vsize = calc_vertex_size(vertex_format, flags, version)
        arr = bytearray(vsize*vertex_count)
        
        offset = 0
        if version < 0x02000000:
            pass
        else:
            # Positions
            if vertex_format.has_positions:
                st = offset
                ed = offset + 12
                for v in vertices:
                    arr[st:ed] = pack_vec3(*v.position)
                    st += vsize
                    ed += vsize
                offset += 12
            
            # Texcoord 0
            if vertex_format.has_texcoord0:
                st = offset
                ed = offset + 4
                for v in vertices:
                    d = v[VertexAttributes.TEXCOORD0]
                    arr[st:ed] = pack_uv_v2(d[0], 1.-d[0])
                    st += vsize
                    ed += vsize
                offset += 4
            
            # Normals
            if vertex_format.has_normals:
                st = offset
                ed = offset + 12
                for v in vertices:
                    arr[st:ed] = pack_vec3(*v.normal)
                    st += vsize
                    ed += vsize
                offset += 12
                
            # Tangents
            if vertex_format.has_tangents:
                st = offset
                ed = offset + 12
                for v in vertices:
                    arr[st:ed] = pack_vec3(*v.tangent)
                    st += vsize
                    ed += vsize
                offset += 12
                
            # Binormals
            if vertex_format.has_binormals:
                st = offset
                ed = offset + 12
                for v in vertices:
                    arr[st:ed] = pack_vec3(*v.binormal)
                    st += vsize
                    ed += vsize
                offset += 12
                
            # Texcoord 1
            if vertex_format.has_texcoord1:
                st = offset
                ed = offset + 4
                for v in vertices:
                    d = v[VertexAttributes.TEXCOORD1]
                    arr[st:ed] = pack_uv_v2(d[0], 1.-d[0])
                    st += vsize
                    ed += vsize
                offset += 4
                
            # Texcoord 2
            if vertex_format.has_texcoord2:
                st = offset 
                ed = offset + 4
                for v in vertices:
                    d = v[VertexAttributes.TEXCOORD2]
                    arr[st:ed] = pack_uv_v2(d[0], 1.-d[0])
                    st += vsize
                    ed += vsize
                offset += 4
            
            # Color 0
            if vertex_format.has_color0:
                st = offset
                ed = offset + 4
                for v in vertices:
                    arr[st:ed] = pack_color(*v.color0)
                    st += vsize
                    ed += vsize
                offset += 4
            
            # Color 1
            if vertex_format.has_color1:
                st = offset
                ed = offset + 4
                for v in vertices:
                    arr[st:ed] = pack_color(*v.color1)
                    st += vsize
                    ed += vsize
                offset += 4
        
            # Weights
            if flags.has_weights:
                p1 = offset 
                p2 = offset + 16
                p3 = offset + 32
                for v in vertices:
                    arr[p1:p2] = pack_wgt(*[max(min(0xFFFF, int(round(e*0xFFFF,0))), 0) for e in v[VertexAttributes.WEIGHTS]])
                    arr[p2:p3] = pack_wgt(*v[VertexAttributes.INDICES])
                    p1 += vsize
                    p2 += vsize
                    p3 += vsize
                offset += 32
        
        return value
    
    def count(rw, value, vertex_count, vertex_format, flags, version):
        vsize = calc_vertex_size(vertex_format, flags, version)
        rw.advance_offset(vsize*vertex_count)
        return value
