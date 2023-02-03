import array
import math

import bpy
from mathutils import Matrix, Vector, Quaternion

from ..Utils.UVMapManagement import make_uv_map_name
from .Utils.BoneConstruction import mat3_to_vec_roll, construct_bone


def import_model(gfs, name):
    initial_obj = bpy.context.view_layer.objects.active

    armature_name = name
    main_armature = bpy.data.objects.new(armature_name, bpy.data.armatures.new(armature_name))
    bpy.context.collection.objects.link(main_armature)
    bpy.context.view_layer.objects.active = main_armature
    
    main_armature.data.GFSTOOLS_ModelProperties.root_node_name = gfs.bones[0].name if len(gfs.bones) else ""
    main_armature.data.GFSTOOLS_ModelProperties.has_external_emt = gfs.data_0x000100F8 is not None
    main_armature.data.GFSTOOLS_ModelProperties.export_bounding_box = gfs.keep_bounding_box
    main_armature.data.GFSTOOLS_ModelProperties.export_bounding_sphere = gfs.keep_bounding_sphere
    main_armature.data.GFSTOOLS_ModelProperties.flag_3 = gfs.flag_3
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy_node_names  = [None]*len(gfs.bones)
    bpy_nodes       = [None]*len(gfs.bones)
    bone_transforms = [None]*len(gfs.bones)
    
    nodes_with_meshes = set()
    for mesh in gfs.meshes:
        nodes_with_meshes.add(mesh.node)
    
    rigged_bones, unrigged_bones = filter_rigging_bones_and_ancestors(gfs)

    meshes_to_rename         = set.intersection(rigged_bones,   nodes_with_meshes)
    bones_to_ignore          = set.intersection(unrigged_bones, nodes_with_meshes)
    unrigged_bones_to_import = set.difference(unrigged_bones, bones_to_ignore)
        
    # Get rid of root node
    bones_to_ignore.add(0)

    gfs_to_bpy_bone_map = {}
    bpy_bone_counter = 0
    # upY_to_upZ_matrix = Matrix([[ 1.,  0.,  0.,  0.],
    #                             [ 0.,  0., -1.,  0.],
    #                             [ 0.,  1.,  0.,  0.],
    #                             [ 0.,  0.,  0.,  1.]])
    for i, node in enumerate(gfs.bones):
        matrix = node.bind_pose_matrix
        matrix = Matrix([matrix[0:4], matrix[4:8], matrix[8:12], [0., 0., 0., 1.]])

        if i not in bones_to_ignore:            
            bpy_bone = construct_bone(node.name, main_armature, matrix, 10)
            if node.parent_idx > -1:
                bpy_bone.parent = bpy_nodes[node.parent_idx] 
            bpy_nodes[i]           = bpy_bone
            gfs_to_bpy_bone_map[i] = bpy_bone_counter
            bpy_bone_counter      += 1
            
        bpy_node_names[i]  = node.name
        bone_transforms[i] = matrix

    bpy.ops.object.mode_set(mode="OBJECT")

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
    for i, node in enumerate(gfs.bones):
        if i in bones_to_ignore:
            continue
        
        bpy_bone = main_armature.data.bones[node.name]
        bpy_bone.GFSTOOLS_BoneProperties.unknown_float = node.unknown_float
        
        for prop in node.properties:
            item = bpy_bone.GFSTOOLS_BoneProperties.properties.add()
            item.dname = prop.name
            if prop.type == 1:
                item.dtype = "INT32"
                item.int32_data = prop.data
            elif prop.type == 2:
                item.dtype = "FLOAT32"
                item.float32_data = prop.data
            elif prop.type == 3:
                item.dtype = "UINT8"
                item.uint8_data = prop.data
            elif prop.type == 4:
                item.dtype = "STRING"
                item.string_data = prop.data   
            elif prop.type == 5:
                item.dtype = "UINT8VEC3"
                item.uint8vec3_data = prop.data  
            elif prop.type == 6:
                item.dtype = "UINT8VEC4"
                item.uint8vec4_data = prop.data
            elif prop.type == 7:
                item.dtype = "FLOAT32VEC3"
                item.float32vec3_data = prop.data
            elif prop.type == 8:
                item.dtype = "FLOAT32VEC4"
                item.float32vec4_data = prop.data
            elif prop.type == 9:
                item.dtype = "BYTES"
                item.bytes_data = '0x' + ''.join(rf"{e:0>2X}" for e in prop.data)
    

    # Import meshes and parent them to the armature
    mesh_groups = {idx: [] for idx in sorted(set((mesh.node for mesh in gfs.meshes)))}
    for mesh in gfs.meshes:
        mesh_groups[mesh.node].append(mesh)
    for node_idx, meshes in mesh_groups.items():
        mesh_name = bpy_node_names[node_idx]
        if node_idx in meshes_to_rename:
            mesh_name += "_mesh"
        import_mesh_group(mesh_name, bpy_node_names[node_idx], i, meshes, bpy_node_names, main_armature, bone_transforms[node_idx])
    
    # Import cameras
    for i, cam in enumerate(gfs.cameras):
        import_camera("camera", i, cam, main_armature, bpy_node_names)
    
    # Import lights
    for i, light in enumerate(gfs.lights):
        import_light("light", i, light, main_armature, bpy_node_names)
    
    # Reset state
    bpy.ops.object.mode_set(mode='OBJECT')
    main_armature.rotation_euler = [math.pi/2, 0, 0]
    main_armature.rotation_quaternion = [.5**0.5, .5**.5, 0, 0]
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
    bones_to_check = sorted(used_indices)
    for bone_idx in bones_to_check:
        node = gfs.bones[bone_idx]
        while node.parent_idx != -1:
            used_indices.add(node.parent_idx)
            node = gfs.bones[node.parent_idx]
    
    unused_indices = set([i for i in range(len(gfs.bones))]).difference(used_indices)

    return used_indices, unused_indices


