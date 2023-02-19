import array

import bpy
from mathutils import Matrix
import numpy as np

from ..WarningSystem.Warning import ReportableError
from ..Utils.Maths import convert_rotation_to_quaternion, convert_Zup_to_Yup
from ..Utils.UVMapManagement import is_valid_uv_map, get_uv_idx_from_name
from ...FileFormats.GFS.SubComponents.CommonStructures.SceneNode.MeshBinary import VertexBinary, VertexAttributes

class NonTriangularFacesError(ReportableError):
    __slots__ = ("mesh", "poly_indices", "prev_obj")
    
    HAS_DISPLAYABLE_ERROR = True
    
    def __init__(self, mesh, poly_indices):
        msg = f"Mesh '{mesh.name}' has {len(poly_indices)} non-triangular faces. Ensure that all faces are triangular before exporting."
        super().__init__(msg)
        self.mesh = mesh
        self.poly_indices = poly_indices
        self.prev_obj = None
        
    def showErrorData(self):
        self.prev_obj = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = self.mesh
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        
        for pidx in self.poly_indices:
            self.mesh.data.polygons[pidx].select_set(True)
        
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type="FACE")
        
    def hideErrorData(self):
        bpy.context.view_layer.objects.active = self.mesh
        bpy.ops.object.mode_set(mode="OBJECT")
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        if self.prev_obj is not None:
            bpy.context.view_layer.objects.active = self.prev_obj
        

class TooManyIndicesError(ReportableError):
    __slots__ = ("mesh", "vertex_indices", "prev_obj")
    
    HAS_DISPLAYABLE_ERROR = True
    
    def __init__(self, mesh, vertex_indices):
        msg = f"Mesh '{mesh.name}' has {len(vertex_indices)} vertices that belong to more than 4 vertex groups. Ensure that all vertices belong to, at most, 4 groups before exporting."
        super().__init__(msg)
        self.mesh = mesh
        self.vertex_indices = vertex_indices
        self.prev_obj = None
        
    def showErrorData(self):
        self.prev_obj = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = self.mesh
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        
        for vidx in self.vertex_indices:
            self.mesh.data.vertices[vidx].select_set(True)
        
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type="VERTEX")
        
    def hideErrorData(self):
        bpy.context.view_layer.objects.active = self.mesh
        bpy.ops.object.mode_set(mode="OBJECT")
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        if self.prev_obj is not None:
            bpy.context.view_layer.objects.active = self.prev_obj
        

def export_mesh_data(gfs, armature, errorlog):
    meshes = [obj for obj in armature.children if obj.type == "MESH"]
    material_names = set()
    for bpy_mesh_object in meshes:
        node_id = len(gfs.bones)
        
        bind_pose_matrix = convert_Zup_to_Yup(armature.matrix_world.inverted() @ bpy_mesh_object.matrix_world)
        
        # Keep this code around in case you ever allow meshes to be 
        # parented to anything other that RootNode
        parent_idx = 0
        parent_relative_bind_pose_matrix = bind_pose_matrix
        #parent_relative_bind_pose_matrix = armature.data.bones[gfs.bones[parent_idx].name].matrix_local @ bind_pose_matrix
        pos, rot, scl = parent_relative_bind_pose_matrix.decompose()
        
        node_props = bpy_mesh_object.data.GFSTOOLS_NodeProperties
        bpm = [*bind_pose_matrix[0], *bind_pose_matrix[1], *bind_pose_matrix[2]]
        gfs_node = gfs.add_node(parent_idx, bpy_mesh_object.name, [pos.x, pos.y, pos.z], [rot.x, rot.y, rot.z, rot.w], [scl.x, scl.y, scl.z], node_props.unknown_float, bpm)        
        for prop in node_props.properties:
            gfs_node.add_property(*prop.extract_data(prop))
        
        create_mesh(gfs, bpy_mesh_object, armature, node_id, material_names, errorlog)
        attached_meshes =  [obj for obj in bpy_mesh_object.children if obj.type == "MESH"]
        for bpy_submesh_object in attached_meshes:
            create_mesh(gfs, bpy_submesh_object, armature, node_id, material_names, errorlog)
        
    return sorted(material_names)


