import copy

from ...Utils.Matrices import multiply_transform_matrices, normalise_transform_matrix_scale
from ...Utils.Matrices import transforms_to_matrix, transposed_mat4x4_to_mat4x3, mat4x3_to_transposed_mat4x4
from ...Utils.Matrices import are_transform_matrices_close, invert_transform_matrix

from ..CommonStructures.SceneNode import NodeInterface
from .Binary import ModelPayload


def build_rest_pose(bone, bones):
    local_pose = transforms_to_matrix(bone.position, bone.rotation, bone.scale)
    parent_idx = bone.parent_idx
    
    if parent_idx >= 0:
        parent_pose = build_rest_pose(bones[parent_idx], bones)
        return multiply_transform_matrices(parent_pose, local_pose)
    else:
        return local_pose


class ModelInterface:
    @classmethod
    def from_binary(cls, binary, copy_verts=True, warnings=None):
        #instance.skinning_data = binary.skinning_data
        bb_max = None
        bb_min = None
        if binary.flags.has_bounding_box:
            bb_max = binary.bounding_box_max_dims
            bb_min = binary.bounding_box_min_dims
        bs_centre = None
        bs_radius = None
        if binary.flags.has_bounding_sphere:
            bs_centre = binary.bounding_sphere_centre
            bs_radius = binary.bounding_sphere_radius
        flag_3 = binary.flags.flag_3
        
        bones,   \
        meshes,  \
        cameras, \
        lights,  \
        epls     = NodeInterface.binary_node_tree_to_list(binary.root_node)

        # Find which nodes have BPMs, and which meshes give them context
        nodes_with_ibpms = {}
        has_bad_vidxs = False
        if binary.flags.has_skin_data is not None:
            for mesh in meshes:
                if copy_verts:
                    mesh.vertices = copy.deepcopy(mesh.vertices)
                if mesh.vertices[0].indices is not None:
                    # Remap indices from local indices to global indices
                    palette_indices = set()
                    for v in mesh.vertices:
                        indices = [0, 0, 0, 0]
                        for idx_idx, (idx, wgt) in enumerate(zip(v.indices[::-1], v.weights)):
                            if wgt > 0:
                                palette_indices.add(idx)
                            if idx < len(binary.skinning_data.matrix_palette):
                                indices[idx_idx] = binary.skinning_data.matrix_palette[idx]
                            else:
                                indices[idx_idx] = 0
                                has_bad_vidxs = True
                        v.indices = indices

                    # Link IBPMs to the nodes they are relative to
                    palette_indices = sorted(palette_indices)
                    node_idx = mesh.node
                    for palette_idx in palette_indices:
                        weighted_node_idx = binary.skinning_data.matrix_palette[palette_idx]
                        weighted_ibpm     = binary.skinning_data.ibpms[palette_idx]
                        bpm               = invert_transform_matrix(transposed_mat4x4_to_mat4x3(weighted_ibpm))
                        
                        if weighted_node_idx not in nodes_with_ibpms:
                            nodes_with_ibpms[weighted_node_idx] = []
                        nodes_with_ibpms[weighted_node_idx].append((node_idx, bpm))

        # Now construct bind poses for bones
        world_pose_matrices = [None]*len(bones)
        world_pose_matrices[0] = transforms_to_matrix(bones[0].position, bones[0].rotation, [1., 1., 1.])
        world_rest_matrices = [None]*len(bones)
        world_rest_matrices[0] = transforms_to_matrix(bones[0].position, bones[0].rotation, bones[0].scale)
        for i, bone in enumerate(bones[1:]):
            i = i+1
            local_bpm = transforms_to_matrix(bone.position, bone.rotation, [1., 1., 1.])
            world_pose_matrices[i] = multiply_transform_matrices(world_pose_matrices[bone.parent_idx], local_bpm)
            local_rpm = transforms_to_matrix(bone.position, bone.rotation, bone.scale)
            world_rest_matrices[i] = multiply_transform_matrices(world_rest_matrices[bone.parent_idx], local_rpm)
            
        for i, bone in enumerate(bones):
            if i in nodes_with_ibpms:
                # Average together all bpms for the node
                # Hopefully they're all similar
                contributing_matrices = []
                for node_idx, bpm in nodes_with_ibpms[i]:
                    world_matrix = multiply_transform_matrices(world_rest_matrices[node_idx], bpm)
                    contributing_matrices.append(normalise_transform_matrix_scale(world_matrix))

                n = len(contributing_matrices)
                bone.bind_pose_matrix = [sum([m[comp_idx] for m in contributing_matrices])/n for comp_idx in range(12)]
            else:
                bone.bind_pose_matrix = normalise_transform_matrix_scale(world_pose_matrices[i])
         
        if has_bad_vidxs and warnings is not None:
            warnings.append("Vertex indices were detected that overflow the bind pose matrix buffer. These have been remapped to the root node.")
        return bones, meshes, cameras, lights, epls, bb_min, bb_max, bs_centre, bs_radius, flag_3
        
    @staticmethod
    def to_binary(bones, meshes, cameras, lights, epls, keep_bounding_box, keep_bounding_sphere, overrides, flag_3, copy_verts=True):
        binary = ModelPayload()
        binary.flags.flag_3 = flag_3
        
        # At this point, the bone indices in the mesh binaries are global.
        # Need to convert them to "local" matrix palette bones at the end of 
        # the function.
        binary.root_node, old_node_id_to_new_node_id_map, mesh_binaries = NodeInterface.list_to_binary_node_tree(bones, meshes, cameras, lights, epls)


        #########################
        # CREATE MATRIX PALETTE #
        #########################
        binary.flags.has_skin_data = False
        for mesh_binary, mesh_node_id in mesh_binaries:
            if mesh_binary.flags.has_weights:
                binary.flags.has_skin_data = True
                break
            
        # Create the world rest pose matrices
        rest_pose_matrices = [None]*len(bones)
        for i, bone in enumerate(bones):
            rest_pose_matrices[i] = build_rest_pose(bone, bones)
            
        if binary.flags.has_skin_data:
            ibpms = []
            matrix_palette = []
            matrix_cache = {}
            index_lookup = {}
            for mesh_binary, mesh_node_id in mesh_binaries[::-1]:
                node_matrix = rest_pose_matrices[mesh_node_id]
                
                if mesh_binary.flags.has_weights:
                    # Find all indices
                    # Track unweighted indices and weighted indices separately,
                    # because unweighted indices can be merged into a single
                    # index because they don't matter
                    indices = set()
                    local_unweighted_indices = set()
                    for vertex in mesh_binary.vertices:
                        for idx, wgt in zip(vertex.indices[::-1], vertex.weights[::-1]):
                            if wgt == 0:
                                local_unweighted_indices.add(idx)
                            else:
                                indices.add(idx)
                    
                    # Deal with unweighted
                    for idx in sorted(local_unweighted_indices):
                        index_lookup[(mesh_node_id, idx)] = 0
                    
                    # Deal with weighted
                    for idx in sorted(indices):        
                        index_matrix = bones[idx].bind_pose_matrix
                        ibpm = multiply_transform_matrices(invert_transform_matrix(index_matrix), node_matrix)
                        
                        if idx not in matrix_cache:
                            matrix_cache[idx] = {}
                        
                        matching_matrix_found = False
                        for palette_idx, palette_ibpm in matrix_cache[idx].items():
                            if all(are_transform_matrices_close(ibpm, palette_ibpm, rot_tol=0.001, trans_tol=0.01)):
                                index_lookup[(mesh_node_id, idx)] = palette_idx
                                matching_matrix_found = True
                                break
                            
                        if not matching_matrix_found:
                            palette_idx = len(matrix_palette)
                            matrix_cache[idx][palette_idx] = ibpm
                            matrix_palette.append(old_node_id_to_new_node_id_map[idx])
                            ibpms.append(ibpm)
                            index_lookup[(mesh_node_id, idx)] = palette_idx
            
            binary.skinning_data.matrix_palette = matrix_palette
            binary.skinning_data.ibpms = [mat4x3_to_transposed_mat4x4(ibpm) for ibpm in ibpms]
            binary.skinning_data.bone_count = len(matrix_palette)
            
            all_indices = set()
            # REMAP VERTEX INDICES
            for mesh, mesh_node_id in mesh_binaries:
                if copy_verts:
                    mesh.vertices = copy.deepcopy(mesh.vertices)
                if mesh.vertices[0].indices is not None:
                    for v in mesh.vertices:
                        indices = [index_lookup[(mesh_node_id, idx)] for idx in v.indices]
                        all_indices.update(indices)
                        for wgt_idx, wgt in enumerate(v.weights):
                            if wgt == 0:
                                indices[wgt_idx] = 0
                        v.indices = indices[::-1]
        
        if keep_bounding_box:
            binary.flags.has_bounding_box = True
            bounding_box = overrides.bounding_box
            if bounding_box.enabled:
                binary.bounding_box_min_dims = bounding_box.min_dims
                binary.bounding_box_max_dims = bounding_box.max_dims
            else:
                binary.autocalc_bounding_box()
            
        if keep_bounding_sphere:
            binary.flags.has_bounding_sphere = True
            bounding_sph = overrides.bounding_sphere
            if bounding_sph.enabled:
                binary.bounding_sphere_centre = bounding_sph.center
                binary.bounding_sphere_radius = bounding_sph.radius
            else:
                binary.autocalc_bounding_sphere()
        
        return binary, old_node_id_to_new_node_id_map
    