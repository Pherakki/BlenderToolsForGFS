import bpy
from mathutils import Matrix, Vector, Quaternion
import numpy as np

from ...FileFormats.GFS import GFSBinary
from ...FileFormats.GFS.SubComponents.CommonStructures.SceneNode import NodeInterface
from ..Globals import GFS_MODEL_TRANSFORMS
from ..modelUtilsTest.API.Version import bpy_at_least
from ..modelUtilsTest.Mesh.Import.MergeVertices import create_merged_mesh
from ..modelUtilsTest.Mesh.Import.LoopImport    import create_loop_normals
from ..modelUtilsTest.Mesh.Import.LoopImport    import create_uv_map
from ..modelUtilsTest.Mesh.Import.LoopImport    import create_color_map
from ..Utils.Maths import MayaBoneToBlenderBone, convert_Yup_to_Zup, decomposableToTRS
from ..Utils.Object import lock_obj_transforms
from ..Utils.UVMapManagement import make_uv_map_name
from ..Utils.UVMapManagement import make_color_map_name
from .Utils.BoneConstruction import construct_bone, resize_bone_length
from .ImportProperties import import_properties



def decode_obj_name(obj_name, store_bytestring_on_obj, encoding="utf8"):
    try:
        return obj_name.string.decode(encoding, errors="replace")
    except UnicodeDecodeError:
        store_bytestring_on_obj(obj_name.string)
        return obj_name.string.decode(encoding, errors="replace")


class VertexAttributeTracker:
    __slots__ = ("normals", "tangents", "binormals", "color0s", "color1s")
    
    def __init__(self):
        self.normals   = []
        self.tangents  = []
        self.binormals = []
        self.color0s   = []
        self.color1s   = []


def build_bones_from_bind_pose(gfs, main_armature, bones_to_ignore):
    skewed_bpm_nodes = []
    gfs_to_bpy_bone_map = {}
    bpy_bone_counter = 0
    
    bpy_nodes       = [None]*len(gfs.bones)
    bone_transforms = [None]*len(gfs.bones)
    bone_rest_transforms = [None]*len(gfs.bones)
    for i, node in enumerate(gfs.bones):
        matrix = node.bind_pose_matrix
        matrix = Matrix([matrix[0:4], matrix[4:8], matrix[8:12], [0., 0., 0., 1.]])

        if i not in bones_to_ignore:      
            bpy_bone = construct_bone(node.name, main_armature, 
                                     MayaBoneToBlenderBone(matrix), 
                                     10)
            if node.parent_idx > -1:
                bpy_bone.parent = bpy_nodes[node.parent_idx] 
            bpy_nodes[i]           = bpy_bone
            gfs_to_bpy_bone_map[i] = bpy_bone_counter
            bpy_bone_counter      += 1
            
            if not decomposableToTRS(matrix):
                skewed_bpm_nodes.append(i)
        
        t = node.position
        r = node.rotation
        s = node.scale
        rest_matrix = Matrix.Translation(t) @ Quaternion([r[3], r[0], r[1], r[2]]).to_matrix().to_4x4() @ Matrix.Diagonal([*s, 1.])
        if node.parent_idx > -1:
            bone_rest_transforms[i] = bone_rest_transforms[node.parent_idx] @ rest_matrix
        else:
            bone_rest_transforms[i] = convert_Yup_to_Zup(rest_matrix)
        bone_transforms[i] = convert_Yup_to_Zup(matrix)
        
    return bpy_nodes, bone_transforms, bone_rest_transforms, gfs_to_bpy_bone_map, skewed_bpm_nodes


