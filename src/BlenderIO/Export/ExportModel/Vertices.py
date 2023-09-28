from ....FileFormats.GFS.SubComponents.CommonStructures.SceneNode.MeshBinary import VertexBinary
from ...modelUtilsTest.Mesh.Export.ExtractMeshBuffers import bpy_mesh_to_VBO_IBO
from ...modelUtilsTest.Mesh.Export.Attributes import get_normals
from ...modelUtilsTest.Mesh.Export.Attributes import get_tangents
from ...modelUtilsTest.Mesh.Export.Attributes import get_binormals
from ...modelUtilsTest.Mesh.Export.Attributes import get_uvs
from ...modelUtilsTest.Mesh.Export.Attributes import get_colors
from ...Utils.UVMapManagement import make_uv_map_name, is_valid_uv_map, get_uv_idx_from_name
from ...Utils.UVMapManagement import make_color_map_name
from .Errors import MissingUVMapsError
from .Errors import MissingVertexGroupsError
from .Errors import PartiallyUnriggedMeshError
from .Errors import TooManyIndicesError


def extract_vertices(bpy_mesh_obj, bone_names, errorlog, export_policies):
    bpy_mesh     = bpy_mesh_obj.data
    bpy_material = bpy_mesh_obj.active_material # Revist this...
    
    missing_uv_maps_policy = export_policies.missing_uv_maps_policy
    recalculate_tangents   = export_policies.recalculate_tangents
    
    if bpy_material is None:
        return [], []
    
    used_attributes = get_used_attributes(bpy_mesh, bpy_material)
    
    # Deal with any zero vectors
    zero_vec = (0., 0., 0.)
    loop_normals = [l.normal for l in bpy_mesh.loops]
    lnorms_zero = [tuple(normal) == zero_vec for normal in loop_normals]
    if any(lnorms_zero):
        if not bpy_mesh.has_custom_normals:
            bpy_mesh.create_normals_split()
        bpy_mesh.calc_normals_split()
        res = []
        for j, iszero in enumerate(lnorms_zero):
            res.append(bpy_mesh.loops[j].normal if iszero else loop_normals[j])
        bpy_mesh.normals_split_custom_set(res)
    
    # Create loop data if we need it but it doesn't exist
    if used_attributes.requires_normals and tuple(bpy_mesh.loops[0].normal) == (0., 0., 0.):
        bpy_mesh.calc_normals_split()
    if (used_attributes.requires_tangents or used_attributes.requires_binormals) and (tuple(bpy_mesh.loops[0].tangent) == (0., 0., 0.) or recalculate_tangents):
        if used_attributes.tangent_uvs is None:
            errorlog.log_error_message(f"Material '{bpy_material.name}' requires tangents for export, but mesh '{bpy_mesh_obj.name}' does not have any UV maps")
        else:
            bpy_mesh.calc_tangents(uvmap=used_attributes.tangent_uvs)
    
    # Extract data
    loop_data = [
        get_normals(bpy_mesh_obj,   used_attributes.requires_normals,   4),
        get_tangents (bpy_mesh_obj, used_attributes.requires_tangents,  4),
        get_binormals(bpy_mesh_obj, used_attributes.requires_binormals, 4),
        fetch_uv(bpy_mesh_obj,      used_attributes.requires_uv0, make_uv_map_name(0), 6, errorlog, missing_uv_maps_policy),
        fetch_uv(bpy_mesh_obj,      used_attributes.requires_uv1, make_uv_map_name(1), 6, errorlog, missing_uv_maps_policy),
        fetch_uv(bpy_mesh_obj,      used_attributes.requires_uv2, make_uv_map_name(2), 6, errorlog, missing_uv_maps_policy),
        fetch_uv(bpy_mesh_obj,      used_attributes.requires_uv3, make_uv_map_name(3), 6, errorlog, missing_uv_maps_policy),
        fetch_uv(bpy_mesh_obj,      used_attributes.requires_uv4, make_uv_map_name(4), 6, errorlog, missing_uv_maps_policy),
        fetch_uv(bpy_mesh_obj,      used_attributes.requires_uv5, make_uv_map_name(5), 6, errorlog, missing_uv_maps_policy),
        fetch_uv(bpy_mesh_obj,      used_attributes.requires_uv6, make_uv_map_name(6), 6, errorlog, missing_uv_maps_policy),
        fetch_uv(bpy_mesh_obj,      used_attributes.requires_uv7, make_uv_map_name(7), 6, errorlog, missing_uv_maps_policy),
        get_colors(bpy_mesh_obj,    used_attributes.requires_color0, make_color_map_name(0), "BYTE", errorlog, transform=lambda x,l: [x[3], x[0], x[1], x[2]]),
        get_colors(bpy_mesh_obj,    used_attributes.requires_color1, make_color_map_name(1), "BYTE", errorlog, transform=lambda x,l: [x[3], x[0], x[1], x[2]]),    
    ]
    
    # Convert to VAO/IBO
    vertex_group_idx_to_name_map = {g.index: g.name for g in bpy_mesh_obj.vertex_groups}
    vertex_getter = GFSVertexGetter(bone_names, vertex_group_idx_to_name_map, export_policies, errorlog)
    mesh_buffers = bpy_mesh_to_VBO_IBO(bpy_mesh, vertex_getter, loop_data, construct_vertex)
    vertex_getter.log_errors(bpy_mesh_obj, mesh_buffers.vertices)
    
    for v in mesh_buffers.vertices:
        if v.indices is None:
            v.indices = [0., 0., 0., 0.]
            v.weights = [0., 0., 0., 0.]
    
    return mesh_buffers


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


