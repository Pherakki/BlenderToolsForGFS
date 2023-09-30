from collections import defaultdict

import bpy
from mathutils import Quaternion, Vector, Matrix
import numpy as np

from ...Globals import GFS_MODEL_TRANSFORMS
from ...Utils.Maths import convert_Zup_to_Yup, convert_Yup_to_Zup

from ...modelUtilsTest.Context.ActiveObject import safe_active_object_switch, get_active_obj, set_active_obj, set_mode
from ...modelUtilsTest.Misc.ID.UniqueName import new_unique_name
from .Errors import MultipleMaterialsError
from .Errors import NonTriangularFacesError
from .Errors import TooManyVerticesError
from .Vertices import extract_vertices


VERTEX_LIMIT = TooManyVerticesError.vtx_limit
COMBINED_NODE_NAME = "mesh"


def export_mesh_data(gfs, armature, bpy_to_gfs_node, bind_pose_matrices, errorlog, export_policies):
    too_many_vertices_policy      = export_policies.too_many_vertices_policy
    multiple_materials_policy     = export_policies.multiple_materials_policy
    combine_new_mesh_nodes        = export_policies.combine_new_mesh_nodes
    
    # Find meshes
    meshes = armature.GFSTOOLS_ObjectProperties.get_model_meshes()
    material_names = set()
    
    bad_meshes = []
    multiple_materials_meshes = []
    for bpy_mesh_object in meshes:
        oprops = bpy_mesh_object.GFSTOOLS_ObjectProperties
        
        if not oprops.is_valid_mesh():
            errorlog.log_warning_message(f"THIS IS A BUG: An invalid mesh '{bpy_mesh_object.name}' made its way to the exporter when it should have been skipped. This mesh has NOT been exported and your export is otherwise unaffected, but this message should have never appeared. Please create an Issue on the GitHub page with FULL reproduction instructions and any required files to reproduce this error message.")
        
        existing_meshes = set(o.name for o in bpy.data.objects)
        material_index = validate_mesh_materials(bpy_mesh_object, multiple_materials_meshes, export_policies)
        
        # Get node ID
        if oprops.requires_new_node():
            node_id = len(gfs.bones)
        else:
            node_name = oprops.get_node_name()
            node_id = bpy_to_gfs_node[node_name]

        # Convert bpy meshes -> gfs meshes
        gfs_meshes = []
        gfs_meshes.append(create_mesh(gfs, bpy_mesh_object, armature, node_id, material_names, material_index, errorlog, export_policies))
        
        if len(gfs_meshes[-1].vertices) > VERTEX_LIMIT:
            bad_meshes.append(bpy_mesh_object)

        # Also do any meshes generated by the material-split policy
        # These will have identical properties to the original mesh
        new_meshes = set(o.name for o in bpy.data.objects) - existing_meshes
        for new_mesh_object in sorted(new_meshes):
            gfs_meshes.append(create_mesh(gfs, new_mesh_object, armature, node_id, material_names, 0, errorlog, export_policies))

        # Yeet the vertex weights if unrigged
        if oprops.is_unrigged():
            for gm in gfs_meshes:
                for v in gm.vertices:
                    v.indices = None
                    v.weights = None
        
        # Handle the new vs. attached node behaviours
        if oprops.requires_new_node():
            export_name = COMBINED_NODE_NAME if combine_new_mesh_nodes else bpy_mesh_object.name
            if oprops.get_rigged_type() == oprops.RIGGED_NEW_NODE_INVALID:
                errorlog.log_warning_message(f"Mesh '{bpy_mesh_object.name}' is associated with the bone '{oprops.node}', but this bone does not exist in the armature '{armature.name}'. A new bone '{export_name}' has been generated in the exported GFS file to associate with the mesh instead.")
            
            if combine_new_mesh_nodes:
                for gfs_mesh in gfs_meshes:
                    bake_mesh_transform(gfs_mesh, bpy_mesh_object.matrix_local)
                continue
            # Create new node with the mesh transform
            create_mesh_node(gfs, export_name, armature, bpy_mesh_object.matrix_local, bpy_mesh_object.data.GFSTOOLS_NodeProperties)
        else:
            # Transform the vertex data by the mesh/node discrepancy
            bpm = bind_pose_matrices[node_id]
            relative_transform = convert_Yup_to_Zup(bpm).inverted() @ bpy_mesh_object.matrix_local
            
            for gfs_mesh in gfs_meshes:
                bake_mesh_transform(gfs_mesh, relative_transform)
    
    if combine_new_mesh_nodes:
        create_mesh_node(gfs, COMBINED_NODE_NAME, armature, Matrix.Identity(4))
    
    if len(bad_meshes):
        if too_many_vertices_policy == "IGNORE":
            pass
        elif too_many_vertices_policy == "WARN":
            errorlog.log_warning_message(f"{len(bad_meshes)} meshes need to be split into more than {VERTEX_LIMIT} vertices for export. This might cause issues and it is recommended to split these meshes into smaller meshes. The affected meshes are {', '.join([m.name for m in bad_meshes])}")
        elif too_many_vertices_policy == "ERROR":
            errorlog.log_error(TooManyVerticesError(bad_meshes))
        else:
            raise NotImplementedError(f"CRITICAL INTERNAL ERROR: TOO_MANY_VERTICES_POLICY '{too_many_vertices_policy}' NOT DEFINED")
    
    if len(multiple_materials_meshes):
        if multiple_materials_policy == "WARN":
            newline = '\n'
            errorlog.log_warning_message(f"The following meshes have more than one material. They have been exported with whichever material is used by the most faces per mesh.\n{newline.join([o.name for o in multiple_materials_meshes])}\nYou can change this behaviour from the Export menu and in the Addon Preferences")
        elif multiple_materials_policy == "ERROR":    
            errorlog.log_error(MultipleMaterialsError(multiple_materials_meshes))
        elif multiple_materials_policy == "AUTOSPLIT_DESTRUCTIVE":
            newline = '\n'
            errorlog.log_warning_message(f"The following meshes contained more than one material and were split into multiple meshes within Blender:\n{newline.join([o.name for o in multiple_materials_meshes])}\nYou can change this behaviour from the Export menu and in the Addon Preferences")
        else:
            raise NotImplementedError(f"CRITICAL INTERNAL ERROR: MULTIPLE_MATERIALS_POLICY '{multiple_materials_policy}' NOT DEFINED")
    
    aprops     = armature.data.GFSTOOLS_ModelProperties
    boxprops = aprops.bounding_box
    if boxprops.export_policy == "MANUAL":
        gfs.bounding_box_max_dims = np.array(boxprops.max_dims) @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3.copy()
        gfs.bounding_box_min_dims = np.array(boxprops.min_dims) @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3.copy()
    elif boxprops.export_policy == "AUTO":
        gfs.bounding_box_min_dims, gfs.bounding_box_max_dims, _ = make_bounding_box(gfs)
        
    sphprops = aprops.bounding_sphere
    if sphprops.export_policy == "MANUAL":
        gfs.bounding_sphere_centre = np.array(sphprops.center) @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3.copy()
        gfs.bounding_sphere_radius = sphprops.radius
    elif sphprops.export_policy == "AUTO":
        b_min, b_max, centre = make_bounding_box(gfs)
        
        gfs.bounding_sphere_centre = centre
        gfs.bounding_sphere_radius = max([np.linalg.norm(centre - b_min), np.linalg.norm(centre - b_max)])

    return sorted(material_names)



