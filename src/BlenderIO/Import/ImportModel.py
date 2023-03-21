import array
import math

import bpy
from mathutils import Matrix, Vector, Quaternion

from ...FileFormats.GFS import GFSBinary
from ...FileFormats.GFS.SubComponents.CommonStructures.SceneNode import NodeInterface
from ..Utils.Maths import MayaBoneToBlenderBone, convert_Yup_to_Zup, decomposableToTRS
from ..Utils.Object import lock_obj_transforms
from ..Utils.UVMapManagement import make_uv_map_name
from ..Utils.UVMapManagement import make_color_map_name
from .Utils.BoneConstruction import construct_bone, resize_bone_length
from .Utils.VertexMerging    import merge_vertices, facevert_to_loop_lookup
from .ImportProperties import import_properties


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


def build_bones_from_rest_pose(gfs, main_armature, bones_to_ignore, filepath):
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
    gb.read(filepath)
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



def import_model(gfs, name, materials, errorlog, is_vertex_merge_allowed, bone_pose, filepath):
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
    
    main_armature.data.GFSTOOLS_ModelProperties.root_node_name         = gfs.bones[0].name if len(gfs.bones) else ""
    main_armature.data.GFSTOOLS_ModelProperties.has_external_emt       = gfs.data_0x000100F8 is not None
    main_armature.data.GFSTOOLS_ModelProperties.export_bounding_box    = gfs.keep_bounding_box
    main_armature.data.GFSTOOLS_ModelProperties.export_bounding_sphere = gfs.keep_bounding_sphere
    main_armature.data.GFSTOOLS_ModelProperties.flag_3                 = gfs.flag_3
    main_armature.rotation_mode = 'XYZ'
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    nodes_with_meshes = set()
    for mesh in gfs.meshes:
        nodes_with_meshes.add(mesh.node)
    
    rigged_bones, unrigged_bones = filter_rigging_bones_and_ancestors(gfs)
    meshes_to_rename             = set.intersection(rigged_bones,   nodes_with_meshes)
    bones_to_ignore              = set.intersection(unrigged_bones, nodes_with_meshes)
    unrigged_bones_to_import     = set.difference  (unrigged_bones, bones_to_ignore)
    
    # Get rid of root node
    bones_to_ignore.add(0)
    bpy_node_names  = [None]*len(gfs.bones)
    mesh_node_map = {}

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
        skewed_bpm_nodes = build_bones_from_rest_pose(gfs, main_armature, bones_to_ignore, filepath)
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
        for bpy_bone in main_armature.data.bones:
            bpy_bone.layers[0] = True
            bpy_bone.layers[1] = True
            bpy_bone.layers[2] = False
    
        for i in sorted(unrigged_bones_to_import):
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
        if (i in bones_to_ignore) or (i in meshes_to_rename):
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
        bpy_mesh_obj = import_mesh_group(mesh_name, gfs.bones[node_idx], bpy_node_names[node_idx], i, meshes, bpy_node_names, main_armature, bone_transforms[node_idx], bone_rest_transforms[node_idx], materials, material_vertex_attributes, errorlog, is_vertex_merge_allowed, node_idx in meshes_to_rename)
        mesh_node_map[node_idx] = bpy_mesh_obj.data
    
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

    return main_armature, gfs_to_bpy_bone_map, mesh_node_map


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


