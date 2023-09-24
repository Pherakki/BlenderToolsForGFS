def bpy_mesh_to_VBO_IBO(bpy_mesh, get_vertex_data, loop_data, vertex_constructor):
    """
    A function to convert a Blender mesh to a Vertex Buffer Object and an
    Index Buffer Object. The VBO is generated from unique sets of loop attributes
    combined with vertex data from the vertex the loop is associated with.
    Inputs:
        - bpy_mesh:           A Blender Mesh (bpy.types.Mesh)
        - get_vertex_data:    A callable that returns a set of data from an input 
                              vertex and vertex index
        - loop_data:          A struct-of-arrays containing loop attribute data.
        - vertex_constructor: A function that takes in the outputs of get_vertex_data,
                              plus a list of loop attributes extracted from loop_data,
                              and returns a user-defined object representing a vertex.
    Outputs:
        - MeshBuffers object: An object containing the VBO, IBO, and a lookup table
                              that when indexed by an index of the VBO, returns the
                              index of the vertex in the Blender Mesh that element
                              of the VBO was constructed from.
    """
    # Get vertex -> loop and loop -> face maps
    vidx_to_lidx_map = generate_vertex_to_loops_map(bpy_mesh)
    lidx_to_fidx_map = generate_loop_to_face_map(bpy_mesh)
    
    # Make loop -> unique value lookup maps
    # This should just be a splat of all vertex attributes
    # normals, tangents, binormals, UVs, colors, etc.
    loop_idx_to_key        = [key for key in (zip(*loop_data))]
    unique_val_map         = {key: i for i, key in enumerate(list(set(loop_idx_to_key)))}
    loop_idx_to_unique_key = {i: unique_val_map[key] for i, key in enumerate(loop_idx_to_key)}
    
    exported_vertices = []
    faces = [{l: bpy_mesh.loops[l].vertex_index for l in f.loop_indices} for f in bpy_mesh.polygons]
    vbo_vert_to_bpy_vert = {}
    for vert_idx, linked_loops in vidx_to_lidx_map.items():
        vertex = bpy_mesh.vertices[vert_idx]
        unique_ids = {i: [] for i in list(set(loop_idx_to_unique_key[ll] for ll in linked_loops))}
        for ll in linked_loops:
            unique_ids[loop_idx_to_unique_key[ll]].append(ll)
        unique_values = [(loop_idx_to_key[lids[0]], lids) for id_, lids in unique_ids.items()]
        
        vertex_data = get_vertex_data(vert_idx, vertex)
        if vertex_data is None:
            continue
        
        # Now split the verts by their loop data
        for unique_value, loops_with_this_value in unique_values:
            # Create the VBO entry
            vb = vertex_constructor(vertex_data, unique_value)

            # Update the vbo -> bpy map
            n_verts = len(exported_vertices)
            vbo_vert_to_bpy_vert[len(exported_vertices)] = vert_idx
            exported_vertices.append(vb)

            # Update the polygon map
            for l in loops_with_this_value:
                face_idx = lidx_to_fidx_map[l]
                faces[face_idx][l] = n_verts

    # Create IBO from faces
    faces = [list(face_verts.values()) for face_verts in faces]

    return MeshBuffers(exported_vertices, faces, vbo_vert_to_bpy_vert)


class MeshBuffers:
    __slots__ = ("vertices", "indices", "vbo_vert_to_bpy_vert_map")
    
    def __init__(self, vertices, indices, vbo_vert_to_bpy_vert_map):
        self.vertices = vertices
        self.indices  = indices
        self.vbo_vert_to_bpy_vert_map = vbo_vert_to_bpy_vert_map


def generate_vertex_to_loops_map(bpy_mesh):
    vidx_to_lidxs = {}
    for loop in bpy_mesh.loops:
        if loop.vertex_index not in vidx_to_lidxs:
            vidx_to_lidxs[loop.vertex_index] = []
        vidx_to_lidxs[loop.vertex_index].append(loop.index)
    return vidx_to_lidxs


def generate_loop_to_face_map(bpy_mesh):
    lidx_to_fidx = {}
    for face in bpy_mesh.polygons:
        for loop_idx in face.loop_indices:
            lidx_to_fidx[loop_idx] = face.index
    return lidx_to_fidx