def create_mesh(gfs, bpy_mesh_object, armature, node_id, export_materials, errorlog):
    # Extract vertex and polygon data from the bpy struct
    bone_names = {bn.name: i for i, bn in enumerate(gfs.bones)}
    vertices, indices = extract_vertex_data(bpy_mesh_object, bone_names)
    
    # Check if any of the mesh data is invalid... we'll accumulate these
    # into an error report for the user.
    # 1) Check for any non-triangular faces
    bad_polys = []
    for pidx, poly in enumerate(bpy_mesh_object.data.polygons):
        if len(poly.vertices) != 3:
            bad_polys.append(pidx)
    if len(bad_polys):
        errorlog.log_error(NonTriangularFacesError(bpy_mesh_object, bad_polys))
    # 2) Check for vertices belonging to more than 4 vertex groups
    bad_vertices = []
    for vidx, vertex in enumerate(bpy_mesh_object.data.vertices):
        if len(vertex.groups) > 4:
            bad_vertices.append(vidx)
    if len(bad_vertices):
        errorlog.log_error(TooManyIndicesError(bpy_mesh_object, bad_vertices))
    
    # Now convert mesh to GFS structs... don't worry if it contains invalid data,
    # we're going to throw an exception at the end of export if any of the meshes
    # were flagged as invalid
    mesh_props = bpy_mesh_object.data.GFSTOOLS_MeshProperties
    mesh = gfs.add_mesh(node_id, vertices, 
                        bpy_mesh_object.active_material.name if bpy_mesh_object.active_material is not None else None, 
                        [fidx for face in indices for fidx in face], 
                        [], # Morphs! 
                        mesh_props.unknown_0x12, 
                        mesh_props.unknown_float_1 if mesh_props.has_unknown_floats else None,
                        mesh_props.unknown_float_2 if mesh_props.has_unknown_floats else None, 
                        mesh_props.export_bounding_box, 
                        mesh_props.export_bounding_sphere)
    
    mesh.flag_5 = mesh_props.flag_5
    mesh.flag_7 = mesh_props.flag_7
    mesh.flag_8 = mesh_props.flag_8
    mesh.flag_9 = mesh_props.flag_9
    mesh.flag_10 = mesh_props.flag_10
    mesh.flag_11 = mesh_props.flag_11
    mesh.flag_13 = mesh_props.flag_13
    mesh.flag_14 = mesh_props.flag_14
    mesh.flag_15 = mesh_props.flag_15
    mesh.flag_16 = mesh_props.flag_16
    mesh.flag_17 = mesh_props.flag_17
    mesh.flag_18 = mesh_props.flag_18
    mesh.flag_19 = mesh_props.flag_19
    mesh.flag_20 = mesh_props.flag_20
    mesh.flag_21 = mesh_props.flag_21
    mesh.flag_22 = mesh_props.flag_22
    mesh.flag_23 = mesh_props.flag_23
    mesh.flag_24 = mesh_props.flag_24
    mesh.flag_25 = mesh_props.flag_25
    mesh.flag_26 = mesh_props.flag_26
    mesh.flag_27 = mesh_props.flag_27
    mesh.flag_28 = mesh_props.flag_28
    mesh.flag_29 = mesh_props.flag_29
    mesh.flag_30 = mesh_props.flag_30
    mesh.flag_31 = mesh_props.flag_31
    
    if bpy_mesh_object.active_material is not None:
        export_materials.add(bpy_mesh_object.active_material.name)

#####################
# PRIVATE FUNCTIONS #
#####################
def extract_vertex_data(mesh_obj, bone_names):
    # Switch to input variables
    vweight_floor = 0
    
    mesh = mesh_obj.data
    
    # Deal with any zero vectors
    zero_vec = (0., 0., 0.)
    loop_normals = [l.normal for l in mesh.loops]
    lnorms_zero = [tuple(normal) == zero_vec for normal in loop_normals]
    if any(lnorms_zero):
        if not mesh.has_custom_normals:
            mesh.create_normals_split()
        mesh.calc_normals_split()
        res = []
        for j, iszero in enumerate(lnorms_zero):
            res.append(mesh.loops[j].normal if iszero else loop_normals[j])
        mesh.normals_split_custom_set(res)

    vidx_to_lidxs = generate_vertex_to_loops_map(mesh)
    lidx_to_fidx  = generate_loop_to_face_map(mesh)
    export_verts, export_faces = split_verts_by_loop_data(bone_names, mesh_obj, vidx_to_lidxs, lidx_to_fidx, vweight_floor)
    
    return export_verts, export_faces