def import_mesh_group(mesh_name, gfs_node, parent_node_name, idx, meshes, bpy_node_names, armature, bind_transform, rest_transform, materials, material_vertex_attributes, errorlog, is_vertex_merge_allowed, requires_rename):
    if requires_rename:
        mesh_name += "_mesh"
    bpy_mesh_object = import_mesh(mesh_name, parent_node_name, None, meshes[0], bpy_node_names, armature, materials, material_vertex_attributes, errorlog, is_vertex_merge_allowed)


    bpy_mesh_object.parent = armature
    
    # There's going to be a bug here if unrigged and rigged meshes share a
    # positioning node.
    # This should be fixed, but it's so unlikely that it's barely ever
    # going to actually happen...
    # Fix when less lazy
    # We differentiate between rigged and unrigged meshes here in the first
    # place because the game does too.
    # We treat unrigged meshes as being rigged only to a single bone. That
    # single bone can control the scale of the mesh via animation.
    # The rigged meshes can't have their positioning node animated. So we
    # place them in their rest pose, where they have correct access to their
    # bones.
    is_unrigged = meshes[0].vertices[0].indices is None
    if is_unrigged:
        transform = bind_transform
    else:
        transform = rest_transform
        if not decomposableToTRS(transform):
            errorlog.log_warning_message(f"Mesh '{mesh_name}' has a skewed world transform. This means that non-uniform scales are present in the non-leaf nodes used to position the mesh. This is not possible to represent in Blender, and you should expect this mesh to have an incorrect rotation and scale.")
    
    # Set transform
    pos, quat, scale = transform.decompose()
    bpy_mesh_object.rotation_mode = "XYZ"
    bpy_mesh_object.location = pos
    bpy_mesh_object.rotation_quaternion = quat
    bpy_mesh_object.rotation_euler = quat.to_euler('XYZ')
    bpy_mesh_object.scale = scale
    
  
    # Add Node Properties
    bpy_mesh_object.data.GFSTOOLS_NodeProperties.unknown_float = gfs_node.unknown_float
    import_properties(gfs_node.properties, bpy_mesh_object.data.GFSTOOLS_NodeProperties.properties)

    for i, mesh in enumerate(meshes[1:]):
        child_bpy_mesh_object = import_mesh(mesh_name, parent_node_name, i, mesh, bpy_node_names, armature, materials, material_vertex_attributes, errorlog, is_vertex_merge_allowed)
    
        child_bpy_mesh_object.parent = bpy_mesh_object
        child_bpy_mesh_object.rotation_mode = "QUATERNION"
        child_bpy_mesh_object.location = [0., 0., 0.]
        child_bpy_mesh_object.rotation_quaternion = [1., 0., 0., 0.]
        child_bpy_mesh_object.scale = [1., 1., 1.]
  
    return bpy_mesh_object
    
    