def import_mesh_group(mesh_name, parent_node_name, idx, meshes, bpy_node_names, armature, transform):
    bpy_mesh_object = import_mesh(mesh_name, parent_node_name, None, meshes[0], bpy_node_names, armature)

    bpy_mesh_object.parent = armature
    pos, quat, scale = transform.decompose()
    bpy_mesh_object.rotation_mode = "QUATERNION"
    bpy_mesh_object.location = pos
    bpy_mesh_object.rotation_quaternion = quat
    bpy_mesh_object.scale = scale

    for i, mesh in enumerate(meshes[1:]):
        child_bpy_mesh_object = import_mesh(mesh_name, parent_node_name, i, mesh, bpy_node_names, armature)
    
        child_bpy_mesh_object.parent = bpy_mesh_object
        child_bpy_mesh_object.rotation_mode = "QUATERNION"
        child_bpy_mesh_object.location = [0., 0., 0.]
        child_bpy_mesh_object.rotation_quaternion = [1., 0., 0., 0.]
        child_bpy_mesh_object.scale = [1, 1., 1.]
    
    
def import_mesh(mesh_name, parent_node_name, idx, mesh, bpy_node_names, armature):
    # Cache the Blender states we are going to change
    prev_obj = bpy.context.view_layer.objects.active
    
    # What about vertex merging?
    if idx is None:
        meshobj_name = mesh_name
    else:
        meshobj_name = f"{mesh_name}_{idx}"
    bpy_mesh = bpy.data.meshes.new(name=meshobj_name)
    bpy_mesh_object = bpy.data.objects.new(meshobj_name, bpy_mesh)
    
    # Generate geometry
    positions = [v.position for v in mesh.vertices]
    new_tris = [(a, b, c) for a, b, c in zip(mesh.indices[0::3], mesh.indices[1::3], mesh.indices[2::3])]
    bpy_mesh_object.data.from_pydata(positions, [], new_tris)
    bpy.context.collection.objects.link(bpy_mesh_object)
    
    bpy.context.view_layer.objects.active = bpy_mesh_object

    # Create UVs
    add_uv_map(bpy_mesh, [v.texcoord0 for v in mesh.vertices], make_uv_map_name(0))
    add_uv_map(bpy_mesh, [v.texcoord1 for v in mesh.vertices], make_uv_map_name(1))
    add_uv_map(bpy_mesh, [v.texcoord2 for v in mesh.vertices], make_uv_map_name(2))
    add_uv_map(bpy_mesh, [v.texcoord3 for v in mesh.vertices], make_uv_map_name(3))
    add_uv_map(bpy_mesh, [v.texcoord4 for v in mesh.vertices], make_uv_map_name(4))
    add_uv_map(bpy_mesh, [v.texcoord5 for v in mesh.vertices], make_uv_map_name(5))
    add_uv_map(bpy_mesh, [v.texcoord6 for v in mesh.vertices], make_uv_map_name(6))
    add_uv_map(bpy_mesh, [v.texcoord7 for v in mesh.vertices], make_uv_map_name(7))

    # Rig
    if mesh.vertices[0].indices is not None:
        groups = {}
        for vert_idx, v in enumerate(mesh.vertices):
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
        vertex_group.add([i for i in range(len(mesh.vertices))], 1., 'REPLACE')

    # Assign normals
    # Works thanks to this stackexchange answer https://blender.stackexchange.com/a/75957
    # which a few of these comments below are also taken from
    # Do this LAST because it can remove some loops
    bpy_mesh.create_normals_split()
    for face in bpy_mesh.polygons:
        face.use_smooth = True  # loop normals have effect only if smooth shading ?

    # Set loop normals
    loop_normals = [Vector(mesh.vertices[loop.vertex_index].normal) for loop in bpy_mesh.loops]
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
    
    # Set materials
    if mesh.material_name is not None:
        active_material = bpy.data.materials.get(mesh.material_name)
        if active_material is not None:
            bpy_mesh.materials.append(active_material)
            bpy.data.objects[meshobj_name].active_material = active_material
        else:
            raise NotImplementedError("This needs to be a ReportableWarning")
    
    bpy_mesh.validate(verbose=True, clean_customdata=False)
    
    bpy_mesh.update()
    bpy_mesh.update()

    # Activate rigging
    modifier = bpy_mesh_object.modifiers.new(name="Armature", type="ARMATURE")
    modifier.object = armature
    
    return bpy_mesh_object

    
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
    if len(mesh.vertices):
        bpy_mesh.GFSTOOLS_MeshProperties.export_normals   = mesh.vertices[0].normal   is not None
        bpy_mesh.GFSTOOLS_MeshProperties.export_tangents  = mesh.vertices[0].tangent  is not None
        bpy_mesh.GFSTOOLS_MeshProperties.export_binormals = mesh.vertices[0].binormal is not None
    
    bpy.context.view_layer.objects.active = prev_obj


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
            uv_layer.data[loop_idx].uv = texcoords[loop.vertex_index]