def build_bones_from_rest_pose(gfs, main_armature, bones_to_ignore, raw_gfs):
    skewed_bpm_nodes = []
    gfs_to_bpy_bone_map = {}
    bpy_bone_counter = 0
    
    bpy_nodes       = [None]*len(gfs.bones)
    true_transforms = [None]*len(gfs.bones)
    bone_transforms = [None]*len(gfs.bones)
    for i, node in enumerate(gfs.bones):
        t = node.position
        r = node.rotation
        
        local_bind_matrix = Matrix.Translation(t) @ Quaternion([r[3], r[0], r[1], r[2]]).to_matrix().to_4x4()
        if node.parent_idx > -1:
            bind_matrix = true_transforms[node.parent_idx] @ local_bind_matrix
        else:
            bind_matrix = local_bind_matrix
            
        true_transforms[i] = bind_matrix

        if i not in bones_to_ignore:      
            bpy_bone = construct_bone(node.name, main_armature, 
                                     MayaBoneToBlenderBone(bind_matrix), 
                                     10)
            if node.parent_idx > -1:
                bpy_bone.parent = bpy_nodes[node.parent_idx] 
            bpy_nodes[i]           = bpy_bone
            gfs_to_bpy_bone_map[i] = bpy_bone_counter
            bpy_bone_counter      += 1
            
            if not decomposableToTRS(bind_matrix):
                skewed_bpm_nodes.append(i)

        bone_transforms[i] = convert_Yup_to_Zup(bind_matrix)
        
    # Now let's replace the mesh vertex data with transformed data
    gb = GFSBinary()
    gb.unpack(raw_gfs)
    model_binary = gb.get_model_block().data
    
    bones,   \
    meshes,  \
    cameras, \
    lights,  \
    epls     = NodeInterface.binary_node_tree_to_list(model_binary.root_node)

    matrix_lookup = model_binary.skinning_data.matrix_palette
    if matrix_lookup is not None:
        ibpms = model_binary.skinning_data.ibpms
        ibpms = [Matrix([ibpm[0:4], ibpm[4:8], ibpm[8:12], ibpm[12:16]]).transposed() for ibpm in ibpms]
        idx_count = len(matrix_lookup)
    
        y_up_to_z_up = convert_Yup_to_Zup(Matrix.Identity(4))
        for raw_mesh, mesh in zip(meshes, gfs.meshes):
            if mesh.vertices[0].indices is not None:
                for raw_v, v in zip(raw_mesh.vertices, mesh.vertices):
                    animation_matrix = Matrix.Diagonal([0., 0., 0., 0.])
                    for idx, weight in zip(raw_v.indices[::-1], raw_v.weights):
                        if idx >= idx_count: idx = 0
                        animation_matrix += weight*(true_transforms[matrix_lookup[idx]] @ ibpms[idx])
                    animation_matrix = y_up_to_z_up @ animation_matrix
                    if v.position is not None: v.position = (animation_matrix @ Vector([*v.position, 1.]))[:3]
                    if v.normal   is not None: v.normal   = (animation_matrix @ Vector([*v.normal,   0.])).normalized()[:3]
                    
                    # Not going to import these, no need to do them
                    #if v.tangent  is not None: v.tangent  = (animation_matrix @ Vector([*v.tangent,  0.])).normalized()[:3]
                    #if v.binormal is not None: v.binormal = (animation_matrix @ Vector([*v.binormal, 0.])).normalized()[:3]

    return bpy_nodes, bone_transforms, [Matrix.Identity(4) for b in bone_transforms], gfs_to_bpy_bone_map, skewed_bpm_nodes


