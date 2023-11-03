from ......serialization.Serializable import Serializable
from ......serialization.utils import safe_format, hex32_format
from ....Utils.Matrices import transforms_to_matrix, multiply_transform_matrices, transform_vector
from ...CommonStructures import BitVector, SceneNodeBinary
from .SkinningDataBinary import SkinningDataBinary


class ModelFlags(BitVector):
    has_bounding_box    = BitVector.DEF_FLAG(0x00)
    has_bounding_sphere = BitVector.DEF_FLAG(0x01)
    has_skin_data       = BitVector.DEF_FLAG(0x02)
    flag_3              = BitVector.DEF_FLAG(0x03)
    flag_4              = BitVector.DEF_FLAG(0x04)
    flag_5              = BitVector.DEF_FLAG(0x05)
    flag_6              = BitVector.DEF_FLAG(0x06)
    flag_7              = BitVector.DEF_FLAG(0x07)
    flag_8              = BitVector.DEF_FLAG(0x08)
    flag_9              = BitVector.DEF_FLAG(0x09)
    flag_10             = BitVector.DEF_FLAG(0x0A)
    flag_11             = BitVector.DEF_FLAG(0x0B)
    flag_12             = BitVector.DEF_FLAG(0x0C)
    flag_13             = BitVector.DEF_FLAG(0x0D)
    flag_14             = BitVector.DEF_FLAG(0x0E)
    flag_15             = BitVector.DEF_FLAG(0x0F)
    flag_16             = BitVector.DEF_FLAG(0x10)
    flag_17             = BitVector.DEF_FLAG(0x11)
    flag_18             = BitVector.DEF_FLAG(0x12)
    flag_19             = BitVector.DEF_FLAG(0x12)
    flag_20             = BitVector.DEF_FLAG(0x14)
    flag_21             = BitVector.DEF_FLAG(0x15)
    flag_22             = BitVector.DEF_FLAG(0x16)
    flag_23             = BitVector.DEF_FLAG(0x17)
    flag_24             = BitVector.DEF_FLAG(0x18)
    flag_25             = BitVector.DEF_FLAG(0x19)
    flag_26             = BitVector.DEF_FLAG(0x1A)
    flag_27             = BitVector.DEF_FLAG(0x1B)
    flag_28             = BitVector.DEF_FLAG(0x1C)
    flag_29             = BitVector.DEF_FLAG(0x1D)
    flag_30             = BitVector.DEF_FLAG(0x1E)
    flag_31             = BitVector.DEF_FLAG(0x1F)


class ModelPayload(Serializable):
    TYPECODE = 0x00010003
         
    APPROVED_VERSIONS = set([
        #0x01104920,
        #0x01105000,
        #0x01105010,
        #0x01105020,
        #0x01105030,
        #0x01105040,
        #0x01105060,
        #0x01105070,
        #0x01105080,
        #0x01105090,
        0x01105100
    ])
    
    def __init__(self, endianness='>'):
        super().__init__()
        self.context.endianness = endianness
        
        self.flags           = ModelFlags(endianness)
        self.skinning_data   = SkinningDataBinary(endianness)
        self.bounding_box_max_dims  = None
        self.bounding_box_min_dims  = None
        self.bounding_sphere_centre = None
        self.bounding_sphere_radius = None
        self.root_node = SceneNodeBinary()
        
    def __repr__(self):
        return f"[GFD::SceneContainer] {safe_format(self.flags._value, hex32_format)}"

    def read_write(self, rw, version):
        self.flags = rw.rw_obj(self.flags)
        
        if self.flags.has_skin_data:
            rw.rw_obj(self.skinning_data)
        if self.flags.has_bounding_box:
            self.bounding_box_max_dims = rw.rw_float32s(self.bounding_box_max_dims, 3)
            self.bounding_box_min_dims = rw.rw_float32s(self.bounding_box_min_dims, 3)
        if self.flags.has_bounding_sphere:
            self.bounding_sphere_centre = rw.rw_float32s(self.bounding_sphere_centre, 3)
            self.bounding_sphere_radius = rw.rw_float32(self.bounding_sphere_radius)
            
        rw.rw_obj(self.root_node, version)
    
    def get_mesh_bounding_boxes(self):
        flat_nodes = self.root_node.flattened()
        nodes        = flat_nodes.nodes
        node_parents = flat_nodes.node_parents
        
        matrices = [None for _ in range(len(nodes))]
        for i, bone in enumerate(nodes):
            matrix = transforms_to_matrix(bone.position, bone.rotation, bone.scale)
            parent_idx = node_parents[i]
            if parent_idx > -1:
                matrices[i] = multiply_transform_matrices(matrices[parent_idx], matrix)
            else:
                matrices[i] = matrix
        
        mesh_verts = []
        for node_idx, mesh in self.root_node.get_meshes():
            if not mesh.flags.has_bounding_box:
                continue
            matrix   = matrices[node_idx]
            min_dims = mesh.bounding_box_min_dims
            max_dims = mesh.bounding_box_max_dims
            
            mesh_verts.append(transform_vector(matrix, min_dims))
            mesh_verts.append(transform_vector(matrix, max_dims))
        return mesh_verts, matrices

    def calc_bounding_box(self):
        mesh_verts, matrices = self.get_mesh_bounding_boxes()
        if not len(mesh_verts):
            return ([0, 0, 0], [0, 0, 0])
        verts = []
        for m in matrices:
            verts.append([m[0*4+3], m[1*4+3], m[2*4+3]])
            
        max_dims = [max(vs) for vs in zip(*[*mesh_verts, *verts])]
        min_dims = [min(vs) for vs in zip(*[*mesh_verts, *verts])]
        
        return (min_dims, max_dims)
    
    def autocalc_bounding_box(self):
        self.bounding_box_min_dims, self.bounding_box_max_dims = self.calc_bounding_box()
        self.flags.has_bounding_box = True
    
    def calc_bounding_sphere(self):
        mesh_verts, matrices = self.get_mesh_bounding_boxes()
        min_dims, max_dims = self.calc_bounding_box()
        center = [sum(vs)/len(vs) for vs in zip(*mesh_verts)]
        if max_dims is not None and min_dims is not None:
            max_dim_radius = sum([(v1 - v2)**2 for v1, v2 in zip(max_dims, center)])**.5
            min_dim_radius = sum([(v1 - v2)**2 for v1, v2 in zip(min_dims, center)])**.5
        else:
            max_dim_radius = max_dims
            min_dim_radius = min_dims
        
        radius = max([max_dim_radius, min_dim_radius])
        
        return (center, radius)
    
    def autocalc_bounding_sphere(self):
        self.bounding_sphere_centre, self.bounding_sphere_radius = self.calc_bounding_sphere()
        self.flags.has_bounding_sphere = True