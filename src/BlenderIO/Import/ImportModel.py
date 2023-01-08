import array

import bpy
from mathutils import Matrix, Vector, Quaternion

from .Utils.BoneConstruction import mat3_to_vec_roll, construct_bone


def import_pincushion_model(gfs, name):
    initial_obj = bpy.context.view_layer.objects.active

    armature_name = f"{name}_armature"
    main_armature = bpy.data.objects.new(armature_name, bpy.data.armatures.new(armature_name))
    bpy.context.collection.objects.link(main_armature)
    bpy.context.view_layer.objects.active = main_armature
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy_node_names  = [None]*len(gfs.bones)
    bpy_nodes       = [None]*len(gfs.bones)
    bone_transforms = [None]*len(gfs.bones)
    for i, node in enumerate(gfs.bones):
        matrix = node.bind_pose_matrix
        matrix = Matrix([matrix[0:4], matrix[4:8], matrix[8:12], [0., 0., 0., 1.]])

        bpy_bone = construct_bone(node.name, main_armature, matrix, 10)
        if node.parent != -1:
            bpy_bone.parent  = bpy_nodes[node.parent] 
            
        bpy_node_names[i]  = node.name
        bpy_nodes[i]       = bpy_bone
        bone_transforms[i] = matrix
   
    bpy.context.view_layer.objects.active = main_armature
    bpy.ops.object.mode_set(mode="OBJECT")
    
    ###################
    # PUSH EXTRA DATA #
    ###################
    for node in gfs.bones:
        bpy_bone = main_armature.data.bones[node.name]
        bpy_bone.GFSTOOLS_BoneProperties.unknown_float = node.unknown_float
        
        for prop in node.properties:
            item = bpy_bone.GFSTOOLS_BoneProperties.properties.add()
            item.dname = prop.name.string
            if prop.type == 1:
                item.dtype = "UINT32"
                item.uint32_data = prop.data
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
    
    ######################################
    # CREATE PINNED ARMATURES FOR MESHES #
    ######################################
    armature_indices = {}
    for mesh in gfs.meshes:
        if mesh.node not in armature_indices:
            armature_indices[mesh.node] = set()
        armature_index_set = armature_indices[mesh.node]

        if mesh.vertices[0].indices is not None:
            for vert_idx, v in enumerate(mesh.vertices):
                for bone_idx, weight in zip(v.indices, v.weights):
                    if weight == 0.:
                        continue
                    armature_index_set.add(bone_idx)
             
    # Create all necessary pinned armatures
    pinned_armatures = {}       
    for node_idx, armature_index_set in armature_indices.items():
        pinned_armatures[node_idx] = import_pinned_armature(node_idx, armature_index_set, name, main_armature, bpy_node_names, bone_transforms)
        
    # Import meshes and armature-parent them to the relevant pinned armature
    for i, mesh in enumerate(gfs.meshes):
        import_pinned_mesh("mesh", i, mesh, bpy_nodes, bpy_node_names, main_armature, pinned_armatures[mesh.node], bpy_nodes[mesh.node], bone_transforms[mesh.node])
    
    # Import cameras
    for i, cam in enumerate(gfs.cameras):
        import_camera("camera", i, cam, main_armature, bpy_node_names)
    
    # Import lights
    for i, light in enumerate(gfs.lights):
        import_light("light", i, light, main_armature, bpy_node_names)
    
    # Reset state
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = initial_obj

    return main_armature, bone_transforms


def import_pinned_armature(node_idx, armature_index_set, name, main_armature, bpy_node_names, bone_transforms):
    # TODO: Enable this when implementing mesh->bone parenting
    # Enable this when ready, double-check that it causes no issues
    # if len(armature_index_set) == 0:
    #     return None
    
    # Order the bone indices we intend to import
    armature_index_set = sorted(armature_index_set)
    
    # Create armature
    armature_name = f"{name}_{bpy_node_names[node_idx]}_armature"
    armature = bpy.data.objects.new(armature_name, bpy.data.armatures.new(armature_name))
    bpy.context.collection.objects.link(armature)
    
    # Parent the pinned armature to the main armature
    # Probably works, but let's get the export working before messing about
    # with this
    # armature.parent = main_armature
    # armature.parent_type = "BONE"
    # armature.parent_bone = bpy_node_names[node_idx]
    constraint = armature.constraints.new("CHILD_OF")
    constraint.target = main_armature
    constraint.subtarget = bpy_node_names[node_idx]
    constraint.inverse_matrix = Matrix.Identity(4)
    
    # Cache the Blender states we are going to change
    before_armature_obj = bpy.context.view_layer.objects.active
    
    # Set up the armature for editing
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')

    # Construct all bones required by the pinned armature
    bone_names = []
    for idx in armature_index_set:
        matrix = bone_transforms[node_idx].inverted() @ bone_transforms[idx]
        # Since the bone transforms are currently all pos-rot matrices, this
        # step should be unnecessary
        # Keep it for now until the import is set in stone
        # This just bakes the scale of the matrix into the matrix positions
        pos, rot, scl = matrix.decompose()
        pos = Matrix.Diagonal([*scl, 1.]) @ Matrix.Translation(pos)
        matrix = pos @ rot.to_matrix().to_4x4()
        
        construct_bone(bpy_node_names[idx], armature, matrix, 10)
        bone_names.append(bpy_node_names[idx])
        
    # Set up the armature for adding constraints
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # "Pin" all bones to their counterparts in the main armature
    for pose_bone, ref_name in zip(armature.pose.bones, bone_names):
        constraint = pose_bone.constraints.new("COPY_TRANSFORMS")
        constraint.target = main_armature
        constraint.subtarget = ref_name
    
    # Restore Blender to the state it was in before the function call
    bpy.context.view_layer.objects.active = before_armature_obj
    
    return armature
    