def import_model(gfs, name, materials, errorlog, is_vertex_merge_allowed, bone_pose, raw_gfs, import_policies):
    """
    This is a really bad function. It's way too long - it needs to be split
    up into smaller, more modular chunks. Although it's all logically
    seperated into chunks, it's difficult to see where those chunk boundaries
    are when it's a single monolithic function.
    """
    initial_obj = bpy.context.view_layer.objects.active

    armature_name = name
    main_armature = bpy.data.objects.new(armature_name, bpy.data.armatures.new(armature_name))
    bpy.context.collection.objects.link(main_armature)
    bpy.context.view_layer.objects.active = main_armature
    
    main_armature.data.GFSTOOLS_ModelProperties.version          = f"0x{gfs.version:0>8x}"
    main_armature.data.GFSTOOLS_ModelProperties.flag_3           = gfs.flag_3
    main_armature.data.GFSTOOLS_ModelProperties.root_node_name   = gfs.bones[0].name if len(gfs.bones) else ""
    main_armature.data.GFSTOOLS_ModelProperties.has_external_emt = gfs.data_0x000100F8 is not None
    
    # Bounding box
    boxprops = main_armature.data.GFSTOOLS_ModelProperties.bounding_box
    boxprops.export_policy = "AUTO" if gfs.keep_bounding_box else "NONE"
    if gfs.keep_bounding_box:
        maxd = np.array(gfs.overrides.bounding_box.max_dims) @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy()
        mind = np.array(gfs.overrides.bounding_box.min_dims) @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy()
        boxprops.max_dims = np.max([maxd, mind], axis=0)
        boxprops.min_dims = np.min([maxd, mind], axis=0)
    
    # Bounding sphere
    sphprops = main_armature.data.GFSTOOLS_ModelProperties.bounding_sphere
    sphprops.export_policy = "AUTO" if gfs.keep_bounding_sphere else "NONE"
    if gfs.keep_bounding_sphere:
        sphprops.center = np.array(gfs.overrides.bounding_sphere.center) @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy()
        sphprops.radius = gfs.overrides.bounding_sphere.radius
    
    main_armature.rotation_mode = 'XYZ'
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    # nodes_with_meshes = set()
    # for mesh in gfs.meshes:
    #     nodes_with_meshes.add(mesh.node)
    
    bones_to_ignore = set()
    rigged_bones, unrigged_bones = filter_rigging_bones_and_ancestors(gfs)
    # meshes_to_rename             = set.intersection(rigged_bones,   nodes_with_meshes)
    # bones_to_ignore              = set.intersection(unrigged_bones, nodes_with_meshes)
    # unrigged_bones_to_import     = set.difference  (unrigged_bones, bones_to_ignore)
    
    # Get rid of root node
    bones_to_ignore.add(0)
    bpy_node_names  = [None]*len(gfs.bones)
    
    # Import nodes
    if bone_pose == "bindpose":
        bpy_nodes,            \
        bone_transforms,      \
        bone_rest_transforms, \
        gfs_to_bpy_bone_map,  \
        skewed_bpm_nodes = build_bones_from_bind_pose(gfs, main_armature, bones_to_ignore)
    elif bone_pose == "restpose":
        bpy_nodes,            \
        bone_transforms,      \
        bone_rest_transforms, \
        gfs_to_bpy_bone_map,  \
        skewed_bpm_nodes = build_bones_from_rest_pose(gfs, main_armature, bones_to_ignore, raw_gfs)
    else:
        errorlog.log_error_message(f"CRITICAL INTERNAL ERROR: Did not recognise bone pose '{bone_pose}'. THIS IS A BUG - PLEASE REPORT IT.")

    if len(skewed_bpm_nodes):
        errorlog.log_warning_message(f"{len(skewed_bpm_nodes)} bones have skewed bind pose matrices. This should *not* happen, and is probably due to a buggy model. Bone rotations are likely to be incorrect. A list of skewed bones is printed in the console.")
        print(", ".join([gfs.bones[i].name for i in skewed_bpm_nodes]))

    bpy.ops.object.mode_set(mode="OBJECT")

    # Figure out bone names
    for i, node in enumerate(gfs.bones):
        if i in gfs_to_bpy_bone_map:
            bpy_bone = main_armature.data.bones[gfs_to_bpy_bone_map[i]]
            bpy_node_name = bpy_bone.name
            bpy_node_names[i] = bpy_node_name
            if bpy_node_name != node.name:
                bpy_bone.GFSTOOLS_NodeProperties.override_name = node.name
        else:
            bpy_node_names[i] = node.name
    

    # If there are meshes, create bone layers of rigged and unrigged bones
    if len(gfs.meshes):
        if bpy_at_least(4, 0, 0):
            col_rigbones   = main_armature.data.collections.new("Rigged Bones")
            col_norigbones = main_armature.data.collections.new("Unrigged Bones")
            
            for bpy_bone in main_armature.data.bones:
                col_rigbones.assign(bpy_bone)
            
            for i in sorted(unrigged_bones):
                remapped_index = gfs_to_bpy_bone_map[i]
                bpy_bone = main_armature.data.bones[remapped_index]
                
                col_rigbones.unassign(bpy_bone)
                col_norigbones.assign(bpy_bone)
        else:
            for bpy_bone in main_armature.data.bones:
                bpy_bone.layers[0] = True
                bpy_bone.layers[1] = True
                bpy_bone.layers[2] = False
        
            #for i in sorted(unrigged_bones_to_import):
            for i in sorted(unrigged_bones):
                remapped_index = gfs_to_bpy_bone_map[i]
                main_armature.data.bones[remapped_index].layers[0] = True
                main_armature.data.bones[remapped_index].layers[1] = False
                main_armature.data.bones[remapped_index].layers[2] = True
        
    bpy.context.view_layer.objects.active = main_armature
    
    ###################
    # PUSH EXTRA DATA #
    ###################
    # Import root node as the armature
    if len(gfs.bones):
        node = gfs.bones[0]
        main_armature.data.GFSTOOLS_NodeProperties.unknown_float = node.unknown_float
        import_properties(gfs.bones[0].properties, main_armature.data.GFSTOOLS_NodeProperties.properties)
    
    # Now import other nodes
    for i, node in enumerate(gfs.bones):
        # We'll import properties to the meshes during mesh import
        if (i in bones_to_ignore):# or (i in meshes_to_rename):
            continue
        
        bpy_bone = main_armature.data.bones[gfs_to_bpy_bone_map[i]]
        bpy_bone.GFSTOOLS_NodeProperties.unknown_float = node.unknown_float
        
        import_properties(node.properties, bpy_bone.GFSTOOLS_NodeProperties.properties)
    
    
    #######################
    # ADJUST BONE LENGTHS #
    #######################
    min_bone_length = 0.01
    dims = calc_model_dims(gfs)
    if dims is None:
        dims = Vector([10., 10., 10.])
    else:
        dims = Vector([max(0.05*d, min_bone_length) for d in dims])
    
    bpy.context.view_layer.objects.active = main_armature
    bpy.ops.object.mode_set(mode="EDIT")
    
    for bpy_bone in main_armature.data.edit_bones:
        resize_bone_length(bpy_bone, dims, min_bone_length)
        
    if import_policies.connect_child_bones:
        for bpy_bone in main_armature.data.edit_bones:
            for child in bpy_bone.children:
                child_pos = np.array(list(child.head))
                this_tail = np.array(list(bpy_bone.tail))
                if np.allclose(child_pos, this_tail, rtol=1e-4, atol=1e-4):
                    child.use_connect = True
                
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.mode_set(mode="EDIT")
        
    
    ######################
    # IMPORT ATTACHMENTS #
    ######################
    # Import meshes and parent them to the armature
    # While we're building the meshes, infer which materials need which vertex
    # attributes by asking the meshes what vertex attributes they have
    material_vertex_attributes = {k: VertexAttributeTracker() for k in materials.keys()}
    mesh_groups = {idx: [] for idx in sorted(set((mesh.node for mesh in gfs.meshes)))}
    for mesh in gfs.meshes:
        mesh_groups[mesh.node].append(mesh)
    for node_idx, meshes in mesh_groups.items():
        mesh_name = bpy_node_names[node_idx]
        for i, mesh in zip([None, *list(range(len(meshes)))], meshes):
            import_mesh(mesh_name, bpy_node_names[node_idx], i, mesh, bone_transforms[node_idx], bone_rest_transforms[node_idx], bpy_node_names, main_armature, materials, material_vertex_attributes, errorlog, is_vertex_merge_allowed)
    
    set_material_vertex_attributes(materials, material_vertex_attributes, errorlog)
        
    # Import cameras
    for i, cam in enumerate(gfs.cameras):
        import_camera("camera", i, cam, main_armature, bpy_node_names)
    
    # Import lights
    for i, light in enumerate(gfs.lights):
        import_light("light", i, light, main_armature, bpy_node_names)
    
    bpy.ops.object.mode_set(mode="OBJECT")
    
    # Reset state
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = initial_obj

    return main_armature, gfs_to_bpy_bone_map