def generate_vertex_to_loops_map(mesh):
    vidx_to_lidxs = {}
    for loop in mesh.loops:
        if loop.vertex_index not in vidx_to_lidxs:
            vidx_to_lidxs[loop.vertex_index] = []
        vidx_to_lidxs[loop.vertex_index].append(loop.index)
    return vidx_to_lidxs

def generate_loop_to_face_map(mesh):
    lidx_to_fidx = {}
    for face in mesh.polygons:
        for loop_idx in face.loop_indices:
            lidx_to_fidx[loop_idx] = face.index
    return lidx_to_fidx


def split_verts_by_loop_data(bone_names, mesh_obj, vidx_to_lidxs, lidx_to_fidx, vweight_floor):
    mesh = mesh_obj.data
    has_uvs = len(mesh.uv_layers) > 0

    exported_vertices = []
    vgroup_verts = {}
    faces = [{l: mesh.loops[l].vertex_index for l in f.loop_indices} for f in mesh.polygons]
    nonempty_groups = get_all_nonempty_vertex_groups(mesh_obj)

    group_map = {g.index: bone_names[g.name] for g in nonempty_groups}
    
    map_ids = list(mesh.uv_layers.keys())[:8]
    colour_map = list(mesh.vertex_colors.keys())[:2]
    n_colours = len(colour_map)

    use_normals   = mesh.GFSTOOLS_MeshProperties.export_normals
    use_tangents  = mesh.GFSTOOLS_MeshProperties.export_tangents
    use_binormals = mesh.GFSTOOLS_MeshProperties.export_binormals
    map_name = map_ids[0] if len(map_ids) else 'dummy'
    can_export_tangents = has_uvs and mesh.uv_layers.get(map_name) is not None and (use_normals and (use_tangents or use_binormals))

    if can_export_tangents:
        mesh.calc_tangents(uvmap=map_name)

    sigfigs = 4
    nloops = len(mesh.loops)

    # Extract normals
    if use_normals:
        normals = [(elem,) for elem in fetch_data(mesh.loops, "normal", sigfigs)]
    else:
        normals = [tuple()]*nloops

    # Extract UVs
    UV_data = [[None for _ in range(nloops)]]*8
    for map_id in map_ids:
        if is_valid_uv_map(map_id): # Need to throw a warning here
            idx = get_uv_idx_from_name(map_id)
            if idx < 8:
                UV_data[idx] = fetch_data(mesh.uv_layers[map_id].data, "uv", sigfigs+2)
    if len(UV_data):
        UV_data = [tuple(elems) for elems in zip(*UV_data)]
    else:
        UV_data = [tuple()]*nloops

    # Extract colours
    col_data = [None]*n_colours
    for i, map_id in enumerate(colour_map):
        col_data[i] = fetch_data(mesh.vertex_colors[map_id].data, "color", sigfigs)
    if len(col_data):
        col_data = [tuple(elems) for elems in zip(*col_data)]
    else:
        col_data = [tuple()]*nloops

    # Extract tangents
    if can_export_tangents:
        tangents = [(elem,) for elem in fetch_tangent(mesh.loops, sigfigs)]
    else:
        tangents = [tuple()]*nloops

    # Calculate binormals
    if use_binormals and can_export_tangents:
        bitangents = [(tuple(round_to_sigfigs(tangent[0][3] * np.cross(normal, tangent[0][:3]), sigfigs)),) for normal, tangent in zip(normals, tangents)]
    else:
        bitangents = [tuple()]*nloops

    # Make loop -> unique value lookup maps
    loop_idx_to_key = [key for key in (zip(normals, UV_data, col_data, tangents, bitangents))]
    unique_val_map = {key: i for i, key in enumerate(list(set(loop_idx_to_key)))}
    loop_idx_to_unique_key = {i: unique_val_map[key] for i, key in enumerate(loop_idx_to_key)}

    for vert_idx, linked_loops in vidx_to_lidxs.items():
        vertex = mesh.vertices[vert_idx]
        unique_ids = {i: [] for i in list(set(loop_idx_to_unique_key[ll] for ll in linked_loops))}
        for ll in linked_loops:
            unique_ids[loop_idx_to_unique_key[ll]].append(ll)
        unique_values = [(loop_idx_to_key[lids[0]], lids) for id_, lids in unique_ids.items()]

        for unique_value, loops_with_this_value in unique_values:
            group_indices = [grp for grp in vertex.groups if grp.weight > vweight_floor]
            group_bone_ids = [get_bone_id(mesh_obj, bone_names, grp) for grp in group_indices]
            group_weights = [grp.weight for grp in group_indices]

            # Normalise the group weights
            total_weight = sum(group_weights)
            if total_weight > 0.:
                group_weights = [wght / total_weight for wght in group_weights]

            vb = VertexBinary()
            vb.position = vertex.co
            if len(unique_value[0]): vb.normal = unique_value[0][0]
            for attr_idx, value in zip([VertexAttributes.TEXCOORD0,
                                        VertexAttributes.TEXCOORD1,
                                        VertexAttributes.TEXCOORD2,
                                        VertexAttributes.TEXCOORD3,
                                        VertexAttributes.TEXCOORD4,
                                        VertexAttributes.TEXCOORD5,
                                        VertexAttributes.TEXCOORD6,
                                        VertexAttributes.TEXCOORD7], unique_value[1]):
                vb[attr_idx] = value
            if len(unique_value[2]): vb.color1   = unique_value[2][0]
            if len(unique_value[3]): vb.tangent  = unique_value[3][0]
            if len(unique_value[4]): vb.binormal = unique_value[4][0]
            if len(group_indices):
                n_extra = 4 - len(group_indices)
                vb.indices = [*group_bone_ids, *([0]*n_extra)]
                vb.weights = [*group_weights, *([0]*n_extra)]

            n_verts = len(exported_vertices)
            exported_vertices.append(vb)

            for l in loops_with_this_value:
                face_idx = lidx_to_fidx[l]
                faces[face_idx][l] = n_verts

    faces = [list(face_verts.values()) for face_verts in faces]
    return exported_vertices, faces

