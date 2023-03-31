import array

import bpy
from mathutils import Matrix
import numpy as np

from ..WarningSystem.Warning import ReportableError
from ..Utils.Maths import convert_rotation_to_quaternion, convert_Zup_to_Yup, BlenderBoneToMayaBone, convert_YDirBone_to_XDirBone
from ..Utils.UVMapManagement import make_uv_map_name, is_valid_uv_map, get_uv_idx_from_name
from ..Utils.UVMapManagement import make_color_map_name, is_valid_color_map, get_color_idx_from_name
from ...FileFormats.GFS.SubComponents.CommonStructures.SceneNode.MeshBinary import VertexBinary, VertexAttributes




class DisplayableVerticesError(ReportableError):
    __slots__ = ("mesh", "vertex_indices", "prev_obj")
    
    HAS_DISPLAYABLE_ERROR = True
    
    def __init__(self, msg, mesh, vertex_indices):
        super().__init__(msg)
        self.mesh = mesh
        self.vertex_indices = vertex_indices
        self.prev_obj = None
        
    def showErrorData(self):
        self.prev_obj = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = self.mesh
        bpy.ops.object.mode_set(mode="OBJECT")
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        
        for vidx in self.vertex_indices:
            self.mesh.data.vertices[vidx].select = True
        
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type="VERT")
        
    def hideErrorData(self):
        bpy.context.view_layer.objects.active = self.mesh
        bpy.ops.object.mode_set(mode="OBJECT")
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        if self.prev_obj is not None:
            bpy.context.view_layer.objects.active = self.prev_obj


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
        bpy.ops.object.mode_set(mode="OBJECT")
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        
        for pidx in self.poly_indices:
            self.mesh.data.polygons[pidx].select = True
        
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
        

class MissingVertexGroupsError(DisplayableVerticesError):
    def __init__(self, mesh, vertex_indices, bone_names):
        newline = '\n'
        msg = f"Mesh '{mesh.name}' has {len(vertex_indices)} vertices weighted to bones that do not exist. These vertices have been selected for you. If you wish to ignore this error, check the 'Strip Missing Vertex Groups' option when exporting. The missing bones are:{newline}{newline.join(bone_names)}"
        super().__init__(msg, mesh, vertex_indices)


class TooManyIndicesError(DisplayableVerticesError):
    def __init__(self, mesh, vertex_indices):
        msg = f"Mesh '{mesh.name}' has {len(vertex_indices)} vertices that belong to more than 4 vertex groups. Ensure that all vertices belong to, at most, 4 groups before exporting."
        super().__init__(msg, mesh, vertex_indices)


class PartiallyUnriggedMeshError(DisplayableVerticesError):
    def __init__(self, mesh, vertex_indices):
        msg = f"Mesh '{mesh.name}' has {len(vertex_indices)}/{len(mesh.data.vertices)} vertices that are unrigged. These vertices have been selected for you."
        super().__init__(msg, mesh, vertex_indices)