def filter_rigging_bones_and_ancestors(gfs):
    used_indices = set()
    for mesh in gfs.meshes:
        if mesh.vertices[0].indices is None:
            # Because we're going to rig the mesh to the bone later
            # Can get rid of this if we replace that with bone parenting
            used_indices.add(mesh.node)
        else:
            for v in mesh.vertices:
                used_indices.update([idx for idx, wgt in zip(v.indices, v.weights) if wgt > 0])
    
    for cam in gfs.cameras:
        used_indices.add(cam.node)
    for light in gfs.lights:
        used_indices.add(light.node)
                
    bones_to_check = sorted(used_indices)
    for bone_idx in bones_to_check:
        node = gfs.bones[bone_idx]
        while node.parent_idx != -1:
            used_indices.add(node.parent_idx)
            node = gfs.bones[node.parent_idx]
    
    unused_indices = set([i for i in range(len(gfs.bones))]).difference(used_indices)

    return used_indices, unused_indices


class MergedVertex:
    # Required interface    
    @classmethod
    def from_unmerged(cls, unmerged_verts):
        # All vertices entering this should have the same position, indices, and weights
        v0 = unmerged_verts[0]
        instance = cls(v0.position, v0.indices, v0.weights)
        
        return instance
    
    @staticmethod
    def get_position(v):
        return v.position
    
    @staticmethod
    def get_merge_attributes(v):
        return [v.indices, v.weights]
    
    @staticmethod
    def is_invalid(v):
        return any(any(np.isnan(l)) for l in (v.position, v.indices, v.weights))
    
    # Specialized implementation
    def __init__(self, position, indices, weights):
        self.position = position
        self.indices  = indices
        self.weights  = weights


class UnweightedMergedVertex(MergedVertex):
    @staticmethod
    def get_merge_attributes(v):
        return []
    
    @staticmethod
    def is_invalid(v):
        return any(np.isnan(v.position))


