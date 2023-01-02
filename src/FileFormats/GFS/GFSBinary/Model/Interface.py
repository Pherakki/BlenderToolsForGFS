import copy

from ...Utils.Matrices import transforms_to_matrix, multiply_transform_matrices, are_matrices_close, invert_transform_matrix, ibpm_to_transform_matrix, bake_scale_into_position
from ..CommonStructures import ObjectName
from ..CommonStructures.SceneNodeBinary import SceneNodeBinary
from ..CommonStructures.SceneNodeBinary.MeshBinary import MeshBinary
from ..CommonStructures.SceneNodeBinary.NodeAttachmentBinary import NodeAttachmentBinary
from .Binary import ModelPayload



class NodeInterface:
    def __init__(self):
        self.parent_idx       = None
        self.name             = None
        self.position         = None
        self.rotation         = None
        self.scale            = None
        self.bind_pose_matrix = None
        self.unknown_float    = None
        self.properties       = [] # Property interfaces?
    
    @classmethod
    def binary_node_tree_to_list(cls, binary):
        node_list        = []
        mesh_list        = []
        camera_list      = []
        light_list       = []
        cls._fetch_node_from_tree(binary, -1, node_list, mesh_list, camera_list, light_list)
        
        return node_list, mesh_list, camera_list, light_list
        
    @classmethod
    def _fetch_node_from_tree(cls, node, parent, node_list, mesh_list, camera_list, light_list):
        node_idx = len(node_list)
        node_list.append(cls.from_binary(node, parent))
        for attachment in node.attachments:
            if attachment.type == 4:
                mesh_list.append(MeshInterface.from_binary(node_idx, attachment.data))
            elif attachment.type == 5:
                camera_list.append(CameraInterface.from_binary(node_idx, attachment.data))
            elif attachment.type == 6:
                light_list.append(LightInterface.from_binary(node_idx, attachment.data))
            else:
                raise NotImplementedError("No Interface exists for attachment type '{attachment.type}'")
        for child in node.children[::-1]:
            cls._fetch_node_from_tree(child, node_idx, node_list, mesh_list, camera_list, light_list)
    
    @classmethod
    def list_to_binary_node_tree(cls, node_list, mesh_list, camera_list, light_list):
        node_children = {}
        # First not in list required to be root
        # Should probably throw in a check here to make sure...
        for i, node in enumerate(node_list[1:]):
            n_id = node.parent
            if n_id not in node_children:
                node_children[n_id] = []
            node_children[n_id].append(i+1)
        id_map = {0: 0}
        node_collection = [node.to_binary() for node in node_list]
        
        # Need to clear the node children for now, until every node is actually
        # built from scratch
        for node in node_collection:
            node.children.clear()
            node.attachments.clear()
        cls._push_node_into_tree(0, node_children, node_collection, id_map)
        
        def add_attachments(typename, typevalue, element_list):
            binaries = []
            for i, elem in enumerate(element_list):
                if elem.node < 0:
                    raise ValueError(f"{typename} {i} has an invalid node parent: {elem.node} must be >= 0")
                node = node_collection[elem.node]
                attachment = NodeAttachmentBinary()
                attachment.type = typevalue
                attachment.data = elem.to_binary()
                node.attachments.append(attachment)
                node.attachment_count += 1
                binaries.append((attachment.data, elem.node))
            return binaries
                
        mesh_binaries = add_attachments("Mesh",   4, mesh_list)
        add_attachments("Camera", 5, camera_list)
        add_attachments("Light",  6, light_list)
        
        return node_collection[0], id_map, mesh_binaries
    
    @classmethod
    def _push_node_into_tree(cls, node_idx, node_children, node_collection, id_map):
        child_node_idxs = node_children.get(node_idx, [])
        for cn_id in child_node_idxs:
            id_map[cn_id] = len(id_map)
            node_collection[node_idx].children.insert(0, node_collection[cn_id])
            cls._push_node_into_tree(cn_id, node_children, node_collection, id_map)

    @classmethod
    def from_binary(cls, binary, parent_idx, bind_pose_matrix=None):
        instance = cls()
        
        instance.parent = parent_idx
        instance.name = binary.name.string
        instance.position = binary.position
        instance.rotation = binary.rotation
        instance.scale = binary.scale
        instance.bind_pose_matrix = bind_pose_matrix
        instance.unknown_float = binary.float
        instance.properties = binary.properties.data # Interface?!?
        
        return instance
    
    def to_binary(self):
        binary = SceneNodeBinary()
        
        binary.name = ObjectName.from_name(self.name)
        binary.position = self.position
        binary.rotation = self.rotation
        binary.scale = self.scale
        binary.float = self.unknown_float
        binary.has_properties = len(self.properties) > 0
        binary.properties.data = self.properties  # Interface?!?
        binary.properties.count = len(self.properties)
        
        return binary
    