def export_mesh_data(gfs, armature, errorlog, log_missing_weights, recalculate_tangents, throw_missing_weight_errors):
    meshes = [obj for obj in armature.children if obj.type == "MESH"]
    material_names = set()
    out = []
    for bpy_mesh_object in meshes:
        node_id = len(gfs.bones)
        out.append((bpy_mesh_object.data, node_id))

        # Convert bpy meshes -> gfs meshes
        gfs_meshes = []
        gfs_meshes.append(create_mesh(gfs, bpy_mesh_object, armature, node_id, material_names, errorlog, log_missing_weights, recalculate_tangents, throw_missing_weight_errors))
        attached_meshes =  [obj for obj in bpy_mesh_object.children if obj.type == "MESH"]
        for bpy_submesh_object in attached_meshes:
            gfs_meshes.append(create_mesh(gfs, bpy_submesh_object, armature, node_id, material_names, errorlog, log_missing_weights, recalculate_tangents, throw_missing_weight_errors))
        
        # Now create the parent node
        parent_idx = 0
        bind_pose_matrix = convert_Zup_to_Yup(bpy_mesh_object.matrix_local)
        parent_relative_bind_pose_matrix = armature.matrix_local.inverted() @ bind_pose_matrix
        
        # Check if we can convert any weighted meshes to node children
        # to save on matrix palette space
        # To do this we'll check if there's single bone we can parent the mesh
        # to
        index_sets = []
        for gm in gfs_meshes:
            indices = set()
            if gm.vertices[0].indices is not None:
                for v in gm.vertices:
                    for idx, wgt in zip(v.indices, v.weights):
                        if wgt > 0:
                            indices.add(idx)                    
            index_sets.append(indices)

        all_indices = set.union(*index_sets)
        mesh_props = bpy_mesh_object.data.GFSTOOLS_MeshProperties
        if len(all_indices) == 1 and mesh_props.permit_unrigged_export:
            # We can re-parent the node to this node and yeet the vertex
            # weights
            node_idx = list(all_indices)[0]
            parent_relative_bind_pose_matrix = (convert_YDirBone_to_XDirBone(armature.data.bones[gfs.bones[node_idx].name].matrix_local).inverted() @ bpy_mesh_object.matrix_local)

            for gm in gfs_meshes:
                for v in gm.vertices:
                    v.indices = None
                    v.weights = None
            parent_idx = node_idx
            
        # Now create the transforms for the node
        pos, rot, scl = parent_relative_bind_pose_matrix.decompose()
        
        # Other crap, create node
        node_props = bpy_mesh_object.data.GFSTOOLS_NodeProperties
        bpm = [*bind_pose_matrix[0], *bind_pose_matrix[1], *bind_pose_matrix[2]]
        gfs_node = gfs.add_node(parent_idx, bpy_mesh_object.name, [pos.x, pos.y, pos.z], [rot.x, rot.y, rot.z, rot.w], [scl.x, scl.y, scl.z], node_props.unknown_float, bpm)        
        for prop in node_props.properties:
            gfs_node.add_property(*prop.extract_data(prop))
    
    return sorted(material_names), out


def extract_morphs(bpy_mesh_object, gfs_vert_to_bpy_vert):
    out = []
    skeys = bpy_mesh_object.data.shape_keys
    if skeys is None:
        return out
    for shp in skeys.key_blocks:
        # This is a fragile way of identifying the basis key - sort it out 
        # later.
        if shp.name == "Basis":
            continue
        
        # The following assumes that the "Basis" shapekey is exactly the 
        # underlying mesh.
        # It *should* be frankly, but might want to export the basis positions
        # instead of the vertex positions if the basis is present...
        # Sounds *fun*...
        # If there's *multiple* bases / relative keys, that's also something
        # that just can't be exported, unless the relative keys all form chains
        # going back to the singular root Basis key.
        # Since shape keys are stored with absolute positions, we're just gonna
        # assume that they are all relative to the edit mesh and export those
        # positions. Even if there's relative-key chains, the final positions 
        # of the shape keys will get exported, although the inheritance chain 
        # will be removed.
        # Here we also assume that the gfs_vert_to_bpy_vert is a sorted
        # dict from 0->max; the vertex splitter function should create
        # such a dict.
        verts = bpy_mesh_object.data.vertices
        position_deltas = [(tuple(shp.data[bpy_idx].co - verts[bpy_idx].co)) 
                           for bpy_idx in gfs_vert_to_bpy_vert.values()]
        out.append(position_deltas)
        
    return out
    
