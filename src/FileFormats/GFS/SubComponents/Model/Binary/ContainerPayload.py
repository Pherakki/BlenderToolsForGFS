from ......serialization.formatters import HEX32_formatter
from ....Utils.Matrices import transforms_to_matrix, multiply_transform_matrices, transform_vector
from ...CommonStructures import BitVector0x20
from ...CommonStructures import SceneNodeBinary
from .SkinningDataBinary import SkinningDataBinary


class ModelFlags(BitVector0x20):
    has_bounding_box    = BitVector0x20.DEF_FLAG(0x00)
    has_bounding_sphere = BitVector0x20.DEF_FLAG(0x01)
    has_skin_data       = BitVector0x20.DEF_FLAG(0x02)


class ModelPayload:
    TYPECODE = 0x00010003

    
    def __init__(self):
        self.flags           = ModelFlags()
        self.skinning_data   = SkinningDataBinary()
        self.max_weights            = 8
        self.bounding_box_max_dims  = None
        self.bounding_box_min_dims  = None
        self.bounding_sphere_centre = None
        self.bounding_sphere_radius = None
        self.root_node = SceneNodeBinary()
        
    def __repr__(self):
        return f"[GFD::ModelPayload] {HEX32_formatter(self.flags._value)}"

    def exbip_rw(self, rw, version):
        self.flags = rw.rw_obj(self.flags)
        
        if self.flags.has_skin_data:
            rw.rw_obj(self.skinning_data)
            if version > 0x02040000:
                self.max_weights = rw.rw_int8(self.max_weights)
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