def import_mesh(mesh_name, parent_node_name, idx, mesh, bind_transform, rest_transform, bpy_node_names, armature, materials, material_vertex_attributes, errorlog, is_vertex_merge_allowed):
    # Cache the Blender states we are going to change
    prev_obj = bpy.context.view_layer.objects.active
    
    # What about vertex merging?
    if idx is None:
        meshobj_name = mesh_name
    else:
        meshobj_name = f"{mesh_name}_{idx}"
    
    is_rigged = mesh.vertices[0].weights is not None
    
    # Merge vertices if requested
    mesh_data = create_merged_mesh(meshobj_name, 
                                   mesh.vertices, 
                                   [(a, b, c) for a, b, c in zip(mesh.indices[0::3], mesh.indices[1::3], mesh.indices[2::3])],
                                   MergedVertex if is_rigged else UnweightedMergedVertex,
                                   attempt_merge=is_vertex_merge_allowed,
                                   errorlog=errorlog)
    bpy_mesh = mesh_data.bpy_mesh
    
    # Construct object
    bpy_mesh_object = bpy.data.objects.new(meshobj_name, bpy_mesh)
    bpy.context.collection.objects.link(bpy_mesh_object)
    bpy.context.view_layer.objects.active = bpy_mesh_object
    
    oprops    = bpy_mesh_object.GFSTOOLS_ObjectProperties
    mprops    = bpy_mesh.GFSTOOLS_MeshProperties
    new_verts = mesh_data.vertices

    ####################
    # IMPORT LOOP DATA #
    ####################
    loop_data             = mesh_data.loops
    bpy_vert_to_gfs_verts = mesh_data.verts_to_modelverts_map

    # Create UVs
    create_uv_map_if_exists(bpy_mesh, make_uv_map_name(0), [v.texcoord0 for v in loop_data])
    create_uv_map_if_exists(bpy_mesh, make_uv_map_name(1), [v.texcoord1 for v in loop_data])
    create_uv_map_if_exists(bpy_mesh, make_uv_map_name(2), [v.texcoord2 for v in loop_data])
    create_uv_map_if_exists(bpy_mesh, make_uv_map_name(3), [v.texcoord3 for v in loop_data])
    create_uv_map_if_exists(bpy_mesh, make_uv_map_name(4), [v.texcoord4 for v in loop_data])
    create_uv_map_if_exists(bpy_mesh, make_uv_map_name(5), [v.texcoord5 for v in loop_data])
    create_uv_map_if_exists(bpy_mesh, make_uv_map_name(6), [v.texcoord6 for v in loop_data])
    create_uv_map_if_exists(bpy_mesh, make_uv_map_name(7), [v.texcoord7 for v in loop_data])

    # Create Vertex Colours
    create_color_map_if_exists(bpy_mesh, make_color_map_name(0), [v.color1 for v in loop_data], "BYTE")
    create_color_map_if_exists(bpy_mesh, make_color_map_name(1), [v.color2 for v in loop_data], "BYTE")

    # Rig
    if is_rigged: rig_mesh   (bpy_mesh_object, bpy_node_names,   new_verts, mprops)
    else:         attach_mesh(bpy_mesh_object, parent_node_name, new_verts, mprops)

    # Assign normals
    if loop_data[0].normal is not None:
        create_loop_normals(bpy_mesh, [l.normal for l in loop_data])
    
    ####################
    # SET THE MATERIAL #
    ####################
    set_material(bpy_mesh_object, mesh, materials, material_vertex_attributes, errorlog)
    
    #################
    # FINALISE MESH #
    #################
    bpy_mesh.validate(verbose=True, clean_customdata=False)
    bpy_mesh.use_auto_smooth = True
    
    bpy_mesh.update()
    bpy_mesh.update()

    # Activate rigging
    modifier = bpy_mesh_object.modifiers.new(name="Armature", type="ARMATURE")
    modifier.object = armature
    
    
    #####################
    # IMPORT MORPH KEYS #
    #####################
    if len(mesh.morphs):
        import_morphs(bpy_mesh_object, new_verts, mesh, bpy_vert_to_gfs_verts)
        
    ########################
    # DO THE LEFTOVER DATA #
    ########################
    mprops.flag_5   = mesh.flag_5
    mprops.flag_7   = mesh.flag_7
    mprops.flag_8   = mesh.flag_8
    mprops.flag_9   = mesh.flag_9
    mprops.flag_10  = mesh.flag_10
    mprops.flag_11  = mesh.flag_11
    mprops.flag_13  = mesh.flag_13
    mprops.flag_14  = mesh.flag_14
    mprops.flag_15  = mesh.flag_15
    mprops.flag_16  = mesh.flag_16
    mprops.flag_17  = mesh.flag_17
    mprops.flag_18  = mesh.flag_18
    mprops.flag_19  = mesh.flag_19
    mprops.flag_20  = mesh.flag_20
    mprops.flag_21  = mesh.flag_21
    mprops.flag_22  = mesh.flag_22
    mprops.flag_23  = mesh.flag_23
    mprops.flag_24  = mesh.flag_24
    mprops.flag_25  = mesh.flag_25
    mprops.flag_26  = mesh.flag_26
    mprops.flag_27  = mesh.flag_27
    mprops.flag_28  = mesh.flag_28
    mprops.flag_29  = mesh.flag_29
    mprops.flag_30  = mesh.flag_30
    mprops.flag_31  = mesh.flag_31

    # Unknowns
    mprops.unknown_0x12  = mesh.unknown_0x12
    if mesh.unknown_float_1 is not None and mesh.unknown_float_2 is not None:
        mprops.has_unknown_floats = True
        mprops.unknown_float_1  = mesh.unknown_float_1
        mprops.unknown_float_2  = mesh.unknown_float_2
    
    # Bounding box
    if mesh.keep_bounding_box:
        mprops.bounding_box.export_policy = "AUTO"
        mprops.bounding_box.min_dims = np.array(mesh.overrides.bounding_box.min_dims)# @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy() 
        mprops.bounding_box.max_dims = np.array(mesh.overrides.bounding_box.max_dims)# @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy()
    else:
        mprops.bounding_box.export_policy = "NONE"
    
    # Bounding sphere
    if mesh.keep_bounding_sphere:
        mprops.bounding_sphere.export_policy = "AUTO"
        mprops.bounding_sphere.center = np.array(mesh.overrides.bounding_sphere.center)# @ GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy() 
        mprops.bounding_sphere.radius = mesh.overrides.bounding_sphere.radius
    else:
        mprops.bounding_sphere.export_policy = "NONE"
    
    bpy.context.view_layer.objects.active = prev_obj

    ####################
    # SCENE PROPERTIES #
    ####################
    bpy_mesh_object.parent = armature
    if is_rigged:
        transform = rest_transform
    else:
        transform = bind_transform

    # Set transform
    if not decomposableToTRS(transform):
        errorlog.log_warning_message(f"Mesh '{mesh_name}' has a skewed world transform. This means that non-uniform scales are present in the non-leaf nodes used to position the mesh. This is not possible to represent in Blender, and you should expect this mesh to have an incorrect rotation and scale.")


    pos, quat, scale = transform.decompose()
    bpy_mesh_object.rotation_mode = "XYZ"
    bpy_mesh_object.location = pos
    bpy_mesh_object.rotation_quaternion = quat
    bpy_mesh_object.rotation_euler = quat.to_euler('XYZ')
    bpy_mesh_object.scale = scale
    
    oprops.node = parent_node_name
    

    return bpy_mesh_object


def create_uv_map_if_exists(bpy_mesh, name, texcoords):
    if texcoords[0] is not None:
        create_uv_map(bpy_mesh, name, texcoords)


def unpack_colour(colour):
    # ARGB -> RGBA
    return [colour[1], colour[2], colour[3], colour[0]]


def create_color_map_if_exists(bpy_mesh, name, color_data, datatype):
    if color_data[0] is not None:
        create_color_map(bpy_mesh, name, [unpack_colour(c) for c in color_data], datatype)