def create_mesh(gfs, bpy_mesh_object, armature, node_id, export_materials, errorlog, log_missing_weights, recalculate_tangents, throw_missing_weight_errors):
    # Extract vertex and polygon data from the bpy struct
    bone_names = {bn.name: i for i, bn in enumerate(gfs.bones)}
    vertices, indices, gfs_vert_to_bpy_vert = extract_vertex_data(bpy_mesh_object, bone_names, errorlog, log_missing_weights, recalculate_tangents, throw_missing_weight_errors)
    
    # Check if any of the mesh data is invalid... we'll accumulate these
    # into an error report for the user.
    # 1) Check for any non-triangular faces
    bad_polys = []
    for pidx, poly in enumerate(bpy_mesh_object.data.polygons):
        if len(poly.vertices) != 3:
            bad_polys.append(pidx)
    if len(bad_polys):
        errorlog.log_error(NonTriangularFacesError(bpy_mesh_object, bad_polys))
    # 2) We already checked for vertices belonging to more than 4 vertex groups
    #    and verts with missing vertex group bones in the data extraction
    
    # Now convert mesh to GFS structs... don't worry if it contains invalid data,
    # we're going to throw an exception at the end of export if any of the meshes
    # were flagged as invalid by the errorlog.
    mesh_props = bpy_mesh_object.data.GFSTOOLS_MeshProperties
    mesh = gfs.add_mesh(node_id, vertices, 
                        bpy_mesh_object.active_material.name if bpy_mesh_object.active_material is not None else None, 
                        [fidx for face in indices for fidx in face], 
                        extract_morphs(bpy_mesh_object, gfs_vert_to_bpy_vert),
                        mesh_props.unknown_0x12, 
                        mesh_props.unknown_float_1 if mesh_props.has_unknown_floats else None,
                        mesh_props.unknown_float_2 if mesh_props.has_unknown_floats else None, 
                        mesh_props.export_bounding_box, 
                        mesh_props.export_bounding_sphere)
    
    # Export flags we can't currently deduce from Blender data...
    # We might be able to represent some of these flags within Blender itself
    # if we can figure out what some of them do.
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
    
    # Finally log the name of the material so we can pass it on to the material
    # exporter in a different function
    if bpy_mesh_object.active_material is not None:
        export_materials.add(bpy_mesh_object.active_material.name)
    
    return mesh

#####################
# PRIVATE FUNCTIONS #
#####################
def extract_vertex_data(mesh_obj, bone_names, errorlog, log_missing_weights, recalculate_tangents, throw_missing_weight_errors):
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
    export_verts, export_faces, gfs_vert_to_bpy_vert = split_verts_by_loop_data(bone_names, mesh_obj, vidx_to_lidxs, lidx_to_fidx, vweight_floor, errorlog, log_missing_weights, recalculate_tangents, throw_missing_weight_errors)
    
    return export_verts, export_faces, gfs_vert_to_bpy_vert

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

def pack_colour(colour):
    # RGBA -> ARGB
    return tuple([max(int(colour[3]*255), 255), 
                  max(int(colour[0]*255), 255), 
                  max(int(colour[1]*255), 255),
                  max(int(colour[2]*255), 255)])

def extract_colours(bpy_mesh, map_name):
    # Blender 3.2+ 
    # vertex_colors is equivalent to color_attributes.new(name=name, type="BYTE_COLOR", domain="CORNER").
    # Original data is just uint8s so this is accurate.
    if hasattr(bpy_mesh, "color_attributes"):
        if map_name not in bpy_mesh.color_attributes:
            return 0
        
        ca = bpy_mesh.color_attributes[map_name]
        if ca.domain == "CORNER":
            return tuple([pack_colour(c.color) for c in ca.data])
        elif ca.domain == "POINT":
            # Copy vertex data to loop data
            return tuple([pack_colour(ca.data[loop.vertex_index].color) for loop in bpy_mesh.loop])
        else:
            return 1
    # Blender 2.81-3.2
    else:
        if map_name not in bpy_mesh.vertex_colors:
            return 0
        vc = bpy_mesh.vertex_colors[map_name]
        return tuple([pack_colour(l.color) for l in vc.data])