def import_camera(name, i, camera, armature, bpy_node_names):
    bpy_camera = bpy.data.cameras.new(f"{name}_{i}")
    
    # Import attributes
    bpy_camera.type       = "PERSP"
    bpy_camera.clip_start = camera.binary.zNear
    bpy_camera.clip_end   = camera.binary.zFar
    bpy_camera.lens_unit  = "FOV"
    bpy_camera.lens       = camera.binary.fov # Need to compare with camera sensor
    
    # Custom properties
    bpy_camera["aspect_ratio"] = camera.binary.aspect_ratio # Can hook into Blender scene callback
    bpy_camera["unknown_0x50"] = camera.binary.unknown_0x50 # Always 0...

    # Create the object
    bpy_camera_object = bpy.data.objects.new(bpy_camera.name, bpy_camera)
    bpy.context.collection.objects.link(bpy_camera_object)

    # Link to the armature
    bpy_camera_object.parent = armature
    bpy_camera_object.parent_type = "BONE"
    bpy_camera_object.parent_bone = bpy_node_names[camera.node]
    bpy_camera_object.matrix_parent_inverse = Matrix.Translation([0., -10., 0.])
    
    # Set view matrix
    bpy_camera_object.matrix_local = Matrix([camera.binary.view_matrix[ 0: 4],
                                             camera.binary.view_matrix[ 4: 8],
                                             camera.binary.view_matrix[ 8:12],
                                             camera.binary.view_matrix[12:16]])


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

    # Link to the armature
    bpy_light_object.parent = armature
    bpy_light_object.parent_type = "BONE"
    bpy_light_object.parent_bone = bpy_node_names[light.node]
    bpy_light_object.matrix_parent_inverse = Matrix.Translation([0., -10., 0])