class MeshInterface:
    def __init__(self):
        self.node    = None
        
        self.flag_5  = None
        self.flag_7  = None
        self.flag_8  = None
        self.flag_9  = None
        self.flag_10 = None
        self.flag_11 = None
        self.flag_13 = None
        self.flag_14 = None
        self.flag_15 = None
        self.flag_16 = None
        self.flag_17 = None
        self.flag_18 = None
        self.flag_19 = None
        self.flag_20 = None
        self.flag_21 = None
        self.flag_22 = None
        self.flag_23 = None
        self.flag_24 = None
        self.flag_25 = None
        self.flag_26 = None
        self.flag_27 = None
        self.flag_28 = None
        self.flag_29 = None
        self.flag_30 = None
        self.flag_31 = None
    
        self.vertices = None
        self.material_name = None
        self.indices = None
        self.morphs = None
        self.unknown_0x12 = None
        self.unknown_float_1 = None
        self.unknown_float_2 = None
        
        # THINGS THAT COULD BE REMOVABLE
        self.index_type = None
        self.keep_bounding_box = None
        self.keep_bounding_sphere = None
        
    
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        
        # Deal with unpacking later...
        instance.node = node_idx
        
        # Can get rid of some of these in a minute
        # 0x00000001 says if weights are used
        # 0x00000002 says if a material is used
        # 0x00000004 says if indices are present
        instance.keep_bounding_box    = binary.flags.has_bounding_box
        instance.keep_bounding_sphere = binary.flags.has_bounding_sphere
        instance.flag_5               = binary.flags.flag_5
        # 0x00000040 says if any morphs are present
        instance.flag_7               = binary.flags.flag_7
        instance.flag_8               = binary.flags.flag_8
        instance.flag_9               = binary.flags.flag_9
        instance.flag_10              = binary.flags.flag_10
        instance.flag_11              = binary.flags.flag_11
        # 0x00001000 says if unknown floats are present
        instance.flag_13              = binary.flags.flag_13
        instance.flag_14              = binary.flags.flag_14
        instance.flag_15              = binary.flags.flag_15
        instance.flag_16              = binary.flags.flag_16
        instance.flag_17              = binary.flags.flag_17
        instance.flag_18              = binary.flags.flag_18
        instance.flag_19              = binary.flags.flag_19
        instance.flag_20              = binary.flags.flag_20
        instance.flag_21              = binary.flags.flag_21
        instance.flag_22              = binary.flags.flag_22
        instance.flag_23              = binary.flags.flag_23
        instance.flag_24              = binary.flags.flag_24
        instance.flag_25              = binary.flags.flag_25
        instance.flag_26              = binary.flags.flag_26
        instance.flag_27              = binary.flags.flag_27
        instance.flag_28              = binary.flags.flag_28
        instance.flag_29              = binary.flags.flag_29
        instance.flag_30              = binary.flags.flag_30
        instance.flag_31              = binary.flags.flag_31
        
        instance.vertices        = binary.vertices
        instance.material_name   = binary.material_name.string
        instance.indices         = binary.indices
        instance.index_type      = binary.index_type # Can probably remove this...
        instance.morphs          = binary.morph_data # NEEDS UNPACKING
        instance.unknown_0x12    = binary.unknown_0x12
        instance.unknown_float_1 = binary.unknown_float_1
        instance.unknown_float_2 = binary.unknown_float_2
        
        return instance
        
    def to_binary(self):
        binary = MeshBinary()
        
        if len(self.vertices):
            # Assume that if something is true for the first vertex
            # Empty - 0x00000001 # << 0
            binary.vertex_format.has_positions  = (self.vertices[0].position  is not None) # 0x00000002
            # Empty - 0x00000004 # << 2
            # Empty - 0x00000008 # << 3
            binary.vertex_format.has_normals    = (self.vertices[0].normal    is not None) # 0x00000010
            # Empty - 0x00000020 # << 5
            binary.vertex_format.has_color1     = (self.vertices[0].color1    is not None) # 0x00000040
            # Empty - 0x00000080 # << 7
            binary.vertex_format.has_texcoord_0 = (self.vertices[0].texcoord0 is not None) # 0x00000100
            binary.vertex_format.has_texcoord_1 = (self.vertices[0].texcoord1 is not None) # 0x00000200
            binary.vertex_format.has_texcoord_2 = (self.vertices[0].texcoord2 is not None) # 0x00000400
            binary.vertex_format.has_texcoord_3 = (self.vertices[0].texcoord3 is not None) # 0x00000800
            binary.vertex_format.has_texcoord_4 = (self.vertices[0].texcoord4 is not None) # 0x00001000
            binary.vertex_format.has_texcoord_5 = (self.vertices[0].texcoord5 is not None) # 0x00002000
            binary.vertex_format.has_texcoord_6 = (self.vertices[0].texcoord6 is not None) # 0x00004000
            binary.vertex_format.has_texcoord_7 = (self.vertices[0].texcoord7 is not None) # 0x00008000
            # Empty - 0x00010000 # << 16
            # Empty - 0x00020000 # << 17
            # Empty - 0x00040000 # << 18
            # Empty - 0x00080000 # << 19
            # Empty - 0x00100000 # << 20
            # Empty - 0x00200000 # << 21
            # Empty - 0x00400000 # << 22
            # Empty - 0x00800000 # << 23
            # Empty - 0x01000000 # << 24
            # Empty - 0x02000000 # << 25
            # Empty - 0x04000000 # << 26
            # Empty - 0x08000000 # << 27
            binary.vertex_format.has_tangents    = (self.vertices[0].tangent  is not None) # 0x10000000
            binary.vertex_format.has_binormals   = (self.vertices[0].binormal is not None) # 0x20000000
            binary.vertex_format.has_color2      = (self.vertices[0].color2   is not None) # 0x40000000
            # Empty - 0x80000000 # << 31
            
            binary.flags.has_weights = (self.vertices[0].indices is not None)
        
        binary.flags.has_material        = (self.material_name is not None)
        binary.flags.has_indices         = (len(self.indices) > 0)
        binary.flags.has_bounding_box    = self.keep_bounding_box
        binary.flags.has_bounding_sphere = self.keep_bounding_sphere
        binary.flags.flag_5              = self.flag_5
        binary.flags.has_morphs          = (self.morphs.count is not None)
        binary.flags.flag_7              = self.flag_7
        binary.flags.flag_8              = self.flag_8
        binary.flags.flag_9              = self.flag_9
        binary.flags.flag_10             = self.flag_10
        binary.flags.flag_11             = self.flag_11
        if self.unknown_float_1 is None and self.unknown_float_2 is None:
            pass
        else:
            binary.flags.has_unknown_floats = True
            binary.unknown_float_1 = self.unknown_float_1
            binary.unknown_float_2 = self.unknown_float_2
            if self.unknown_float_1 is None:
                binary.unknown_float_1 = 0.
            if self.unknown_float_2 is None:
                binary.unknown_float_2 = 0.
        binary.flags.flag_13 = self.flag_13
        binary.flags.flag_14 = self.flag_14
        binary.flags.flag_15 = self.flag_15
        binary.flags.flag_16 = self.flag_16
        binary.flags.flag_17 = self.flag_17
        binary.flags.flag_18 = self.flag_18
        binary.flags.flag_19 = self.flag_19
        binary.flags.flag_20 = self.flag_20
        binary.flags.flag_21 = self.flag_21
        binary.flags.flag_22 = self.flag_22
        binary.flags.flag_23 = self.flag_23
        binary.flags.flag_24 = self.flag_24
        binary.flags.flag_25 = self.flag_25
        binary.flags.flag_26 = self.flag_26
        binary.flags.flag_27 = self.flag_27
        binary.flags.flag_28 = self.flag_28
        binary.flags.flag_29 = self.flag_29
        binary.flags.flag_30 = self.flag_30
        binary.flags.flag_31 = self.flag_31
        
        if len(self.indices) % 3:
            raise ValueError("Mesh contains {len(self.indices)} indices; must be a multiple of 3")
        binary.tri_count     = len(self.indices) // 3
        binary.index_type    = self.index_type
        binary.vertex_count  = len(self.vertices)
        binary.unknown_0x12  = self.unknown_0x12
        binary.vertices      = self.vertices
        binary.morph_data.flags = self.morphs.flags        # NEEDS UNPACKING
        binary.morph_data.count = len(self.morphs.targets) # NEEDS UNPACKING
        binary.morph_data.targets = self.morphs.targets    # NEEDS UNPACKING
        binary.indices       = self.indices
        binary.material_name = ObjectName.from_name(self.material_name)
        
        ####################
        # BOUNDING VOLUMES #
        ####################
        if self.keep_bounding_sphere:
            if binary.vertex_format.has_positions:
                # This is WRONG but I can't get an iterative Welzl algorithm
                # working
                max_dims = [*self.vertices[0].position]
                min_dims = [*self.vertices[0].position]
                        
                for v in self.vertices:
                    pos = v.position
                    for i in range(3):
                        max_dims[i] = max(max_dims[i], pos[i])
                        min_dims[i] = min(min_dims[i], pos[i])
                
                if self.keep_bounding_box:
                    binary.bounding_box_max_dims = max_dims
                    binary.bounding_box_min_dims = min_dims
                centre = [.5*(mx + mn) for mx, mn in zip(max_dims, min_dims)]
                radius = 0.
                for v in self.vertices:
                    pos = v.position
                    dist = (p-c for p, c in zip(pos, centre))
                    radius = max(sum(d*d for d in dist), radius)
                binary.bounding_sphere_centre = centre
                binary.bounding_sphere_radius = radius
            else:
                raise ValueError("Mesh is marked for bounding sphere export, but has no vertex position data")
                
        return binary
    