def set_material(bpy_mesh_object, gfs_mesh, materials, material_vertex_attributes, errorlog):
    bpy_mesh = bpy_mesh_object.data
    
    if gfs_mesh.material_name is not None:
        active_material, gfs_material = materials.get(gfs_mesh.material_name)
        if active_material is not None:
            bpy_mesh.materials.append(active_material)
            bpy_mesh_object.active_material = active_material
            vas = material_vertex_attributes[gfs_mesh.material_name]
            
            vas.normals  .append(gfs_mesh.vertices[0].normal   is not None)
            vas.tangents .append(gfs_mesh.vertices[0].tangent  is not None)
            vas.binormals.append(gfs_mesh.vertices[0].binormal is not None)
            vas.color0s  .append(gfs_mesh.vertices[0].color1   is not None)
            vas.color1s  .append(gfs_mesh.vertices[0].color2   is not None)
            
            if gfs_mesh.vertices[0].tangent is not None:
                if len(bpy_mesh.uv_layers):
                    uv_map = bpy_mesh.uv_layers.active
                    
                    if gfs_material.normal_texture is not None:
                        uv_idx = gfs_material.texture_indices_1.normal
                        uv_map_name = make_uv_map_name(uv_idx)
                        if uv_map_name in bpy_mesh.uv_layers:
                            uv_map = bpy_mesh.uv_layers[uv_map_name]
                        else:
                            errorlog.log_warning_message(f"Mesh '{bpy_mesh_object.name}' uses material '{active_material.name}', which uses UV map '{uv_map_name}' for the normal texture but this UV map is not present on the mesh - falling back to the active UV map to calculate vertex tangents.")
                    else:
                        errorlog.log_warning_message(f"Mesh '{bpy_mesh_object.name}' has tangent vectors, but no normal map - using the default UV map to calculate tangent vectors.")
                    
                    bpy_mesh.calc_tangents(uvmap=uv_map.name)
                else:
                    errorlog.log_warning_message(f"Mesh '{bpy_mesh_object.name}' has tangents but no UV layers - tangents cannot be imported to Blender.")


def import_camera(name, i, camera, armature, bpy_node_names):
    bpy_camera = bpy.data.cameras.new(f"{name}_{i}")
    
    # Import attributes
    bpy_camera.type       = "PERSP"
    bpy_camera.clip_start = camera.binary.zNear
    bpy_camera.clip_end   = camera.binary.zFar
    bpy_camera.lens_unit  = "FOV"
    bpy_camera.angle      = camera.binary.fov # Need to compare with camera sensor
    
    # Custom properties
    bpy_camera.GFSTOOLS_CameraProperties.aspect_ratio = camera.binary.aspect_ratio # Can hook into Blender scene callback
    bpy_camera.GFSTOOLS_CameraProperties.unknown_0x50 = camera.binary.unknown_0x50 # Always 0...

    # Create the object
    bpy_camera_object = bpy.data.objects.new(bpy_camera.name, bpy_camera)
    bpy.context.collection.objects.link(bpy_camera_object)

    # Lock Transforms
    lock_obj_transforms(bpy_camera_object)
    
    # Link to the armature
    cam_bone = bpy_node_names[camera.node]
    constraint = bpy_camera_object.constraints.new("CHILD_OF")
    constraint.target    = armature
    constraint.subtarget = cam_bone
    constraint.inverse_matrix = Matrix.Identity(4)
    parent_transform = Quaternion([.5**.5, 0., 0., .5**.5]).to_matrix().to_4x4()
    
    # Set view matrix
    bpy_camera_object.matrix_local = Matrix([camera.binary.view_matrix[ 0: 4],
                                             camera.binary.view_matrix[ 4: 8],
                                             camera.binary.view_matrix[ 8:12],
                                             camera.binary.view_matrix[12:16]]) @ parent_transform