def extract_colour_map(bpy_mesh_obj, idx, errorlog):
    map_name = make_color_map_name(0)
    cols = extract_colours(bpy_mesh_obj.data, map_name)
    if cols == 0:
        errorlog.log_warning_message(f"Could not find '{map_name}' on mesh '{bpy_mesh_obj.name}' required by material '{bpy_mesh_obj.active_material.name}' - defaulting to white (1, 1, 1, 1) for each vertex")
        return [(255, 255, 255, 255) for _ in range(len(bpy_mesh_obj.data.loops))]
    elif cols == 1:
        errorlog.log_warning_message(f"Color map '{map_name}' on mesh '{bpy_mesh_obj.name}' required by material '{bpy_mesh_obj.active_material.name}' does not have 'Corner' or 'Vertex' as the map domain - defaulting to white (1, 1, 1, 1) for each vertex")
        return [(255, 255, 255, 255) for _ in range(len(bpy_mesh_obj.data.loops))]
    else:
        return cols
        


def get_tex_idx(nodes, node_name, default_map):
    tex_idx = 0
    uv_map_name = default_map
    
    tex_node = nodes[node_name]
    if tex_node.type != "TEX_IMAGE":
        return tex_idx, uv_map_name
    
    connections = tex_node.inputs["Vector"].links
    if len(connections):
        uv_node = connections[0].from_socket.node
        if uv_node.type == "UVMAP":
            uv_map_name = uv_node.uv_map
            if is_valid_uv_map(uv_map_name):
                proposed_tex_idx = get_uv_idx_from_name(uv_map_name)
                if proposed_tex_idx < 8:
                    tex_idx = proposed_tex_idx
    return tex_idx, uv_map_name