class UsedAttributes:
    __slots__ = ("requires_normals", "requires_tangents", "requires_binormals",
                 "uv0_map", "uv1_map", "uv2_map", "uv3_map",
                 "uv4_map", "uv5_map", "uv6_map", "uv7_map",
                 "requires_color0", "requires_color1",
                 "tangent_uvs")
    def __init__(self):
        self.requires_normals   = True
        self.requires_tangents  = False
        self.requires_binormals = False
        self.uv0_map = None
        self.uv1_map = None
        self.uv2_map = None
        self.uv3_map = None
        self.uv4_map = None
        self.uv5_map = None
        self.uv6_map = None
        self.uv7_map = None
        self.requires_color0 = False
        self.requires_color1 = False
        self.tangent_uvs = None
        
    requires_uv0 = property(lambda self: self.uv0_map is not None)
    requires_uv1 = property(lambda self: self.uv1_map is not None)
    requires_uv2 = property(lambda self: self.uv2_map is not None)
    requires_uv3 = property(lambda self: self.uv3_map is not None)
    requires_uv4 = property(lambda self: self.uv4_map is not None)
    requires_uv5 = property(lambda self: self.uv5_map is not None)
    requires_uv6 = property(lambda self: self.uv6_map is not None)
    requires_uv7 = property(lambda self: self.uv7_map is not None)


def get_used_attributes(bpy_mesh, bpy_material):
    used_attributes = UsedAttributes()
    
    if bpy_material is not None:
        mat_props = bpy_material.GFSTOOLS_MaterialProperties
        
        used_attributes.requires_normals   = mat_props.requires_normals
        used_attributes.requires_tangents  = mat_props.requires_tangents
        used_attributes.requires_binormals = mat_props.requires_binormals
        used_attributes.requires_color0    = mat_props.requires_color0s
        used_attributes.requires_color1    = mat_props.requires_color1s
        
        default_map = None
        if bpy_mesh.uv_layers.active is not None: 
            default_map = bpy_mesh.uv_layers.active.name
        
        # Check what tex indices we need to export
        nodes = bpy_material.node_tree.nodes
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
                
                if   tex_idx == 0: used_attributes.uv0_map = uv_map_name
                elif tex_idx == 1: used_attributes.uv1_map = uv_map_name
                elif tex_idx == 2: used_attributes.uv2_map = uv_map_name
                elif tex_idx == 3: used_attributes.uv3_map = uv_map_name
                elif tex_idx == 4: used_attributes.uv4_map = uv_map_name
                elif tex_idx == 5: used_attributes.uv5_map = uv_map_name
                elif tex_idx == 6: used_attributes.uv6_map = uv_map_name
                elif tex_idx == 7: used_attributes.uv7_map = uv_map_name
            
        # Check if we can ID a tex coord to use for tangent calculations
        tangent_uvs = None
        for nm in ["Normal Texture"]: # Add more if other maps might need tangents
            if nm in nodes:
                _, tangent_uvs = get_tex_idx(nodes, nm, None)
        if tangent_uvs is None:
            tangent_uvs = default_map
        used_attributes.tangent_uvs = tangent_uvs
            
    return used_attributes


def fetch_uv(bpy_mesh_obj, requires_uv0, map_name, sigfigs, errorlog, missing_uv_maps_policy):
    bpy_mesh = bpy_mesh_obj.data
    
    if not (map_name in bpy_mesh.uv_layers or not requires_uv0):
        if missing_uv_maps_policy == "WARN":
            errorlog.log_warning_message(f"Mesh '{bpy_mesh_obj.name}' uses a material that requires UV map '{map_name}', but the mesh does not contain this map. A blank UV map has been generated")
        elif missing_uv_maps_policy == "ERROR":
            errorlog.log_error(MissingUVMapsError(bpy_mesh_obj, map_name))
        else:
            raise NotImplementedError(f"CRITICAL INTERNAL ERROR: MISSING_UV_MAP_POLICY '{missing_uv_maps_policy}' NOT DEFINED")
        errorlog = None
        
    return get_uvs(bpy_mesh_obj, requires_uv0, map_name, sigfigs, errorlog)