def import_light(name, i, light, armature, bpy_node_names):
    bpy_light = bpy.data.lights.new(f"{name}_{i}", "POINT")
    
    # Custom properties
    bpy_light.GFSTOOLS_LightProperties.flag_0  = light.binary.flags.flag_0
    bpy_light.GFSTOOLS_LightProperties.unk_setting = light.binary.flags.unk_setting
    bpy_light.GFSTOOLS_LightProperties.flag_2  = light.binary.flags.flag_2
    bpy_light.GFSTOOLS_LightProperties.flag_3  = light.binary.flags.flag_3
    bpy_light.GFSTOOLS_LightProperties.flag_4  = light.binary.flags.flag_4
    bpy_light.GFSTOOLS_LightProperties.flag_5  = light.binary.flags.flag_5
    bpy_light.GFSTOOLS_LightProperties.flag_6  = light.binary.flags.flag_6
    bpy_light.GFSTOOLS_LightProperties.flag_7  = light.binary.flags.flag_7
    bpy_light.GFSTOOLS_LightProperties.flag_8  = light.binary.flags.flag_8
    bpy_light.GFSTOOLS_LightProperties.flag_9  = light.binary.flags.flag_9
    bpy_light.GFSTOOLS_LightProperties.flag_10 = light.binary.flags.flag_10
    bpy_light.GFSTOOLS_LightProperties.flag_11 = light.binary.flags.flag_11
    bpy_light.GFSTOOLS_LightProperties.flag_12 = light.binary.flags.flag_12
    bpy_light.GFSTOOLS_LightProperties.flag_13 = light.binary.flags.flag_13
    bpy_light.GFSTOOLS_LightProperties.flag_14 = light.binary.flags.flag_14
    bpy_light.GFSTOOLS_LightProperties.flag_15 = light.binary.flags.flag_15
    bpy_light.GFSTOOLS_LightProperties.flag_16 = light.binary.flags.flag_16
    bpy_light.GFSTOOLS_LightProperties.flag_17 = light.binary.flags.flag_17
    bpy_light.GFSTOOLS_LightProperties.flag_18 = light.binary.flags.flag_18
    bpy_light.GFSTOOLS_LightProperties.flag_19 = light.binary.flags.flag_19
    bpy_light.GFSTOOLS_LightProperties.flag_20 = light.binary.flags.flag_20
    bpy_light.GFSTOOLS_LightProperties.flag_21 = light.binary.flags.flag_21
    bpy_light.GFSTOOLS_LightProperties.flag_22 = light.binary.flags.flag_22
    bpy_light.GFSTOOLS_LightProperties.flag_23 = light.binary.flags.flag_23
    bpy_light.GFSTOOLS_LightProperties.flag_24 = light.binary.flags.flag_24
    bpy_light.GFSTOOLS_LightProperties.flag_25 = light.binary.flags.flag_25
    bpy_light.GFSTOOLS_LightProperties.flag_26 = light.binary.flags.flag_26
    bpy_light.GFSTOOLS_LightProperties.flag_27 = light.binary.flags.flag_27
    bpy_light.GFSTOOLS_LightProperties.flag_28 = light.binary.flags.flag_28
    bpy_light.GFSTOOLS_LightProperties.flag_29 = light.binary.flags.flag_29
    bpy_light.GFSTOOLS_LightProperties.flag_30 = light.binary.flags.flag_30
    bpy_light.GFSTOOLS_LightProperties.flag_31 = light.binary.flags.flag_31
    
    bpy_light.GFSTOOLS_LightProperties.color_1 = light.binary.color_1
    bpy_light.color = light.binary.color_2[:3]
    bpy_light.GFSTOOLS_LightProperties.alpha = light.binary.color_2[3]
    bpy_light.GFSTOOLS_LightProperties.color_3 = light.binary.color_3
    
    if light.binary.inner_radius is not None: bpy_light.GFSTOOLS_LightProperties.inner_radius = light.binary.inner_radius
    if light.binary.outer_radius is not None: bpy_light.GFSTOOLS_LightProperties.outer_radius = light.binary.outer_radius
    
    if light.binary.unknown_0x28 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x28 = light.binary.unknown_0x28
    if light.binary.unknown_0x2C is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x2C = light.binary.unknown_0x2C
    if light.binary.unknown_0x30 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x30 = light.binary.unknown_0x30
    if light.binary.unknown_0x34 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x34 = light.binary.unknown_0x34
    if light.binary.unknown_0x38 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x38 = light.binary.unknown_0x38
    if light.binary.unknown_0x3C is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x3C = light.binary.unknown_0x3C
    if light.binary.unknown_0x48 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x48 = light.binary.unknown_0x48
    if light.binary.unknown_0x4C is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x4C = light.binary.unknown_0x4C
    if light.binary.unknown_0x50 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x50 = light.binary.unknown_0x50
    if light.binary.unknown_0x54 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x54 = light.binary.unknown_0x54
    if light.binary.unknown_0x58 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x58 = light.binary.unknown_0x58
    if light.binary.unknown_0x5C is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x5C = light.binary.unknown_0x5C
    if light.binary.unknown_0x60 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x60 = light.binary.unknown_0x60
    if light.binary.unknown_0x64 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x64 = light.binary.unknown_0x64
    if light.binary.unknown_0x68 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x68 = light.binary.unknown_0x68
    if light.binary.unknown_0x6C is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x6C = light.binary.unknown_0x6C
    if light.binary.unknown_0x70 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x70 = light.binary.unknown_0x70
    if light.binary.unknown_0x7C is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x7C = light.binary.unknown_0x7C
    if light.binary.unknown_0x80 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x80 = light.binary.unknown_0x80
    if light.binary.unknown_0x84 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x84 = light.binary.unknown_0x84
    
    # Create the object
    bpy_light_object = bpy.data.objects.new(bpy_light.name, bpy_light)
    bpy.context.collection.objects.link(bpy_light_object)

    # Lock Transforms
    lock_obj_transforms(bpy_light_object)
    
    # Link to the armature
    light_bone = bpy_node_names[light.node]
    constraint = bpy_light_object.constraints.new("CHILD_OF")
    constraint.target    = armature
    constraint.subtarget = light_bone
    constraint.inverse_matrix = Matrix.Identity(4)
    
    transform = Quaternion([.5**.5, 0., 0., .5**.5]).to_matrix().to_4x4()
    bpy_light_object.matrix_local = transform


def rig_mesh(bpy_mesh_object, bpy_node_names, new_verts, mprops):
    mprops.permit_unrigged_export = False
    groups = {}
    for vert_idx, v in enumerate(new_verts):
        for bone_idx, weight in zip(v.indices, v.weights):
            if weight == 0.:
                continue
            if bone_idx not in groups:
                groups[bone_idx] = []
            groups[bone_idx].append((vert_idx, weight))
    for bone_idx, vg in groups.items():
        vertex_group = bpy_mesh_object.vertex_groups.new(name=bpy_node_names[bone_idx])
        for vert_idx, vert_weight in vg:
            vertex_group.add([vert_idx], vert_weight, 'REPLACE')