def import_mesh(mesh_name, parent_node_name, idx, mesh, bpy_node_names, armature, materials, material_vertex_attributes, errorlog, is_vertex_merge_allowed):
    # Cache the Blender states we are going to change
    prev_obj = bpy.context.view_layer.objects.active
    
    # What about vertex merging?
    if idx is None:
        meshobj_name = mesh_name
    else:
        meshobj_name = f"{mesh_name}_{idx}"
    bpy_mesh = bpy.data.meshes.new(name=meshobj_name)
    bpy_mesh_object = bpy.data.objects.new(meshobj_name, bpy_mesh)
    
    # Merge vertices if requested
    new_verts, new_tris, new_facevert_to_old_facevert_map = merge_vertices(
        mesh.vertices, 
        [(a, b, c) for a, b, c in zip(mesh.indices[0::3], mesh.indices[1::3], mesh.indices[2::3])], 
        is_vertex_merge_allowed,
        errorlog
    )
    
    # Generate geometry
    positions = [v.position for v in new_verts]
    bpy_mesh_object.data.from_pydata(positions, [], new_tris)
    bpy.context.collection.objects.link(bpy_mesh_object)
    
    bpy.context.view_layer.objects.active = bpy_mesh_object

    # Generate loop data
    loop_data, bpy_vert_to_gfs_verts = facevert_to_loop_lookup(new_facevert_to_old_facevert_map, bpy_mesh, mesh)

    # Create UVs
    add_uv_map(bpy_mesh, [v.texcoord0 for v in loop_data], make_uv_map_name(0))
    add_uv_map(bpy_mesh, [v.texcoord1 for v in loop_data], make_uv_map_name(1))
    add_uv_map(bpy_mesh, [v.texcoord2 for v in loop_data], make_uv_map_name(2))
    add_uv_map(bpy_mesh, [v.texcoord3 for v in loop_data], make_uv_map_name(3))
    add_uv_map(bpy_mesh, [v.texcoord4 for v in loop_data], make_uv_map_name(4))
    add_uv_map(bpy_mesh, [v.texcoord5 for v in loop_data], make_uv_map_name(5))
    add_uv_map(bpy_mesh, [v.texcoord6 for v in loop_data], make_uv_map_name(6))
    add_uv_map(bpy_mesh, [v.texcoord7 for v in loop_data], make_uv_map_name(7))

    # Create Vertex Colours
    add_color_map(bpy_mesh, [v.color1 for v in loop_data], make_color_map_name(0))
    add_color_map(bpy_mesh, [v.color2 for v in loop_data], make_color_map_name(1))

    # Rig
    if new_verts[0].indices is not None:
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
    # Remove this if you can get bone parenting to work.
    else:
        vertex_group = bpy_mesh_object.vertex_groups.new(name=parent_node_name)
        vertex_group.add([i for i in range(len(new_verts))], 1., 'REPLACE')

    # Assign normals
    if loop_data[0].normal is not None:
        # Works thanks to this stackexchange answer https://blender.stackexchange.com/a/75957
        # which a few of these comments below are also taken from
        # Do this LAST because it can remove some loops
        bpy_mesh.create_normals_split()
        for face in bpy_mesh.polygons:
            face.use_smooth = True  # loop normals have effect only if smooth shading ?
    
        # Set loop normals
        loop_normals = [l.normal for l in loop_data]
        bpy_mesh.loops.foreach_set("normal", [subitem for item in loop_normals for subitem in item])
    
        bpy_mesh.validate(clean_customdata=False)  # important to not remove loop normals here!
        bpy_mesh.update()
    
        clnors = array.array('f', [0.0] * (len(bpy_mesh.loops) * 3))
        bpy_mesh.loops.foreach_get("normal", clnors)
    
        bpy_mesh.polygons.foreach_set("use_smooth", [True] * len(bpy_mesh.polygons))
        # This line is pretty smart (came from the stackoverflow answer)
        # 1. Creates three copies of the same iterator over clnors
        # 2. Splats those three copies into a zip
        # 3. Each iteration of the zip now calls the iterator three times, meaning that three consecutive elements
        #    are popped off
        # 4. Turn that triplet into a tuple
        # In this way, a flat list is iterated over in triplets without wasting memory by copying the whole list
        bpy_mesh.normals_split_custom_set(tuple(zip(*(iter(clnors),) * 3)))
    
    bpy_mesh.use_auto_smooth = True
    
    ####################
    # SET THE MATERIAL #
    ####################
    if mesh.material_name is not None:
        active_material, gfs_material = materials.get(mesh.material_name)
        if active_material is not None:
            bpy_mesh.materials.append(active_material)
            bpy.data.objects[meshobj_name].active_material = active_material
            vas = material_vertex_attributes[mesh.material_name]
            
            vas.normals  .append(mesh.vertices[0].normal   is not None)
            vas.tangents .append(mesh.vertices[0].tangent  is not None)
            vas.binormals.append(mesh.vertices[0].binormal is not None)
            vas.color0s  .append(mesh.vertices[0].color1   is not None)
            vas.color1s  .append(mesh.vertices[0].color2   is not None)
            
            if mesh.vertices[0].tangent is not None:
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
        
    bpy_mesh.validate(verbose=True, clean_customdata=False)
    
    bpy_mesh.update()
    bpy_mesh.update()

    # Activate rigging
    modifier = bpy_mesh_object.modifiers.new(name="Armature", type="ARMATURE")
    modifier.object = armature
    
    
    #####################
    # IMPORT MORPH KEYS #
    #####################
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
    if len(mesh.morphs):
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
                            if (abs(di) > 0.001 and abs(pi) > 0.001) 
                            else (pi - di) > 0.001
                            for pi, di
                            in zip(avg_pos, delta)]):
                        raise ValueError("Invalid shapekey. Try importing without merging vertices.")
                        
                sk.data[bpy_vidx].co = [x1 + x2 for x1, x2 in zip(new_verts[bpy_vidx].position, vert_position_deltas[0])]
                
    ########################
    # DO THE LEFTOVER DATA #
    ########################
    bpy_mesh.GFSTOOLS_MeshProperties.flag_5   = mesh.flag_5
    bpy_mesh.GFSTOOLS_MeshProperties.flag_7   = mesh.flag_7
    bpy_mesh.GFSTOOLS_MeshProperties.flag_8   = mesh.flag_8
    bpy_mesh.GFSTOOLS_MeshProperties.flag_9   = mesh.flag_9
    bpy_mesh.GFSTOOLS_MeshProperties.flag_10  = mesh.flag_10
    bpy_mesh.GFSTOOLS_MeshProperties.flag_11  = mesh.flag_11
    bpy_mesh.GFSTOOLS_MeshProperties.flag_13  = mesh.flag_13
    bpy_mesh.GFSTOOLS_MeshProperties.flag_14  = mesh.flag_14
    bpy_mesh.GFSTOOLS_MeshProperties.flag_15  = mesh.flag_15
    bpy_mesh.GFSTOOLS_MeshProperties.flag_16  = mesh.flag_16
    bpy_mesh.GFSTOOLS_MeshProperties.flag_17  = mesh.flag_17
    bpy_mesh.GFSTOOLS_MeshProperties.flag_18  = mesh.flag_18
    bpy_mesh.GFSTOOLS_MeshProperties.flag_19  = mesh.flag_19
    bpy_mesh.GFSTOOLS_MeshProperties.flag_20  = mesh.flag_20
    bpy_mesh.GFSTOOLS_MeshProperties.flag_21  = mesh.flag_21
    bpy_mesh.GFSTOOLS_MeshProperties.flag_22  = mesh.flag_22
    bpy_mesh.GFSTOOLS_MeshProperties.flag_23  = mesh.flag_23
    bpy_mesh.GFSTOOLS_MeshProperties.flag_24  = mesh.flag_24
    bpy_mesh.GFSTOOLS_MeshProperties.flag_25  = mesh.flag_25
    bpy_mesh.GFSTOOLS_MeshProperties.flag_26  = mesh.flag_26
    bpy_mesh.GFSTOOLS_MeshProperties.flag_27  = mesh.flag_27
    bpy_mesh.GFSTOOLS_MeshProperties.flag_28  = mesh.flag_28
    bpy_mesh.GFSTOOLS_MeshProperties.flag_29  = mesh.flag_29
    bpy_mesh.GFSTOOLS_MeshProperties.flag_30  = mesh.flag_30
    bpy_mesh.GFSTOOLS_MeshProperties.flag_31  = mesh.flag_31

    
    bpy_mesh.GFSTOOLS_MeshProperties.unknown_0x12  = mesh.unknown_0x12
    if mesh.unknown_float_1 is not None and mesh.unknown_float_2 is not None:
        bpy_mesh.GFSTOOLS_MeshProperties.has_unknown_floats = True
        bpy_mesh.GFSTOOLS_MeshProperties.unknown_float_1  = mesh.unknown_float_1
        bpy_mesh.GFSTOOLS_MeshProperties.unknown_float_2  = mesh.unknown_float_2
    
    bpy_mesh.GFSTOOLS_MeshProperties.export_bounding_box    = mesh.keep_bounding_box
    bpy_mesh.GFSTOOLS_MeshProperties.export_bounding_sphere = mesh.keep_bounding_sphere
    
    bpy.context.view_layer.objects.active = prev_obj

    return bpy_mesh_object

