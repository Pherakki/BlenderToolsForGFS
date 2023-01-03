import array

import bpy
from mathutils import Matrix, Vector

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
        import_pinned_mesh("mesh", i, mesh, bpy_nodes, bpy_node_names, pinned_armatures[mesh.node], bpy_nodes[mesh.node], bone_transforms[mesh.node])
    
    # Reset state
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = initial_obj

    return main_armature, bone_transforms


def import_pinned_armature(node_idx, armature_index_set, name, main_armature, bpy_node_names, bone_transforms):
    # Order the bone indices we intend to import
    armature_index_set = sorted(armature_index_set)
    
    # Create armature
    armature_name = f"{name}_{bpy_node_names[node_idx]}_armature"
    armature = bpy.data.objects.new(armature_name, bpy.data.armatures.new(armature_name))
    bpy.context.collection.objects.link(armature)
    
    # Parent the pinned armature to the main armature
    armature.parent = main_armature
    armature.parent_type = "BONE"
    armature.parent_bone = bpy_node_names[node_idx]
    
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
    

def import_pinned_mesh(name, idx, mesh, bpy_nodes, bpy_node_names, armature, bpy_node, transform):
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
    #bpy_mesh.transform(armature.matrix_local)
    
    bpy_mesh.update()
    bpy_mesh.update()
    
    # Activate rigging
    #bpy_mesh.transform(transform)
    bpy_mesh_object.parent = armature
    modifier = bpy_mesh_object.modifiers.new(name="Armature", type="ARMATURE")
    modifier.object = armature
    
    bpy.context.view_layer.objects.active = armature


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