def construct_vertex(vertex_data, loop_data):
    pos, skin_indices, skin_weights = vertex_data
    
    loop_data = iter(loop_data)
    
    vb = VertexBinary()
    vb.position = pos
    vb.normal    = next(loop_data)
    vb.tangent   = next(loop_data)
    vb.binormal  = next(loop_data)
    vb.texcoord0 = next(loop_data)
    vb.texcoord1 = next(loop_data)
    vb.texcoord2 = next(loop_data)
    vb.texcoord3 = next(loop_data)
    vb.texcoord4 = next(loop_data)
    vb.texcoord5 = next(loop_data)
    vb.texcoord7 = next(loop_data)
    vb.color1    = next(loop_data)
    vb.color2    = next(loop_data)
    
    vb.indices = skin_indices
    vb.weights = skin_weights
    
    return vb

def group_sort_key(g):
    return g.weight


class GFSVertexGetter:
    def __init__(self, bone_names, vertex_group_idx_to_name_map, export_policies, errorlog):
        # Vertex group data
        self.bone_names                   = bone_names
        self.vertex_group_idx_to_name_map = vertex_group_idx_to_name_map
        
        # Error-handling policies
        self.log_missing_weights           = not export_policies.strip_missing_vertex_groups
        self.too_many_vertex_groups_policy = export_policies.too_many_vertex_groups_policy
        self.throw_missing_weight_errors   = export_policies.throw_missing_weight_errors
        
        # Error-tracking variables
        self.errorlog = errorlog
        self.missing_bone_names     = []
        self.missing_weight_verts   = []
        self.too_many_indices_verts = []
        self.unrigged_verts         = []
    
    def __call__(self, vert_idx, vertex):
        # Extract bone weights and check for any errors with them
        group_indices = [grp for grp in vertex.groups]
        group_bone_ids = [0, 0, 0, 0]
        group_weights  = [0, 0, 0, 0]
        
        has_missing_weights = False
        if len(group_indices) > 4:
            self.too_many_indices_verts.append(vert_idx)
        elif len(group_indices) == 0:
            self.unrigged_verts.append(vert_idx)
        
        group_indices = list(reversed(sorted(group_indices, key=group_sort_key)))[:4]
        
        for grp_idx, grp in enumerate(group_indices):
            bone_name    = self.vertex_group_idx_to_name_map[grp.group]
            grp_bone_idx = self.bone_names.get(bone_name)
            
            if grp_bone_idx is None:
                has_missing_weights = True
                self.missing_bone_names.add(bone_name)
            else:
                group_bone_ids[grp_idx] = grp_bone_idx
                group_weights[grp_idx] = grp.weight
        
        if has_missing_weights:
            self.missing_weight_verts.append(vert_idx)
            
        # Normalise the group weights
        total_weight = sum(group_weights)
        if total_weight > 0.:
            group_weights = [weight / total_weight for weight in group_weights]
            
        return vertex.co, group_bone_ids, group_weights

    def log_errors(self, bpy_mesh_obj, vertices):
        # Log any errors that were encountered
        if self.log_missing_weights and len(self.missing_weight_verts):
            self.errorlog.log_error(MissingVertexGroupsError(bpy_mesh_obj, self.missing_weight_verts, self.missing_bone_names))
        if len(self.too_many_indices_verts):
            if self.too_many_vertex_groups_policy == "WARN":
                self.errorlog.log_warning_message(f"{len(self.too_many_indices_verts)} vertices on mesh '{bpy_mesh_obj.name}' had too many vertex groups. The least influential groups were removed. Change the export policy to 'Throw Error' if you want to see which vertices have this problem instead.")
            elif self.too_many_vertex_groups_policy == "ERROR":
                self.errorlog.log_error(TooManyIndicesError(bpy_mesh_obj, self.too_many_indices_verts))
            else:
                raise NotImplementedError(f"CRITICAL INTERNAL ERROR: UNKNOWN TOO_MANY_VERTEX_GROUPS_POLICY '{self.too_many_vertex_groups_policy}'")
        if 0 < len(self.unrigged_verts) < len(vertices):
            if self.throw_missing_weight_errors:
                self.errorlog.log_error(PartiallyUnriggedMeshError(bpy_mesh_obj, self.unrigged_verts))
            else:
                self.errorlog.log_warning_message(f"Mesh '{bpy_mesh_obj.name}' is rigged, but some vertices are not rigged to any vertex groups. Use the 'Throw Errors for Unrigged Vertices' option on export to see which vertices have this issue.")