def attach_mesh(bpy_mesh_object, parent_node_name, new_verts, mprops):
    vertex_group = bpy_mesh_object.vertex_groups.new(name=parent_node_name)
    vertex_group.add([i for i in range(len(new_verts))], 1., 'REPLACE')
    mprops.permit_unrigged_export = True
    
    
def import_morphs(bpy_mesh_object, new_verts, mesh, bpy_vert_to_gfs_verts):
    # This is a bit simplified.
    # There are a few bits of data here that are neglected since they seem to
    # always take the same values / be unused.
    # The entire morph set has flags that always seems to just be 0x00000002,
    # each morph itself has flags that always seems to just be 0x00000002,
    # and then there's a set of integers as an attachment to nodes with
    # morphable meshes that always just seems to be a list of 0s with the
    # same length as the morph set.
    # We're just going to ignore that data on import (since it's not added to
    # the GFSInterface) and create it on export automatically with the
    # GFSInterface.
    # Use the GFSBinary in a separate script if, for some reason, these values
    # need to be edited!
    
    # Create base position
    sk_basis = bpy_mesh_object.shape_key_add(name='Basis')
    sk_basis.interpolation = 'KEY_LINEAR'
    bpy_mesh_object.data.shape_keys.use_relative = True
    for vidx, v in enumerate(new_verts):
        sk_basis.data[vidx].co = v.position
    
    # Import each shape key
    for i, position_deltas in enumerate(mesh.morphs):
        sk = bpy_mesh_object.shape_key_add(name=str(i))
        sk.interpolation = "KEY_LINEAR"
        
        # position each vert
        for bpy_vidx, gfs_vidxs in bpy_vert_to_gfs_verts.items():
            vert_position_deltas = [position_deltas[gfs_vidx] for gfs_vidx in gfs_vidxs]
            
            # Safety check: Check that the shapekey is manifold
            avg_pos = [sum(dim)/len(vert_position_deltas) for dim in zip(*vert_position_deltas)]
            for delta in vert_position_deltas:
                # Check if any of the deltas disagree by more than 0.1% from the average
                if any([abs((pi - di)/di) > 0.001 
                        if   (abs(di) > 0.001 and abs(pi) > 0.001) 
                        else (pi - di) > 0.001
                        for  (pi, di)
                        in   zip(avg_pos, delta)]):
                    raise ValueError("Invalid shapekey. Try importing without merging vertices.")
                    
            sk.data[bpy_vidx].co = [x1 + x2 for x1, x2 in zip(new_verts[bpy_vidx].position, vert_position_deltas[0])]
            

def make_bounding_box(gfs):
    maxes = []
    mins = []
    for mesh in gfs.meshes:
        if mesh.vertices[0].position is not None:
            local_max = mesh.vertices[0].position
            local_min = mesh.vertices[0].position
            for vertex in mesh.vertices[1:]:
                pos = vertex.position
                local_max = [max(mx, p) for mx, p in zip(local_max, pos)]
                local_min = [min(mn, p) for mn, p in zip(local_min, pos)]
            maxes.append(local_max)
            mins.append(local_min)
            
    if len(maxes):
        global_max = [max(ps) for ps in zip(*maxes)]
        global_min = [max(ps) for ps in zip(*mins)]
        
        return global_max, global_min
    else:
        return None, None
    

def calc_model_dims(gfs):
    mx, mn = make_bounding_box(gfs)
    if mx is None:
        return None
    else:
        return [mxi - mni for mxi, mni in zip(mx, mn)]

        
def set_material_vertex_attributes(materials, material_vertex_attributes, errorlog):
    for key in materials:
        props = materials[key][0].GFSTOOLS_MaterialProperties
        vas   = material_vertex_attributes[key]
        
        # Normals
        if any(vas.normals):
            if not all(vas.normals):
                errorlog.log_warning_message(f"Meshes using material '{key}' inconsistently possess vertex normals - assuming the material requires normals")
            props.requires_normals = True
        else:
            props.requires_normals = False
        
        # Tangents
        if any(vas.tangents):
            if not all(vas.tangents):
                errorlog.log_warning_message(f"Meshes using material '{key}' inconsistently possess vertex tangents - assuming the material requires tangents")
            props.requires_tangents = True
        else:
            props.requires_tangents = False

        # Binormals
        if any(vas.binormals):
            if not all(vas.binormals):
                errorlog.log_warning_message(f"Meshes using material '{key}' inconsistently possess vertex binormals - assuming the material requires binormals")
            props.requires_binormals = True
        else:
            props.requires_binormals = False

        # Color0
        if any(vas.color0s):
            if not all(vas.color0s):
                errorlog.log_warning_message(f"Meshes using material '{key}' inconsistently possess vertex color map 0 - assuming the material requires color map 0")
            props.requires_color0s = True
        else:
            props.requires_color0s = False

        # Color1
        if any(vas.color1s):
            if not all(vas.color1s):
                errorlog.log_warning_message(f"Meshes using material '{key}' inconsistently possess vertex color map 1 - assuming the material requires color map 1")
            props.requires_color1s = True
        else:
            props.requires_color1s = False