@safe_active_object_switch
def triangulate_mesh(bpy_mesh_object):
    set_active_obj(bpy_mesh_object)
    set_mode("EDIT")
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris()
    set_mode("OBJECT")


def make_bounding_box(gfs):
    # Should call an internal method here...
    verts = []
    matrices = np.empty((len(gfs.bones), 4, 4))
    for i, bone in enumerate(gfs.bones):
        matrix = np.eye(4)
        q = bone.rotation
        matrix[:3, :3] = np.array(Quaternion([q[3], q[0], q[1], q[2]]).to_matrix())
        matrix = matrix @ np.diag([*bone.scale, 1.])
        matrix[:3, 3] = bone.position
        
        if bone.parent_idx > -1:
            matrices[i] = matrices[bone.parent_idx] @ matrix
        else:
            matrices[i] = matrix
            
        verts.append(matrices[i][:3, 3])
    
    mesh_verts = []
    for mesh in gfs.meshes:
        if not mesh.keep_bounding_box:
            continue
        matrix = matrices[mesh.node]
        max_dims = np.max([v.position for v in mesh.vertices], axis=0)
        min_dims = np.min([v.position for v in mesh.vertices], axis=0)
        
        mesh_verts.append((matrix @ np.array([*max_dims, 1.]))[:3])
        mesh_verts.append((matrix @ np.array([*min_dims, 1.]))[:3])
        
    max_dims = np.max([*verts, *mesh_verts], axis=0)
    min_dims = np.min([*verts, *mesh_verts], axis=0)

    return min_dims, max_dims, np.mean(mesh_verts, axis=0)