def split_verts_by_loop_data(bone_names, mesh_obj, vidx_to_lidxs, lidx_to_fidx, vweight_floor, errorlog, log_missing_weights, recalculate_tangents, throw_missing_weight_errors):
    mesh = mesh_obj.data
    
    # Figure out what vertex attributes to export 
    if mesh_obj.active_material is not None:
        material = mesh_obj.active_material
        mat_props = material.GFSTOOLS_MaterialProperties
        
        use_normals   = mat_props.requires_normals
        use_tangents  = mat_props.requires_tangents
        use_binormals = mat_props.requires_binormals
        use_color0    = mat_props.requires_color0s
        use_color1    = mat_props.requires_color1s
        
        uv0_map = None
        uv1_map = None
        uv2_map = None
        uv3_map = None
        uv4_map = None
        uv5_map = None
        uv6_map = None
        uv7_map = None
        
        if mesh.uv_layers.active is not None:
            default_map = mesh.uv_layers.active.name
        else:
            default_map = None
        
        # Check what tex indices we need to export
        nodes = material.node_tree.nodes
        for nm in ["Diffuse Texture",
                   "Normal Texture",
                   "Specular Texture",
                   "Reflection Texture",
                   "Highlight Texture",
                   "Glow Texture",
                   "Night Texture",
                   "Detail Texture",
                   "Shadow Texture"]:
            
            if nm in nodes:
                tex_idx, uv_map_name = get_tex_idx(nodes, nm, default_map)
                
                if   tex_idx == 0: uv0_map = uv_map_name
                elif tex_idx == 1: uv1_map = uv_map_name
                elif tex_idx == 2: uv2_map = uv_map_name
                elif tex_idx == 3: uv3_map = uv_map_name
                elif tex_idx == 4: uv4_map = uv_map_name
                elif tex_idx == 5: uv5_map = uv_map_name
                elif tex_idx == 6: uv6_map = uv_map_name
                elif tex_idx == 7: uv7_map = uv_map_name
            
        # Check if we can ID a tex coord to use for tangent calculations
        tangent_uvs = None
        for nm in ["Normal Texture"]: # Add more if other maps might need tangents
            if nm in nodes:
                _, tangent_uvs = get_tex_idx(nodes, nm, None)
        if tangent_uvs is None:
            tangent_uvs = default_map
                
    else:
        tangent_uvs = None
        use_normals = True
        use_tangents = False
        use_binormals = False
        use_color0 = False
        use_color1 = False
        uv0_map = None
        uv1_map = None
        uv2_map = None
        uv3_map = None
        uv4_map = None
        uv5_map = None
        uv6_map = None
        uv7_map = None

    exported_vertices = []
    faces = [{l: mesh.loops[l].vertex_index for l in f.loop_indices} for f in mesh.polygons]
    
    # Create loop data if we need it but it doesn't exist
    if use_normals and tuple(mesh.loops[0].normal) == (0., 0., 0.):
        mesh.calc_normals_split()
    if (use_tangents or use_binormals) and (tuple(mesh.loops[0].tangent) == (0., 0., 0.) or recalculate_tangents):
        if tangent_uvs is None:
            errorlog.log_error_message(f"Material '{mesh_obj.active_material.name}' requires tangents for export, but mesh '{mesh_obj.name}' does not have any UV maps")
        else:
            mesh.calc_tangents(uvmap=tangent_uvs)

    sigfigs = 4
    nloops = len(mesh.loops)

    # Extract normals
    if use_normals:
        normals = [(elem,) for elem in fetch_data(mesh.loops, "normal", sigfigs)]
    else:
        normals = [tuple()]*nloops

    # Extract UVs
    UV_data = [[None for _ in range(nloops)]]*8
    if uv0_map is not None: UV_data[0] = fetch_data(mesh.uv_layers[uv0_map].data, "uv", sigfigs+2)
    if uv1_map is not None: UV_data[1] = fetch_data(mesh.uv_layers[uv1_map].data, "uv", sigfigs+2)
    if uv2_map is not None: UV_data[2] = fetch_data(mesh.uv_layers[uv2_map].data, "uv", sigfigs+2)
    if uv3_map is not None: UV_data[3] = fetch_data(mesh.uv_layers[uv3_map].data, "uv", sigfigs+2)
    if uv4_map is not None: UV_data[4] = fetch_data(mesh.uv_layers[uv4_map].data, "uv", sigfigs+2)
    if uv5_map is not None: UV_data[5] = fetch_data(mesh.uv_layers[uv5_map].data, "uv", sigfigs+2)
    if uv6_map is not None: UV_data[6] = fetch_data(mesh.uv_layers[uv6_map].data, "uv", sigfigs+2)
    if uv7_map is not None: UV_data[7] = fetch_data(mesh.uv_layers[uv7_map].data, "uv", sigfigs+2)
    
    if len(UV_data):
        UV_data = [tuple(elems) for elems in zip(*UV_data)]
    else:
        UV_data = [tuple()]*nloops

    # Extract colours
    col_data = [[None for _ in range(nloops)]]*2
    if use_color0: col_data[0] = extract_colour_map(mesh_obj, 0, errorlog)
    if use_color1: col_data[1] = extract_colour_map(mesh_obj, 1, errorlog)
    
    if len(col_data):
        col_data = [tuple(elems) for elems in zip(*col_data)]
    else:
        col_data = [tuple()]*nloops

    # Extract tangents
    if use_tangents:
        tangents = [(elem,) for elem in fetch_tangent(mesh.loops, sigfigs)]
    else:
        tangents = [tuple()]*nloops

    # Calculate binormals
    if use_binormals:
        bitangents = [(tuple(round_to_sigfigs(l.bitangent_sign * np.cross(normal[0], tangent[0]), sigfigs)),) for normal, tangent, l in zip(normals, tangents, mesh.loops)]
    else:
        bitangents = [tuple()]*nloops

    # Make loop -> unique value lookup maps
    loop_idx_to_key = [key for key in (zip(normals, UV_data, col_data, tangents, bitangents))]
    unique_val_map = {key: i for i, key in enumerate(list(set(loop_idx_to_key)))}
    loop_idx_to_unique_key = {i: unique_val_map[key] for i, key in enumerate(loop_idx_to_key)}

    gfs_vert_to_bpy_vert = {}
    too_many_indices_verts = []
    missing_weight_verts = []
    unrigged_verts = []
    missing_bone_names = set()
    vertex_group_idx_to_name_map = {g.index: g.name for g in mesh_obj.vertex_groups}
    for vert_idx, linked_loops in vidx_to_lidxs.items():
        vertex = mesh.vertices[vert_idx]
        unique_ids = {i: [] for i in list(set(loop_idx_to_unique_key[ll] for ll in linked_loops))}
        for ll in linked_loops:
            unique_ids[loop_idx_to_unique_key[ll]].append(ll)
        unique_values = [(loop_idx_to_key[lids[0]], lids) for id_, lids in unique_ids.items()]

        # Extract bone weights and check for any errors with them
        group_indices = [grp for grp in vertex.groups if grp.weight > vweight_floor]
        group_bone_ids = [0, 0, 0, 0]
        group_weights  = [0, 0, 0, 0]
        grp_idx = 0
        has_missing_weights = False
        if len(group_indices) > 4:
            too_many_indices_verts.append(vert_idx)
            continue
        elif len(group_indices) == 0:
            unrigged_verts.append(vert_idx)
        for grp in group_indices:
            bone_name = vertex_group_idx_to_name_map[grp.group]
            grp_bone_idx = bone_names.get(bone_name)
            if grp_bone_idx is None:
                has_missing_weights = True
                missing_bone_names.add(bone_name)
            else:
                group_bone_ids[grp_idx] = grp_bone_idx
                group_weights[grp_idx] = grp.weight
                grp_idx += 1
        
        if has_missing_weights:
            missing_weight_verts.append(vert_idx)
            
        # Normalise the group weights
        total_weight = sum(group_weights)
        if total_weight > 0.:
            group_weights = [wght / total_weight for wght in group_weights]
        
        # Now split the verts by their loop data
        for unique_value, loops_with_this_value in unique_values:
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
            for attr_idx, value in zip([VertexAttributes.COLOR1,
                                       VertexAttributes.COLOR2], unique_value[2]):
                vb[attr_idx] = value
            if len(unique_value[3]): vb.tangent  = unique_value[3][0]
            if len(unique_value[4]): vb.binormal = unique_value[4][0]
            if len(group_indices):
                vb.indices = group_bone_ids
                vb.weights = group_weights

            n_verts = len(exported_vertices)
            gfs_vert_to_bpy_vert[len(exported_vertices)] = vert_idx
            exported_vertices.append(vb)

            for l in loops_with_this_value:
                face_idx = lidx_to_fidx[l]
                faces[face_idx][l] = n_verts

    faces = [list(face_verts.values()) for face_verts in faces]
    
    for v in exported_vertices:
        if v.indices is None:
            v.indices = [0., 0., 0., 0.]
            v.weights = [0., 0., 0., 0.]
    
    # Log any errors that were encountered
    if log_missing_weights and len(missing_weight_verts):
        errorlog.log_error(MissingVertexGroupsError(mesh_obj, missing_weight_verts, missing_bone_names))
    if len(too_many_indices_verts):
        errorlog.log_error(TooManyIndicesError(mesh_obj, too_many_indices_verts))
    if 0 < len(unrigged_verts) < len(exported_vertices):
        if throw_missing_weight_errors:
            errorlog.log_error(PartiallyUnriggedMeshError(mesh_obj, unrigged_verts))
        else:
            errorlog.log_warning_message(f"Mesh '{mesh_obj.name}' is rigged, but some vertices are not rigged to any vertex groups. Use the 'Throw Errors for Unrigged Vertices' option on export to see which vertices have this issue.")
        
    return exported_vertices, faces, gfs_vert_to_bpy_vert


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
    return [tuple(round_to_sigfigs(datum, sigfigs)) for datum in zip(*(iter(data),) * dsize)]
