import copy

from ...Utils.Matrices import transforms_to_matrix, multiply_transform_matrices, are_matrices_close, invert_transform_matrix, ibpm_to_transform_matrix, bake_scale_into_position
from ..CommonStructures.SceneNode import NodeInterface
from .Binary import ModelPayload


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
        