def validate_mesh_materials(bpy_mesh_object, multiple_materials_meshes, export_policies):
    multiple_materials_policy = export_policies.multiple_materials_policy
    
    bpy_mesh = bpy_mesh_object.data
    
    index_counts = defaultdict(lambda: 0)
    for poly in bpy_mesh.polygons:
        index_counts[poly.material_index] += 1
    
    if len(index_counts) > 1:
        multiple_materials_meshes.append(bpy_mesh_object)
        
        if multiple_materials_policy == "AUTOSPLIT_DESTRUCTIVE":
            old_obj  = get_active_obj()
            old_mode = bpy_mesh_object.mode
            set_active_obj(bpy_mesh_object)
            
            try:
                # Split the mesh
                set_mode("EDIT")
                bpy.ops.mesh.separate(type='MATERIAL')
                set_mode("OBJECT")
                return 0
            finally:
                set_mode(old_mode)
                set_active_obj(old_obj)
        else:
            # Return material index with most polygons
            return max(index_counts, key=index_counts.get)
    return 0


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


def create_mesh(gfs, bpy_mesh_object, armature, node_id, export_materials, material_index, errorlog, export_policies):
    triangulate_mesh_policy = export_policies.triangulate_mesh_policy

    # Check if any of the mesh data is invalid... we'll accumulate these
    # into an error report for the user.
    # 1) Check for any non-triangular faces
    bad_polys = []
    for pidx, poly in enumerate(bpy_mesh_object.data.polygons):
        if len(poly.vertices) != 3:
            bad_polys.append(pidx)
    if len(bad_polys):
        if triangulate_mesh_policy == "TRIANGULATE_DESTRUCTIVE":
            triangulate_mesh(bpy_mesh_object)
            errorlog.log_warning_message(f"{len(bad_polys)} non-triangular faces were triangulated on mesh '{bpy_mesh_object.name}'. This has affected the mesh present in Blender")
        elif triangulate_mesh_policy == "ERROR":
            errorlog.log_error(NonTriangularFacesError(bpy_mesh_object, bad_polys))
        else:
            raise Exception(f"CRITICAL INTERNAL ERROR: UNKNOWN TRIANGULATE_MESH_POLICY '{triangulate_mesh_policy}'")
    
    # Extract vertex and polygon data from the bpy struct
    bone_names = {bn.name: i for i, bn in enumerate(gfs.bones)}
    
    mesh_buffers = extract_vertices(bpy_mesh_object, bone_names, errorlog, export_policies)
    vertices = mesh_buffers.vertices
    indices = mesh_buffers.indices
    gfs_vert_to_bpy_vert = mesh_buffers.vbo_vert_to_bpy_vert_map
    
    # 2) We already checked for vertices belonging to more than 4 vertex groups
    #    and verts with missing vertex group bones in the data extraction
    
    # Now convert mesh to GFS structs... don't worry if it contains invalid data,
    # we're going to throw an exception at the end of export if any of the meshes
    # were flagged as invalid by the errorlog.
    material_name = bpy_mesh_object.data.materials[material_index].name if len(bpy_mesh_object.data.materials) else None
    mesh_props = bpy_mesh_object.data.GFSTOOLS_MeshProperties
    bbox = mesh_props.bounding_box
    bsph = mesh_props.bounding_sphere
    gfs_mesh = gfs.add_mesh(node_id, vertices, 
                            material_name,
                            [fidx for face in indices for fidx in face], 
                            extract_morphs(bpy_mesh_object, gfs_vert_to_bpy_vert),
                            mesh_props.unknown_0x12, 
                            mesh_props.unknown_float_1 if mesh_props.has_unknown_floats else None,
                            mesh_props.unknown_float_2 if mesh_props.has_unknown_floats else None, 
                            bbox.export_policy != "NONE" if len(vertices) else False, 
                            bsph.export_policy != "NONE" if len(vertices) else False)
    
    if bbox.export_policy == "MANUAL":
        obox = gfs_mesh.overrides.bounding_box
        obox.enabled = True
        obox.min_dims = np.array(bbox.min_dims)# @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3.copy()
        obox.max_dims = np.array(bbox.max_dims)# @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3.copy()
    
    if bsph.export_policy == "MANUAL":
        osph = gfs_mesh.overrides.bounding_sphere
        osph.enabled = True
        osph.center = np.array(bsph.center)# @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3.copy()
        osph.radius = np.array(bsph.radius)# @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3.copy()
    
    
    # Export flags we can't currently deduce from Blender data...
    # We might be able to represent some of these flags within Blender itself
    # if we can figure out what some of them do.
    gfs_mesh.flag_5 = mesh_props.flag_5
    gfs_mesh.flag_7 = mesh_props.flag_7
    gfs_mesh.flag_8 = mesh_props.flag_8
    gfs_mesh.flag_9 = mesh_props.flag_9
    gfs_mesh.flag_10 = mesh_props.flag_10
    gfs_mesh.flag_11 = mesh_props.flag_11
    gfs_mesh.flag_13 = mesh_props.flag_13
    gfs_mesh.flag_14 = mesh_props.flag_14
    gfs_mesh.flag_15 = mesh_props.flag_15
    gfs_mesh.flag_16 = mesh_props.flag_16
    gfs_mesh.flag_17 = mesh_props.flag_17
    gfs_mesh.flag_18 = mesh_props.flag_18
    gfs_mesh.flag_19 = mesh_props.flag_19
    gfs_mesh.flag_20 = mesh_props.flag_20
    gfs_mesh.flag_21 = mesh_props.flag_21
    gfs_mesh.flag_22 = mesh_props.flag_22
    gfs_mesh.flag_23 = mesh_props.flag_23
    gfs_mesh.flag_24 = mesh_props.flag_24
    gfs_mesh.flag_25 = mesh_props.flag_25
    gfs_mesh.flag_26 = mesh_props.flag_26
    gfs_mesh.flag_27 = mesh_props.flag_27
    gfs_mesh.flag_28 = mesh_props.flag_28
    gfs_mesh.flag_29 = mesh_props.flag_29
    gfs_mesh.flag_30 = mesh_props.flag_30
    gfs_mesh.flag_31 = mesh_props.flag_31
    
    # Finally log the name of the material so we can pass it on to the material
    # exporter in a different function
    if material_name is not None:
        export_materials.add(material_name)
    
    return gfs_mesh