class CameraInterface:
    def __init__(self):
        self.node   = None
        self.binary = None
        
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        # Deal with unpacking later...
        instance.node = node_idx
        instance.binary = binary
        
        return instance
        
    def to_binary(self):
        return self.binary
    
class LightInterface:
    def __init__(self):
        self.node   = None
        self.binary = None
        
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        
        # Deal with unpacking later...
        instance.node = node_idx
        instance.binary = binary
        
        return instance
        
    def to_binary(self):
        return self.binary

class ModelInterface:
    @classmethod
    def from_binary(cls, binary, copy_verts=True):
        #instance.skinning_data = binary.skinning_data
        keep_bounding_box = binary.flags.has_bounding_box
        keep_bounding_sphere = binary.flags.has_bounding_sphere
        
        bones,   \
        meshes,  \
        cameras, \
        lights = NodeInterface.binary_node_tree_to_list(binary.root_node)
        
        nodes_with_ibpms = {}
        if binary.flags.has_skin_data is not None:
            for mesh in meshes:
                if copy_verts:
                    mesh.vertices = copy.deepcopy(mesh.vertices)
                if mesh.vertices[0].indices is not None:
                    # Remap indices from local indices to global indices
                    palette_indices = set()
                    for v in mesh.vertices:
                        for idx, wgt in zip(v.indices[::-1], v.weights):
                            if wgt > 0:
                                palette_indices.add(idx)
                        v.indices = [binary.skinning_data.matrix_palette[idx] for idx in v.indices[::-1]]
                    
                    # Link IBPMs to the nodes they are relative to
                    palette_indices = sorted(palette_indices)
                    node_idx = mesh.node
                    for palette_idx in palette_indices:
                        weighted_node_idx = binary.skinning_data.matrix_palette[palette_idx]
                        weighted_ibpm     = binary.skinning_data.ibpms[palette_idx]
                        bpm               = invert_transform_matrix(ibpm_to_transform_matrix(weighted_ibpm))
                        
                        if weighted_node_idx not in nodes_with_ibpms:
                            nodes_with_ibpms[weighted_node_idx] = []
                        nodes_with_ibpms[weighted_node_idx].append((node_idx, bpm))
        
        # Now construct bind poses for bones
        world_pose_matrices = [None]*len(bones)
        world_pose_matrices[0] = transforms_to_matrix(bones[0].position, bones[0].rotation, bones[0].scale)
        for i, bone in enumerate(bones[1:]):
            i = i+1
            local_bpm = transforms_to_matrix(bone.position, bone.rotation, bone.scale)
            world_pose_matrices[i] = multiply_transform_matrices(world_pose_matrices[bone.parent], local_bpm)
            
        for i, bone in enumerate(bones):
            if i in nodes_with_ibpms:
                # Average together all bpms for the node
                # Hopefully they're all similar
                contributing_matrices = []
                for node_idx, bpm in nodes_with_ibpms[i]:
                    world_matrix = multiply_transform_matrices(world_pose_matrices[node_idx], bpm)
                    contributing_matrices.append(bake_scale_into_position(world_matrix))
                n = len(contributing_matrices)
                bone.bind_pose_matrix = [sum([m[comp_idx] for m in contributing_matrices])/n for comp_idx in range(12)]
            else:
                bone.bind_pose_matrix = bake_scale_into_position(world_pose_matrices[i])

                    
        return bones, meshes, cameras, lights, keep_bounding_box, keep_bounding_sphere
        
    @staticmethod
    def to_binary(bones, meshes, cameras, lights, keep_bounding_box, keep_bounding_sphere, copy_verts=True):
        binary = ModelPayload()

        binary.flags.has_bounding_box    = keep_bounding_box
        binary.flags.has_bounding_sphere = keep_bounding_sphere
        
        # Need to return mesh binary list here too!
        binary.root_node, old_node_id_to_new_node_id_map, mesh_binaries = NodeInterface.list_to_binary_node_tree(bones, meshes, cameras, lights)

        ####################
        # BOUNDING VOLUMES #
        ####################
        if keep_bounding_box or keep_bounding_sphere:
            verts = []
            for mesh_binary, mesh_node_id in mesh_binaries:
                if mesh_binary.flags & 0x00000008 != 0:  # Check if you need to do the others here too
                    mx = mesh_binary.bounding_box_max_dims
                    mn = mesh_binary.bounding_box_min_dims
                    verts.extend([
                        [mx[0], mx[1], mx[2]],
                        [mx[0], mx[1], mn[2]],
                        [mx[0], mn[1], mx[2]],
                        [mx[0], mn[1], mn[2]],
                        [mn[0], mn[1], mn[2]],
                        [mn[0], mn[1], mx[2]],
                        [mn[0], mx[1], mn[2]],
                        [mn[0], mx[1], mx[2]]
                    ])
                
            if not len(verts):
                if keep_bounding_box:
                    raise ValueError("Model is marked for bounding box export, but has no meshes with vertex position data")
                elif keep_bounding_sphere:
                    raise ValueError("Model is marked for bounding sphere export, but has no meshes with vertex position data")
            
            
            max_dims = [*verts[0]]
            min_dims = [*verts[0]]
                    
            for pos in verts:
                for i in range(3):
                    max_dims[i] = max(max_dims[i], pos[i])
                    min_dims[i] = min(min_dims[i], pos[i])
            
            # Do box
            if keep_bounding_box:
                binary.bounding_box_max_dims = max_dims
                binary.bounding_box_min_dims = min_dims
                
            # Do sphere
            # This is WRONG but I can't get an iterative Welzl algorithm working
            if keep_bounding_sphere:
                centre = [.5*(mx + mn) for mx, mn in zip(max_dims, min_dims)]
                radius = 0.
                for mesh_binary, mesh_node_id in mesh_binaries:
                    if mesh_binary.vertex_format & 0x00000002 == 0:
                        continue
                    for v in mesh_binary.vertices:
                        pos = v.position
                        dist = (p-c for p, c in zip(pos, centre))
                        radius = max(sum(d*d for d in dist), radius)
                binary.bounding_sphere_centre = centre
                binary.bounding_sphere_radius = radius
            
        #########################
        # CREATE MATRIX PALETTE #
        #########################
        binary.flags.has_skin_data = False
        for mesh_binary, mesh_node_id in mesh_binaries:
            if mesh_binary.flags & 0x00000001:
                binary.flags.has_skin_data = True
                break
            
        if binary.flags.has_skin_data:
            # GENERATE SKINNING DATA STRUCTURE
            world_matrices = [None]*len(bones)
            for i, bone in enumerate(bones):
                local_matrix = transforms_to_matrix(bone.position, bone.rotation, bone.scale)
                if bone.parent > -1:
                    world_matrices[i] = multiply_transform_matrices(world_matrices[bone.parent], local_matrix)
                else:
                    world_matrices[i] = local_matrix
            
            ibpms = []
            matrix_palette = []
            matrix_cache = {}
            index_lookup = {}
            for mesh_binary, mesh_node_id in mesh_binaries:
                node_matrix = world_matrices[mesh_node_id]
                if mesh_binary.flags & 0x00000001:
                    indices = set()
                    for vertex in mesh_binary.vertices:
                        for idx, wgt in zip(vertex.indices[::-1], vertex.weights):
                            if wgt > 0:
                                indices.add(idx)
                                
                    for idx in sorted(indices):
                        inv_index_matrix = invert_transform_matrix(world_matrices[idx])
                        ibpm = multiply_transform_matrices(inv_index_matrix, node_matrix)
                        if idx not in matrix_cache:
                            matrix_cache[idx] = {}
                            
                        matching_matrix_found = False
                        for palette_idx, palette_ibpm in matrix_cache[idx].items():
                            if are_matrices_close(ibpm, palette_ibpm, atol=0.01, rtol=0.05):
                                index_lookup[(mesh_node_id, idx)] = palette_idx
                                matching_matrix_found = True
                                break
                            
                        if not matching_matrix_found:
                            palette_idx = len(matrix_palette)
                            matrix_cache[idx][palette_idx] = ibpm
                            matrix_palette.append(idx)
                            ibpms.append(ibpm)
                            index_lookup[(mesh_node_id, idx)] = palette_idx
            
            binary.skinning_data.matrix_palette = matrix_palette
            binary.skinning_data.ibpms = ibpms
            binary.skinning_data.bone_count = len(matrix_palette)
            
            # REMAP VERTEX INDICES
            for mesh, mesh_node_id in mesh_binaries:
                if copy_verts:
                    mesh.vertices = copy.deepcopy(mesh.vertices)
                if mesh.vertices[0].indices is not None:
                    for v in mesh.vertices:
                        # Need to factor in remapped nodes
                        #v.indices = [idx for idx in v.indices[::-1]]
                        indices = [index_lookup.get((mesh_node_id, idx), 0) for idx in v.indices]
                        for wgt_idx, wgt in enumerate(v.weights):
                            if wgt == 0:
                                indices[wgt_idx] = 0
                        v.indices = indices[::-1]
        return binary
        