def get_all_nonempty_vertex_groups(mesh_obj):
    nonempty_vgs = set()
    for vertex in mesh_obj.data.vertices:
        for group in vertex.groups:
            #if group.weight > vweight_floor:
           nonempty_vgs.add(group.group)
    nonempty_vgs = sorted(list(nonempty_vgs))
    nonempty_vgs = [mesh_obj.vertex_groups[idx] for idx in nonempty_vgs]

    return nonempty_vgs


def round_to_sigfigs(x, p):
    """
    Credit to Scott Gigante
    Taken from https://stackoverflow.com/a/59888924
    Rounds a float x to p significant figures
    """
    x = np.asarray(x)
    x_positive = np.where(np.isfinite(x) & (x != 0), np.abs(x), 10**(p-1))
    mags = 10 ** (p - 1 - np.floor(np.log10(x_positive)))
    return np.round(x * mags) / mags


def fetch_data(obj, element, sigfigs):
    dsize = len(getattr(obj[0], element))
    data = array.array('f', [0.0] * (len(obj) * dsize))
    obj.foreach_get(element, data)
    return [tuple(round_to_sigfigs(datum, sigfigs)) for datum in zip(*(iter(data),) * dsize)]


def fetch_tangent(obj, sigfigs):
    dsize = len(getattr(obj[0], "tangent"))
    data = array.array('f', [0.0] * (len(obj) * dsize))
    obj.foreach_get("tangent", data)

    signs = array.array('f', [0.0] * (len(obj)))
    obj.foreach_get("bitangent_sign", data)
    return [(*round_to_sigfigs(datum, sigfigs), sign) for datum, sign in zip(zip(*(iter(data),) * dsize), signs)]

def get_bone_id(mesh_obj, bone_names, grp):
    group_idx = grp.group
    bone_name = mesh_obj.vertex_groups[group_idx].name
    bone_id = bone_names[bone_name]
    return bone_id