def import_pinned_mesh(name, idx, mesh, bpy_nodes, bpy_node_names, main_armature, armature, bpy_node, transform):
    # Cache the Blender states we are going to change
    prev_obj = bpy.context.view_layer.objects.active
    
    # What about vertex merging?
    meshobj_name = f"{name}_{idx}"
    bpy_mesh = bpy.data.meshes.new(name=meshobj_name)
    bpy_mesh_object = bpy.data.objects.new(meshobj_name, bpy_mesh)
    
    # Generate geometry
    positions = [v.position for v in mesh.vertices]
    new_tris = [(a, b, c) for a, b, c in zip(mesh.indices[0::3], mesh.indices[1::3], mesh.indices[2::3])]
    bpy_mesh_object.data.from_pydata(positions, [], new_tris)
    bpy.context.collection.objects.link(bpy_mesh_object)
    
    bpy.context.view_layer.objects.active = bpy_mesh_object

    # Create UVs
    add_uv_map(bpy_mesh, [v.texcoord0 for v in mesh.vertices], "UV0")
    add_uv_map(bpy_mesh, [v.texcoord1 for v in mesh.vertices], "UV1")
    add_uv_map(bpy_mesh, [v.texcoord2 for v in mesh.vertices], "UV2")
    add_uv_map(bpy_mesh, [v.texcoord3 for v in mesh.vertices], "UV3")
    add_uv_map(bpy_mesh, [v.texcoord4 for v in mesh.vertices], "UV4")
    add_uv_map(bpy_mesh, [v.texcoord5 for v in mesh.vertices], "UV5")
    add_uv_map(bpy_mesh, [v.texcoord6 for v in mesh.vertices], "UV6")
    add_uv_map(bpy_mesh, [v.texcoord7 for v in mesh.vertices], "UV7")

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
    active_material = bpy.data.materials[mesh.material_name]
    bpy_mesh.materials.append(active_material)
    bpy.data.objects[meshobj_name].active_material = active_material
    
    bpy_mesh.validate(verbose=True, clean_customdata=False)
    
    bpy_mesh.update()
    bpy_mesh.update()
    
    # Activate rigging
    # TODO: Enable this when implementing mesh->bone parenting
    # Enable this when ready, double-check that it causes no issues
    # if armature is None:
    #     bpy_mesh_object.parent = main_armature
    #     bpy_mesh_object.parent_type = "BONE"
    #     bpy_mesh_object.parent_bone = bpy_node_names[idx]
    # else:
    bpy_mesh_object.parent = armature
    modifier = bpy_mesh_object.modifiers.new(name="Armature", type="ARMATURE")
    modifier.object = armature
    
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
    bpy_camera.clip_start = camera.zNear
    bpy_camera.clip_end   = camera.zFar
    bpy_camera.angle      = camera.fov
    
    # Custom properties
    bpy.camera["unknown_0x50"] = camera.unknown_0x50
    bpy.camera["aspect_ratio"] = camera.aspect_ratio
    bpy.camera["unknown_0x50"] = camera.unknown_0x50
    
    bpy.camera["view_matrix_0"] = camera.view_matrix[ 0: 4]
    bpy.camera["view_matrix_1"] = camera.view_matrix[ 4: 8]
    bpy.camera["view_matrix_2"] = camera.view_matrix[ 8:12]
    bpy.camera["view_matrix_3"] = camera.view_matrix[12:16]

    # Link to the armature
    bpy_camera.parent = armature
    bpy_camera.parent_type = "BONE"
    bpy_camera.parent_bone = bpy_node_names[camera.node]

def import_light(name, i, light, armature, bpy_node_names):
    bpy_light = bpy.data.lights.new(f"{name}_{i}")
    
    # Custom properties
    bpy_light.GFSTOOLS_LightProperties.flag_0  = light.binary.flags.flag_0
    bpy_light.GFSTOOLS_LightProperties.unk_setting  = light.binary.flags.unk_setting
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
    bpy_light.GFSTOOLS_LightProperties.color_2 = light.binary.color_2
    bpy_light.GFSTOOLS_LightProperties.color_3 = light.binary.color_3
    
    if light.binary.unknown_0x28 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x28 = light.binary.unknown_0x28
    if light.binary.unknown_0x2C is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x2C = light.binary.unknown_0x2C
    if light.binary.unknown_0x30 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x30 = light.binary.unknown_0x30
    if light.binary.unknown_0x34 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x34 = light.binary.unknown_0x34
    if light.binary.unknown_0x38 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x38 = light.binary.unknown_0x38
    if light.binary.unknown_0x3C is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x3C = light.binary.unknown_0x3C
    if light.binary.unknown_0x40 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x40 = light.binary.unknown_0x40
    if light.binary.unknown_0x44 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x44 = light.binary.unknown_0x44
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
    if light.binary.unknown_0x74 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x74 = light.binary.unknown_0x74
    if light.binary.unknown_0x78 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x78 = light.binary.unknown_0x78
    if light.binary.unknown_0x7C is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x7C = light.binary.unknown_0x7C
    if light.binary.unknown_0x80 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x80 = light.binary.unknown_0x80
    if light.binary.unknown_0x84 is not None: bpy_light.GFSTOOLS_LightProperties.unknown_0x84 = light.binary.unknown_0x84
    
    # Link to the armature
    bpy_light.parent = armature
    bpy_light.parent_type = "BONE"
    bpy_light.parent_bone = bpy_node_names[light.node]