def import_bounding_volumes(name, idx, mesh, bpy_bones, armature, bpy_bone, transform):
    # # Bounding box
    # bbox_verts = []
    # mx = mesh.bounding_box_max_dims
    # mn = mesh.bounding_box_min_dims
    # bbox_verts = [
    #     [mx[0], mx[1], mx[2]],
    #     [mx[0], mx[1], mn[2]],
    #     [mx[0], mn[1], mx[2]],
    #     [mx[0], mn[1], mn[2]],
    #     [mn[0], mn[1], mn[2]],
    #     [mn[0], mn[1], mx[2]],
    #     [mn[0], mx[1], mn[2]],
    #     [mn[0], mx[1], mx[2]]
    # ]
    # bbox_indices = [
    #     [0, 1, 2],
    #     [1, 3, 2],
    #     [3, 1, 4],
    #     [1, 6, 4],
    #     [4, 5, 6],
    #     [5, 7, 6],
    #     [1, 0, 6],
    #     [0, 7, 6],
    #     [2, 0, 5],
    #     [0, 5, 7],
    #     [2, 3, 5],
    #     [3, 4, 5]
    # ]
    # bpy_bbox = bpy.data.meshes.new(name=meshobj_name + "_bbox")
    # bpy_bbox_object = bpy.data.objects.new(meshobj_name + "_bbox", bpy_bbox)
    
    # bpy.context.view_layer.objects.active = bpy_bbox_object
    # bpy_bbox_object.data.from_pydata(bbox_verts, [], bbox_indices)
    # bpy.context.collection.objects.link(bpy_bbox_object)
    
    # constraint = bpy_bbox_object.constraints.new("CHILD_OF")
    # constraint.target = armature
    # constraint.subtarget = bpy_bone.name
    
    # # Bounding sphere
    # # Create an empty mesh and the object.
    # bpy_bsph = bpy.data.meshes.new(meshobj_name + "_bsphere")
    # bpy_bsph_object = bpy.data.objects.new(meshobj_name + "_bsphere", bpy_bsph)
    
    # # Add the object into the scene.
    # bpy.context.collection.objects.link(bpy_bsph_object)
    
    # # Select the newly created object
    # bpy.context.view_layer.objects.active = bpy_bsph_object
    # bpy_bsph_object.select_set(True)
    
    # # Construct the bmesh sphere and assign it to the blender mesh.
    # bm = bmesh.new()
    # bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=mesh.bounding_sphere_radius/2)
    # bm.to_mesh(bpy_bsph)
    # bm.free()
    
    # transform = Matrix([
    #     [1., 0., 0., mesh.bounding_sphere_centre[0]],
    #     [0., 1., 0., mesh.bounding_sphere_centre[1]],
    #     [0., 0., 1., mesh.bounding_sphere_centre[2]],
    #     [0., 0., 0., 1]
    # ])
    # bpy_bsph.transform(transform)
    
    # bpy.ops.object.shade_smooth()
    # bpy_bsph_object.select_set(False)
        
    # constraint = bpy_bsph_object.constraints.new("CHILD_OF")
    # constraint.target = armature
    # constraint.subtarget = bpy_bone.name
    
    pass
        
