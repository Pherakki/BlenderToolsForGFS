import traceback

import numpy as np


class LoopCandidate:
    def __init__(self, vertex_id, face_id, face_normal, face_centre, data):
        self.vert_id = vertex_id
        self.face_id = face_id
        self.face_normal = face_normal
        self.face_centre = face_centre
        self.data = data


class BlenderVertexInfo:
    def __init__(self, position, indices, weights):
        self.position = position
        self.indices = indices
        self.weights = weights


def merge_vertices(vertices, triangles, merge_vertices, errorlog):
    """
    Given a list of input vertices and polygons, merge vertices with the same position attribute with face normals
    within 90 degrees of the normal of the best-fitting plane of the centres of all faces associated with that position.
    This process will cause any loose vertices in the input collection to be lost on output.
    Outputs:
    a list of objects containing positions, bone indices, and bone weights to be turned into Blender vertices,
    a list of triangles mapped to the new vertices,
    a map of (new_face_idx, new_vert_idx) to (old_face_idx, old_vert_idx)
    """
    exception_generated = False
    try:
        if merge_vertices:
            # First get all vertex-face pairs
            # We plan to merge some of these into Blender vertices (i.e. collections of VBO vertices with the same position)
            # However, we need to ensure that e.g. vertices making up faces with opposite normals don't get merged unless they
            # form a boundary of the polygon
            # So in this process, we'll also calculate the face normals and centres
            # NOTE: THIS WILL DROP ANY LOOSE VERTICES!!!
            # Ideally we shouldn't even both with the opposite-normal merging and just
            # go with an algorithm that prevents any faces being removed.
            # So although this algorithm works... there's definitely stuff that should
            # be added to it.
            loop_candidates = []
            for triangle_idx, triangle in enumerate(triangles):
                vert_positions = [np.array(vertices[vert_idx].position) for vert_idx in triangle]
                edge_1 = vert_positions[1] - vert_positions[0]
                edge_2 = vert_positions[2] - vert_positions[1]
                face_normal = np.cross(edge_1, edge_2)
                face_centre = np.mean(vert_positions, axis=0)
                for vert_idx in triangle:
                    loop_candidates.append(LoopCandidate(vert_idx, triangle_idx, face_normal, face_centre, vertices[vert_idx]))
    
            # Now, loop over the loop candidates and collect them by position
            # We'll split these collections by face normals after the collections have been populated
            # Can this list be 'consumed' element-by-element by popping elements off the front to waste less memory?
            grouped_loop_candidates = {}
            for loop_candidate in loop_candidates:
                pos = tuple(loop_candidate.data.position)
                if pos not in grouped_loop_candidates:
                    grouped_loop_candidates[pos] = []
                grouped_loop_candidates[pos].append(loop_candidate)
    
            # Now build the final list of unique loops going into each vertex - these will form the basis of the Blender loops
            new_vertices = []
            old_facevert_to_new_vert = {}
            for position, candidate_group in grouped_loop_candidates.items():
                start_idx = len(new_vertices)
                group_1 = []
                group_2 = []
                all_centres = np.array([candidate_loop.face_centre for candidate_loop in candidate_group])
                # Now find the plane closest to all the face centres
                # We'll store this as the associated covector; i.e. the plane normal
                plane_basis = np.linalg.svd((all_centres - np.mean(all_centres, axis=0)).T)[0]
                covector = plane_basis[:, -1]
                # This covector defines a plane of separation we can use to split the candidate loops into two groups: aligned
                # with and anti-aligned with the plane of separation normal
                # Basically, if we have two surfaces directly on top of each other but with opposite normals,
                # this technique will allow us to separate which loop candidates should go into the "upper" surface and which
                # should go into the "lower" surface
                for old_facevertex in candidate_group:
                    test_normal = old_facevertex.face_normal
                    (group_1 if np.dot(covector, test_normal) >= 0 else group_2).append(old_facevertex)
    
                # Ensure that group 1 will always have at least one element in it
                if len(group_2) > len(group_1):
                    group_1, group_2 = group_2, group_1
    
                # Assume that all loops are weighted the same - no support for non-manifold data here
                # This would require making cuts in the manifold, which is fine, it's just annoying to
                # add to the algorithm and is unlikely to be required..?
                new_vertices.append(BlenderVertexInfo(position, group_1[0].data.indices, group_1[0].data.weights))
                for old_facevert in group_1:
                    old_facevert_to_new_vert[(old_facevert.face_id, old_facevert.vert_id)] = start_idx
                if len(group_2):
                    new_vertices.append(BlenderVertexInfo(position, group_2[0].data.indices, group_2[0].data.weights))
                    for old_facevert in group_2:
                        old_facevert_to_new_vert[(old_facevert.face_id, old_facevert.vert_id)] = start_idx + 1
    
            # Now we can generate some new triangles based on our merged vertices
            new_triangles = []
            new_facevert_to_old_facevert_map = {}
            for face_id, triangle in enumerate(triangles):
                new_triangle = []
                for vert_id in triangle:
                    new_vert_id = old_facevert_to_new_vert[(face_id, vert_id)]
                    new_triangle.append(new_vert_id)
                    new_facevert_to_old_facevert_map[(face_id, new_vert_id)] = (face_id, vert_id)
                new_triangles.append(new_triangle)
    
            return new_vertices, new_triangles, new_facevert_to_old_facevert_map
    except Exception as e:
        errorlog.log_warning_message(f"Vertex merging failed because '{str(e)}'- falling back to unmerged vertices.")
        print(''.join(traceback.TracebackException.from_exception(e).format()))
        exception_generated = True
    
    if not merge_vertices or exception_generated:
        new_vertices = []
        for vert in vertices:
            new_vertices.append(BlenderVertexInfo(vert.position, vert.indices, vert.weights))
        new_facevert_to_old_facevert_map = {}
        for face_id, triangle in enumerate(triangles):
            for vert_id in triangle:
                new_facevert_to_old_facevert_map[(face_id, vert_id)] = (face_id, vert_id)
        return new_vertices, triangles, new_facevert_to_old_facevert_map
    
def facevert_to_loop_lookup(new_facevert_to_old_facevert_map, bpy_mesh, gfs_mesh):
    # Get the loop data
    n_loops = len(bpy_mesh.loops)
    bpy_loop_to_gfs_vert = {}
    bpy_vert_to_gfs_verts = {}
    for new_poly_idx, poly in enumerate(bpy_mesh.polygons):
        for loop_idx in poly.loop_indices:
            assert loop_idx not in bpy_loop_to_gfs_vert, "Loop already exists!"
            new_vert_idx = bpy_mesh.loops[loop_idx].vertex_index
            # Take only the vert id from the old (face_id, vert_id) pair
            old_vert_idx = new_facevert_to_old_facevert_map[(new_poly_idx, new_vert_idx)][1]
            bpy_loop_to_gfs_vert[loop_idx] = old_vert_idx
            
            if new_vert_idx not in bpy_vert_to_gfs_verts:
                bpy_vert_to_gfs_verts[new_vert_idx] = []
            bpy_vert_to_gfs_verts[new_vert_idx].append(old_vert_idx)

    loop_data = [gfs_mesh.vertices[bpy_loop_to_gfs_vert[loop_idx]] for loop_idx in range(n_loops)]
    
    return loop_data, bpy_vert_to_gfs_verts
    