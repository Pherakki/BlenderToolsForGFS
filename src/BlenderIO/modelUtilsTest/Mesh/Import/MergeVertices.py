from collections import defaultdict
import traceback

import bpy
import numpy as np


class LoopCandidate:
    __slots__ = ("vert_id", "face_id", "face_normal", "face_centre")
    
    def __init__(self, vertex_id, face_id, face_normal, face_centre):
        self.vert_id = vertex_id
        self.face_id = face_id
        self.face_normal = face_normal
        self.face_centre = face_centre


class ModelGeometry:
    __slots__ = ("vertices", 
                 "triangles", 
                 "new_facevert_to_old_facevert_map",
                 "ignored_vertices")
    
    def __init__(self, vertices, triangles, new_facevert_to_old_facevert_map, ignored_vertices):
        self.vertices                         = vertices
        self.triangles                        = triangles
        self.new_facevert_to_old_facevert_map = new_facevert_to_old_facevert_map
        self.ignored_vertices                 = ignored_vertices


def sanitize_mergeable_vertices(vertices, VertexType):
    bad_vertices = []
    for i, v in enumerate(vertices):
        if VertexType.is_invalid(v):
            bad_vertices.append(i)
    return bad_vertices


def merge_vertices(vertices, triangles, VertexType, ignored_vertices=None, sanitize_vertices=True):
    # TODOs:
    # TODO: Add support for loose vertices
    # TODO: Add support for multiple overlapping "top" and "bottom" surfaces
    # TODO: Add support for non-triangular faces
    
    # Remove any vertices we've been told to ignore, for example because they
    # contain invalid data.
    # This option is offered internally so that the facevert map can be built
    # in reference to the "full" vertex indices, not the "clean" ones,
    # since only a subset of vertex data enters this function.
    ignore_verts_set = set()
    if sanitize_vertices:
        ignore_verts_set.update(sanitize_mergeable_vertices(vertices, VertexType))
    if ignored_vertices is not None:
        ignore_verts_set.update(ignored_vertices)
    if len(ignore_verts_set):
        triangles = [tri for tri in triangles if all(idx not in ignore_verts_set for idx in tri)]
        
    # Step 1): First get all vertex-face pairs.
    # We plan to merge some of these into Blender vertices (i.e. collections of input vertices with the same position).
    # However, we need to ensure that e.g. vertices making up faces with opposite normals don't get merged unless they
    # form a boundary of the polygon.
    # So in this process, we'll also calculate the face normals and centres.
    loop_candidates = []
    for triangle_idx, triangle in enumerate(triangles):
        vert_positions = [np.array(VertexType.get_position(vertices[vert_idx])) for vert_idx in triangle]
        edge_1 = vert_positions[1] - vert_positions[0]
        edge_2 = vert_positions[2] - vert_positions[1]
        
        face_normal = np.cross(edge_1, edge_2)
        face_centre = np.mean(vert_positions, axis=0)
        for vert_idx in triangle:
            loop_candidates.append(LoopCandidate(vert_idx, triangle_idx, face_normal, face_centre))

    # Step 2): Bin the Loop Candidates into groups by position and any marked attributes.
    # Each of these groups represents all data vertices that *could* be merged into a single
    # Blender vertex. In the next step we will determine how many vertices need to be generated
    # per group.
    grouped_loop_candidates = {}
    for loop_candidate in loop_candidates:
        vert_id = loop_candidate.vert_id
        v = vertices[vert_id]
        key = (tuple(VertexType.get_position(v)), *(tuple(a) for a in VertexType.get_merge_attributes(v)))
        if key not in grouped_loop_candidates:
            grouped_loop_candidates[key] = []
        grouped_loop_candidates[key].append(loop_candidate)

    # Step 3): Find out how few vertices the Loop Groups can be merged into.
    # The Loop Candidates in each subgroup will form the basis of the Blender loops.
    new_vertices = []
    old_facevert_to_new_vert = {}
    for key, candidate_group in grouped_loop_candidates.items():
        # TODO: If any duplicate planes exist, they need to be separated here
        
        # Do this by first checking if any face centres are the same,
        # and for those faces check if all the vertex positions are the same
        all_centres = np.array([candidate_loop.face_centre for candidate_loop in candidate_group])
        
        # Now find the plane closest to all the face centres.
        # We'll store this as the associated covector; i.e. the plane normal.
        plane_basis = np.linalg.svd((all_centres - np.mean(all_centres, axis=0)).T)[0]
        covector = plane_basis[:, -1]
        
        # This covector defines a plane of separation we can use to split the candidate loops into two groups: aligned
        # with and anti-aligned with the plane-of-separation normal.
        # Basically, if we have two surfaces directly on top of each other but with opposite normals,
        # this technique will allow us to separate which loop candidates should go into the "upper" surface and which
        # should go into the "lower" surface
        
        start_idx = len(new_vertices)
        group_1 = []
        group_2 = []
        for old_facevertex in candidate_group:
            test_normal = old_facevertex.face_normal
            (group_1 if np.dot(covector, test_normal) >= 0 else group_2).append(old_facevertex)
        
        # Ensure that group 1 will always have at least one element in it
        # This just means the following code can be written with the assumption that group_1 is never empty
        if len(group_2) > len(group_1):
            group_1, group_2 = group_2, group_1
        
        # Finally, output the merged vertex (and one for the lower surface if required)
        new_vertices.append(VertexType.from_unmerged([vertices[lc.vert_id] for lc in candidate_group]))
        for old_facevert in group_1:
            old_facevert_to_new_vert[(old_facevert.face_id, old_facevert.vert_id)] = start_idx
        if len(group_2):
            # Requires duplicate lower surface vertex
            new_vertices.append(VertexType.from_unmerged([vertices[lc.vert_id] for lc in candidate_group]))
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

    return ModelGeometry(new_vertices, new_triangles, new_facevert_to_old_facevert_map, ignore_verts_set)