def create_mesh_node(gfs, name, armature, bind_matrix, node_props=None):
    parent_idx = 0
    bind_pose_matrix = convert_Zup_to_Yup(bind_matrix)
    parent_relative_bind_pose_matrix = armature.matrix_local.inverted() @ bind_pose_matrix    
        
    # Now create the transforms for the node
    pos, rot, scl = parent_relative_bind_pose_matrix.decompose()
    
    # Other crap, create node
    bpm = [*bind_pose_matrix[0], *bind_pose_matrix[1], *bind_pose_matrix[2]]
    uname = new_unique_name(name, set([b.name for b in gfs.bones]))
    gfs_node = gfs.add_node(parent_idx, uname, [pos.x, pos.y, pos.z], [rot.x, rot.y, rot.z, rot.w], [scl.x, scl.y, scl.z], getattr(node_props, "unknown_float", 1.0), bpm)        
    for prop in getattr(node_props, "properties", []):
        gfs_node.add_property(*prop.extract_data(prop))


def bake_mesh_transform(gfs_mesh, transform):
    vs = gfs_mesh.vertices
    # Position
    if vs[0].position is not None:
        for v in vs: v.position = (transform @ Vector([*v.position, 1.]))[:3]
    # Normal
    if vs[0].normal is not None:
        for v in vs: v.normal   = (transform @ Vector([*v.normal,   0.]))[:3]
    # Tangent
    if vs[0].tangent is not None:
        for v in vs: v.tangent  = (transform @ Vector([*v.tangent,  0.]))[:3]
    # Binormal
    if vs[0].binormal is not None:
        for v in vs: v.binormal = (transform @ Vector([*v.binormal, 0.]))[:3]