def add_uv_map(bpy_mesh, texcoords, name):
    if texcoords[0] is not None:
        uv_layer = bpy_mesh.uv_layers.new(name=name, do_init=True)
        for loop_idx, loop in enumerate(bpy_mesh.loops):
            uv_layer.data[loop_idx].uv = texcoords[loop_idx]

def unpack_colour(colour):
    # ARGB -> RGBA
    return [colour[1]/255, colour[2]/255, colour[3]/255, colour[0]/255]

def add_color_map(bpy_mesh, color_data, name):
    if color_data[0] is not None:
        # Blender 3.2+ 
        # vertex_colors is equivalent to color_attributes.new(name=name, type="BYTE_COLOR", domain="CORNER").
        # Original data is just uint8s so this is accurate.
        if hasattr(bpy_mesh, "color_attributes"):
            ca = bpy_mesh.color_attributes.new(name=name, type="BYTE_COLOR", domain="CORNER")
            for loop_idx, loop in enumerate(bpy_mesh.loops):
                ca.data[loop_idx].color = unpack_colour(color_data[loop_idx])
        # Blender 2.81-3.2
        else:
            vc = bpy_mesh.vertex_colors.new(name=name)
            for loop_idx, loop in enumerate(bpy_mesh.loops):
                vc.data[loop_idx].color = unpack_colour(color_data[loop_idx])


def import_camera(name, i, camera, armature, bpy_node_names):
    bpy_camera = bpy.data.cameras.new(f"{name}_{i}")
    
    # Import attributes
    bpy_camera.type       = "PERSP"
    bpy_camera.clip_start = camera.binary.zNear
    bpy_camera.clip_end   = camera.binary.zFar
    bpy_camera.lens_unit  = "FOV"
    bpy_camera.lens       = camera.binary.fov # Need to compare with camera sensor
    
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