def unmerged_vertices(vertices, triangles, VertexType):
    """
    Returns the same input vertices and triangles in a library-compatible format.
    """
    new_vertices = []
    for v in vertices:
        new_vertices.append(VertexType.from_unmerged([v]))
    new_facevert_to_old_facevert_map = {}
    for face_id, triangle in enumerate(triangles):
        for vert_id in triangle:
            new_facevert_to_old_facevert_map[(face_id, vert_id)] = (face_id, vert_id)
    return ModelGeometry(new_vertices, triangles, new_facevert_to_old_facevert_map, set())


def try_merge_vertices(vertices, triangles, VertexType, ignored_vertices=None, sanitize_vertices=True, attempt_merge=True, errorlog=None):
    """
    Given a list of input vertices and polygons, merge vertices with the same position attribute with face normals
    within 90 degrees of the normal of the best-fitting plane of the centres of all faces associated with that position.
    """ 
    exception_generated = False
    try:
        if attempt_merge:
            return merge_vertices(vertices, triangles, VertexType, ignored_vertices, sanitize_vertices)
    except Exception as e:
        if errorlog is None:
            print(''.join(traceback.TracebackException.from_exception(e).format()))
        else:
            errorlog.log_warning_message(f"Vertex merging failed - falling back to unmerged vertices. Reason: '{str(e)}'")
        exception_generated = True
    
    if not attempt_merge or exception_generated:
        return unmerged_vertices(vertices, triangles, VertexType)


class Loops:
    def __init__(self, cmi, model_verts):
        self.cmi         = cmi
        self.model_verts = model_verts
        
    def __len__(self):
        return len(self.cmi.bpy_mesh.loops)
    
    def __iter__(self):
        for vert_idx in self.cmi.loops_to_modelverts_map:
            yield self.model_verts[vert_idx]
        
    def __getitem__(self, index):
        return self.model_verts[self.cmi.loops_to_modelverts_map[index]]


class ConstructedMeshInfo:
    __slots__ = ("bpy_mesh", "vertices", "faces", "_loops", "loops_to_modelverts_map", "verts_to_modelverts_map")
    
    def __init__(self, bpy_mesh, vertices, faces, loops_to_modelverts_map, verts_to_modelverts_map, model_verts):
        self.bpy_mesh = bpy_mesh
        self.vertices = vertices
        self.faces    = faces
        self._loops  = Loops(self, model_verts)
        
        self.loops_to_modelverts_map = loops_to_modelverts_map
        self.verts_to_modelverts_map = verts_to_modelverts_map
        
    @property
    def loops(self):
        return self._loops


def create_merged_mesh(mesh_name, vertices, faces, VertexType, sanitize_vertices=True, attempt_merge=True, errorlog=None):
    geometry = try_merge_vertices(vertices, faces, VertexType, None, sanitize_vertices, attempt_merge, errorlog)

    ###############
    # CREATE MESH #
    ###############
    # Init mesh
    bpy_mesh = bpy.data.meshes.new(name=mesh_name)
    bpy_mesh.from_pydata([v.position for v in geometry.vertices], [], geometry.triangles)
    
    #################
    # ADD LOOP DATA #
    #################
    # Get the loop data
    new_facevert_to_old_facevert_map = geometry.new_facevert_to_old_facevert_map
    loops_to_modelverts_map = np.empty((len(bpy_mesh.loops)), dtype=np.uint32)
    verts_to_modelverts_map = defaultdict(set)
    for new_poly_idx, poly in enumerate(bpy_mesh.polygons):
        for loop_idx in poly.loop_indices:
            bpy_vert_idx = bpy_mesh.loops[loop_idx].vertex_index
            # Take only the vert id from the old (face_id, vert_id) pair
            mdl_vert_idx = new_facevert_to_old_facevert_map[(new_poly_idx, bpy_vert_idx)][1]
            
            loops_to_modelverts_map[loop_idx] = mdl_vert_idx
            verts_to_modelverts_map[bpy_vert_idx].add(mdl_vert_idx)
    verts_to_modelverts_map = {k: sorted(v) for k, v in verts_to_modelverts_map.items()}

    # Also need to add in loose vertices here too!
    
    return ConstructedMeshInfo(bpy_mesh, 
                               geometry.vertices,
                               geometry.triangles,
                               loops_to_modelverts_map,
                               verts_to_modelverts_map,
                               vertices)
