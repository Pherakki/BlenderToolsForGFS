import array
import os
import math
import tempfile

import bpy
import bmesh
from bpy_extras.io_utils import ImportHelper
from mathutils import Matrix, Quaternion, Vector
import numpy as np

from ..FileFormats.GFS.GFSInterface import GFSInterface
from .Utils.ErrorPopup import handle_errors


def lerp(x, y, t):
    return (1-t)*x + t*y


def slerp(x, y, t):
    omega = np.arccos(np.dot(x, y))
    if omega == 0 or np.isnan(omega):
        return x
    term_1 = x * np.sin((1-t)*omega)
    term_2 = y * np.sin(t*omega)
    return (term_1 + term_2) / np.sin(omega)

def interpolate_keyframe_dict(frames, idx, interpolation_function, debug_output=False):
    frame_idxs = list(frames.keys())
    smaller_elements = [fidx for fidx in frame_idxs if idx >= fidx]
    next_smallest_frame = max(smaller_elements) if len(smaller_elements) else frame_idxs[0]
    larger_elements = [fidx for fidx in frame_idxs if idx <= fidx]
    next_largest_frame = min(larger_elements) if len(larger_elements) else frame_idxs[-1]

    if next_largest_frame == next_smallest_frame:
        t = 0  # Totally arbitrary, since the interpolation will be between two identical values
    else:
        t = (idx - next_smallest_frame) / (next_largest_frame - next_smallest_frame)

    min_value = frames[next_smallest_frame]
    max_value = frames[next_largest_frame]

    if debug_output:
        print(">>>", next_smallest_frame, idx, next_largest_frame)
        print(">>>", "t", t)
        print(">>>", min_value, max_value)

    return interpolation_function(np.array(min_value), np.array(max_value), t)

class TemporaryFile:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file_handle = None
    
    @property
    def filepath(self):
        return os.path.join(tempfile.gettempdir(),self.filename)
    
    def __enter__(self):
        self.file_handle = open(self.filepath, self.mode)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_handle.close()
        os.remove(self.filepath)
        
    def write(self, data):
        self.file_handle.write(data)


def vec_roll_to_mat3(vec, roll):
    """
    Code from
    https://blender.stackexchange.com/a/90240
    with minor edits:
        - Removed 'mathutils' prefix from Matrix classes
        - Fixed invalid operation in penultimate line: * -> @
    """
    #port of the updated C function from armature.c
    #https://developer.blender.org/T39470
    #note that C accesses columns first, so all matrix indices are swapped compared to the C version

    nor = vec.normalized()
    THETA_THRESHOLD_NEGY = 1.0e-9
    THETA_THRESHOLD_NEGY_CLOSE = 1.0e-5

    #create a 3x3 matrix
    bMatrix = Matrix().to_3x3()

    theta = 1.0 + nor[1];

    if (theta > THETA_THRESHOLD_NEGY_CLOSE) or ((nor[0] or nor[2]) and theta > THETA_THRESHOLD_NEGY):

        bMatrix[1][0] = -nor[0];
        bMatrix[0][1] = nor[0];
        bMatrix[1][1] = nor[1];
        bMatrix[2][1] = nor[2];
        bMatrix[1][2] = -nor[2];
        if theta > THETA_THRESHOLD_NEGY_CLOSE:
            #If nor is far enough from -Y, apply the general case.
            bMatrix[0][0] = 1 - nor[0] * nor[0] / theta;
            bMatrix[2][2] = 1 - nor[2] * nor[2] / theta;
            bMatrix[0][2] = bMatrix[2][0] = -nor[0] * nor[2] / theta;

        else:
            #If nor is too close to -Y, apply the special case.
            theta = nor[0] * nor[0] + nor[2] * nor[2];
            bMatrix[0][0] = (nor[0] + nor[2]) * (nor[0] - nor[2]) / -theta;
            bMatrix[2][2] = -bMatrix[0][0];
            bMatrix[0][2] = bMatrix[2][0] = 2.0 * nor[0] * nor[2] / theta;

    else:
        #If nor is -Y, simple symmetry by Z axis.
        bMatrix = Matrix().to_3x3()
        bMatrix[0][0] = bMatrix[1][1] = -1.0;

    #Make Roll matrix
    rMatrix = Matrix.Rotation(roll, 3, nor)

    #Combine and output result
    mat = rMatrix @ bMatrix
    return mat


def mat3_to_vec_roll(mat):
    """
    Code from
    https://blender.stackexchange.com/a/38337
    https://blender.stackexchange.com/a/90240
    """
    vec = mat.col[1]
    vecmat = vec_roll_to_mat3(mat.col[1], 0)
    vecmatinv = vecmat.inverted()
    rollmat = vecmatinv @ mat
    roll = math.atan2(rollmat[0][2], rollmat[2][2])
    return vec, roll



class ImportGFS(bpy.types.Operator, ImportHelper):
    bl_idname = 'import_file.import_gfs'
    bl_label = 'Persona 5 Royal - PC (.GMD)'
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = "*.GMD"


    # filter_glob: bpy.props.StringProperty(
    #                                          default="*.GMD",
    #                                          options={'HIDDEN'},
    #                                      )
    
    def import_file(self, context, filepath):
        bpy.ops.object.select_all(action='DESELECT')

        gfs = GFSInterface.from_file(filepath)
        
        textures  = import_textures(gfs)
        materials = import_materials(gfs, textures)
        armature  = import_pincushion_model(gfs, os.path.split(filepath)[1].split('.')[0])
        
        return {'FINISHED'}
    
    @handle_errors
    def execute(self, context):
        self.import_file(context, self.filepath)

        return {'FINISHED'}

def import_textures(gfs):
    textures = {}
    for tex in gfs.textures:
        filepath = os.path.join(bpy.app.tempdir, tex.name)
        # Try/finally seems to prevent a race condition between Blender and 
        # Python forming
        try:
            with open(filepath, 'wb') as F:
                F.write(tex.image_data)
            img = bpy.data.images.load(filepath)
            img.pack()
            img.filepath_raw = img.name
            
            # Assume for now that duplicate images use the first image
            # Should test this in-game
            if tex.name not in textures:
                textures[tex.name] = img
        finally:
            os.remove(filepath)
    return textures
    
def import_materials(gfs, textures):
    materials = {}

    # Load materials
    for mat in gfs.materials:
        bpy_material = bpy.data.materials.new(mat.name)
        materials[mat.name] = bpy_material
        
        bpy_material.use_nodes = True
        
        nodes = bpy_material.node_tree.nodes
        connect = bpy_material.node_tree.links.new
        bsdf_node = nodes.get('Principled BSDF')
        
        node = add_texture_to_material_node(bpy_material, "Diffuse Texture", mat.diffuse_texture)
        if node is not None:
            connect(node.outputs["Color"], bsdf_node.inputs["Base Color"])
        
        add_texture_to_material_node(bpy_material, "Normal Texture", mat.normal_texture)
        add_texture_to_material_node(bpy_material, "Specular Texture", mat.specular_texture)
        add_texture_to_material_node(bpy_material, "Reflection Texture", mat.reflection_texture)
        add_texture_to_material_node(bpy_material, "Highlight Texture", mat.highlight_texture)
        add_texture_to_material_node(bpy_material, "Glow Texture", mat.glow_texture)
        add_texture_to_material_node(bpy_material, "Night Texture", mat.night_texture)
        add_texture_to_material_node(bpy_material, "Detail Texture", mat.detail_texture)
        add_texture_to_material_node(bpy_material, "Shadow Texture", mat.shadow_texture)     

    return materials

def add_texture_to_material_node(bpy_material, name, texture):
    nodes = bpy_material.node_tree.nodes
    if texture is not None:
        node = nodes.new('ShaderNodeTexImage')
        node.name = name
        node.label = name
        node.image = bpy.data.images[texture.name.string]
        
        #bpy_material[name] = texture.unknowns
        
        return node
    return None


def import_pincushion_model(gfs, name):
    initial_obj = bpy.context.view_layer.objects.active
    
    # bpy_nodes       = [None]*len(gfs.bones)
    # bone_transforms = [None]*len(gfs.bones)
    # for i, node in enumerate(gfs.bones):
    #     bpy_node = bpy.data.objects.new(node.name, None)
    #     bpy.context.scene.collection.objects.link(bpy_node)
    #     bpy_node.empty_display_size = 2
    #     bpy_node.empty_display_type = 'ARROWS'  
    #     if node.parent != -1:
    #         bpy_node.parent = bpy_nodes[node.parent]
        
    #     bpy_node.scale = node.scale
    #     bpy_node.rotation_mode = "QUATERNION"
    #     bpy_node.rotation_quaternion = Quaternion([node.rotation[3], *node.rotation[0:3]])
    #     bpy_node.location = node.position
        
    #     bpy_nodes[i] = bpy_node
        
    #     if node.parent != -1:
    #         bpy_node.parent = bpy_nodes[node.parent]
    #         parent_transform = bone_transforms[node.parent]
    #     else:
    #         parent_transform = Matrix([
    #             [1., 0.,  0., 0.],
    #             [0., 0., -1., 0.],
    #             [0., 1.,  0., 0.],
    #             [0., 0.,  0., 1.]
    #         ])
    
    armature_name = "Armature"
    main_armature = bpy.data.objects.new(armature_name, bpy.data.armatures.new(armature_name))
    bpy.context.collection.objects.link(main_armature)
    bpy.context.view_layer.objects.active = main_armature
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy_node_names  = [None]*len(gfs.bones)
    bpy_nodes       = [None]*len(gfs.bones)
    bone_transforms = [None]*len(gfs.bones)
    for i, node in enumerate(gfs.bones):
        bpy_bone = main_armature.data.edit_bones.new(node.name)
        if node.parent != -1:
            bpy_bone.parent  = bpy_nodes[node.parent]

        matrix = node.bind_pose_matrix
        matrix = Matrix([matrix[0:4], matrix[4:8], matrix[8:12], [0., 0., 0., 1.]])

        tail, roll = mat3_to_vec_roll(matrix.to_3x3())
        tail *= 10  # Make this scale with the model size in the future, for convenience
        
        bpy_bone.head = Vector([0., 0., 0.])
        bpy_bone.tail = Vector([0., 10., 0.])
        
        pos_vector = matrix.to_translation()
        bpy_bone.head = pos_vector
        bpy_bone.tail = pos_vector + tail
        bpy_bone.roll = roll
        
        bpy_node_names[i]  = node.name
        bpy_nodes[i]       = bpy_bone
        bone_transforms[i] = matrix
   
    bpy.context.view_layer.objects.active = main_armature
    bpy.ops.object.mode_set(mode="OBJECT")
    
    armatures = {}
    armature_maps = {}
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
                    
    for node_idx, armature_index_set in armature_indices.items():
        armature_index_set = sorted(armature_index_set)
        
        armature_name = f"{bpy_node_names[node_idx]}_armature"
        armature = bpy.data.objects.new(armature_name, bpy.data.armatures.new(armature_name))
        bpy.context.collection.objects.link(armature)
        # armature.parent = bpy_nodes[node_idx]
        
        constraint = armature.constraints.new("CHILD_OF")
        constraint.target = main_armature
        constraint.subtarget = bpy_node_names[node_idx]
        
        before_armature_obj = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
    
        #bone_nodes = []
        bone_names = []
        for idx in armature_index_set:
            #ref_node = bpy_nodes[idx]
            bpy_bone = armature.data.edit_bones.new(bpy_node_names[idx])

            matrix = bone_transforms[node_idx].inverted() @ bone_transforms[idx]
            
            pos, rot, scl = matrix.decompose()
            pos = Matrix.Diagonal([*scl, 1.]) @ Matrix.Translation(pos)
            matrix = pos @ rot.to_matrix().to_4x4()
            
            tail, roll = mat3_to_vec_roll(matrix.to_3x3())
            tail *= 10  # Make this scale with the model size in the future, for convenience
            
            pos_vector = matrix.to_translation()
            bpy_bone.head = pos_vector
            bpy_bone.tail = pos_vector + tail
            bpy_bone.roll = roll
            
            #bone_nodes.append(ref_node)
            bone_names.append(bpy_node_names[idx])
            
            
        bpy.ops.object.mode_set(mode='OBJECT')
        
        for pose_bone, ref_name in zip(armature.pose.bones, bone_names):
            constraint = pose_bone.constraints.new("COPY_TRANSFORMS")
            constraint.target = main_armature
            constraint.subtarget = ref_name
            
        bpy.context.view_layer.objects.active = before_armature_obj
        armatures[node_idx] = armature
        armature_maps[node_idx] = {bone_idx: i_bone_idx for i_bone_idx, bone_idx in enumerate(armature_index_set)}
        
        
    for i, mesh in enumerate(gfs.meshes):
        import_pinned_mesh("mesh", i, mesh, bpy_nodes, bpy_node_names, armatures[mesh.node], bpy_nodes[mesh.node], bone_transforms[mesh.node])
        
    bpy.ops.object.mode_set(mode='OBJECT')
        
    # Reset state
    bpy.context.view_layer.objects.active = initial_obj

    return main_armature



def import_pinned_mesh(name, idx, mesh, bpy_nodes, bpy_node_names, armature, bpy_node, transform):
    # What about vertex merging?
    meshobj_name = f"{name}_{idx}"
    bpy_mesh = bpy.data.meshes.new(name=meshobj_name)
    bpy_mesh_object = bpy.data.objects.new(meshobj_name, bpy_mesh)
    
    bpy.context.view_layer.objects.active = bpy_mesh_object
    
    # Generate geometry
    positions = [v.position for v in mesh.vertices]
    new_tris = [(a, b, c) for a, b, c in zip(mesh.indices[0::3], mesh.indices[1::3], mesh.indices[2::3])]
    bpy_mesh_object.data.from_pydata(positions, [], new_tris)
    bpy.context.collection.objects.link(bpy_mesh_object)

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
        

def import_model(gfs, name):
    initial_obj = bpy.context.view_layer.objects.active
    # Load bones
    armature_name = "Armature"
    armature = bpy.data.objects.new(armature_name, bpy.data.armatures.new(armature_name))
    bpy.context.collection.objects.link(armature)
    bpy.context.view_layer.objects.active = armature
    
    bpy.ops.object.mode_set(mode='EDIT')
    list_of_bones = [None for _ in range(len(gfs.bones))]
    bone_transforms = [None for _ in range(len(gfs.bones))]
    for i, node in enumerate(gfs.bones):
        bpy_bone = armature.data.edit_bones.new(node.name)
        if node.parent != -1:
            bpy_bone.parent = list_of_bones[node.parent]
            parent_transform = bone_transforms[node.parent]
        else:
            parent_transform = Matrix([
                [1., 0.,  0., 0.],
                [0., 0., -1., 0.],
                [0., 1.,  0., 0.],
                [0., 0.,  0., 1.]
            ])
            
        
        position = Matrix.Translation(node.position)
        rotation = Quaternion([node.rotation[3], *node.rotation[0:3]]).to_matrix().to_4x4()
        scale = Matrix.Diagonal([*node.scale, 1])
        
        matrix = parent_transform @ (position @ rotation @ scale)

    
        tail, roll = mat3_to_vec_roll(matrix.to_3x3())
        tail *= 10  # Make this scale with the model size in the future, for convenience
        
        bpy_bone.head = Vector([0., 0., 0.])
        bpy_bone.tail = Vector([0., 10., 0.])
        
        # pos_vector = matrix.to_translation()
        # bpy_bone.head = pos_vector
        # bpy_bone.tail = pos_vector + tail
        # bpy_bone.roll = roll
        
        list_of_bones[i] = bpy_bone
        bone_transforms[i] = matrix
        
    for i, mesh in enumerate(gfs.meshes):
        import_mesh("mesh", i, mesh, list_of_bones, armature, list_of_bones[mesh.node], bone_transforms[mesh.node])
        
    # Cameras, Lights, EPL...
        
    bpy.ops.object.mode_set(mode='OBJECT')
        
    # Reset state
    bpy.context.view_layer.objects.active = initial_obj
    
    return armature


def import_mesh(name, idx, mesh, bpy_bones, armature, bpy_bone, transform):
    # What about vertex merging?
    meshobj_name = f"{name}_{idx}"
    bpy_mesh = bpy.data.meshes.new(name=meshobj_name)
    bpy_mesh_object = bpy.data.objects.new(meshobj_name, bpy_mesh)
    
    bpy.context.view_layer.objects.active = bpy_mesh_object
    
    # Generate geometry
    positions = [v.position for v in mesh.vertices]
    new_tris = [(a, b, c) for a, b, c in zip(mesh.indices[0::3], mesh.indices[1::3], mesh.indices[2::3])]
    bpy_mesh_object.data.from_pydata(positions, [], new_tris)
    bpy.context.collection.objects.link(bpy_mesh_object)

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
            vertex_group = bpy_mesh_object.vertex_groups.new(name=bpy_bones[bone_idx].name)
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
    bpy_mesh_object.parent = armature
    modifier = bpy_mesh_object.modifiers.new(name="Armature", type="ARMATURE")
    modifier.object = armature
    
    bpy_mesh_object.data.transform(transform)
    
    # constraint = bpy_mesh_object.constraints.new("CHILD_OF")
    # constraint.target = armature
    # constraint.subtarget = bpy_bone.name
    
    
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
    
    bpy.context.view_layer.objects.active = armature
        
def add_uv_map(bpy_mesh, texcoords, name):
    if texcoords[0] is not None:
        uv_layer = bpy_mesh.uv_layers.new(name=name, do_init=True)
        for loop_idx, loop in enumerate(bpy_mesh.loops):
            uv_layer.data[loop_idx].uv = texcoords[loop.vertex_index]

def import_animations(gfs, model_gfs, armature):
    print(">> DOING ANIMS", len(gfs.animations))
    prev_obj = bpy.context.view_layer.objects.active

    armature.animation_data_create()
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode="POSE")
    
    for anim_idx, anim in enumerate(gfs.animations):
        track_name = f"AF0001_020_{anim_idx}"
        action = bpy.data.actions.new(track_name)

        track_database = {track.name: track for track in anim.tracks}
        # Base action
        for node in model_gfs.bones:
            bone_name = node.name
            
            actiongroup = action.groups.new(bone_name)


            position = Matrix.Translation(node.position)
            rotation = Quaternion([node.rotation[3], *node.rotation[0:3]]).to_matrix().to_4x4()
            scale = Matrix.Diagonal([*node.scale, 1])
            base_matrix = position @ rotation @ scale
            
            if node.name not in track_database:
                continue
            data_track = track_database[node.name]
            
            fps = 30
            
            frames = sorted(set([
                *list(data_track.rotations.keys()),
                *list(data_track.positions.keys()),
                *list(data_track.scales.keys())
            ]))
            
            # Get rotations
            if node.name in track_database:
                rotations = {k: v for k, v in track_database[node.name].rotations.items()}
                
                base_pos  = track_database[node.name].base_position
                positions = {k: [bv*bp for bv, bp in zip(v, base_pos)] for k, v in track_database[node.name].positions.items()}
                
                base_scale = track_database[node.name].base_scale
                scales = {k: [bv*bp for bv, bp in zip(v, base_scale)] for k, v in track_database[node.name].scales.items()}
                
                if len(rotations) == 0:
                    rotations = {0: [0., 0., 0., 1.]}
                if len(positions) == 0:
                    positions = {0: [0., 0., 0.]}
                if len(scales) == 0:
                    scales = {0: [1., 1., 1.]}
            else:
                rotations = {0: [0., 0., 0., 1.]}
                positions = {0: [0., 0., 0.]}
                scales    = {0: [1., 1., 1.]}
            
            # Now interpolate...
            for frame in frames:
                if frame not in rotations:
                    rotations[frame] = interpolate_keyframe_dict(rotations, frame, slerp)
                if frame not in positions:
                    positions[frame] = interpolate_keyframe_dict(positions, frame, lerp)
                if frame not in scales:
                    scales[frame] = interpolate_keyframe_dict(scales, frame, lerp)
            
            # Now create transform matrices...
            o_rotations = {}
            o_positions = {}
            o_scales    = {}
            for i in frames:
                pos_mat = Matrix.Translation(positions[i])
                rot_mat = Quaternion([rotations[i][3], *rotations[i][0:3]]).to_matrix().to_4x4()
                scl_mat = Matrix.Diagonal([*scales[i], 1])
                transform = base_matrix.inverted() @ (pos_mat @ rot_mat @ scl_mat)
                pos, rot, scl = transform.decompose()
                
                o_rotations[i] = [rot.x, rot.y, rot.z, rot.w]
                o_positions[i] = [pos.x, pos.y, pos.z]
                o_scales[i]    = [scl.x, scl.y, scl.z]
              
            rotations = o_rotations
            positions = o_positions
            scales = o_scales
              
            # Create animations
            if len(rotations) != 0:
                fcs = []
                for i, quat_idx in enumerate([3, 0, 1, 2]):
                    fc = action.fcurves.new(f'pose.bones["{bone_name}"].rotation_quaternion', index=i)
                    fc.keyframe_points.add(count=len(rotations))
                    fc.keyframe_points.foreach_set("co",
                                                   [x for co in zip([float(fps*elem + 1) for elem in rotations.keys()],
                                                                    [elem[quat_idx] for elem in rotations.values()]) for x in
                                                    co])
                    fc.group = actiongroup
                    fc.lock = True
                    fcs.append(fc)
                for fc in fcs:
                    fc.update()
                for fc in fcs:
                    fc.lock = False
                    

            if len(positions) != 0:
                fcs = []
                for i in range(3):
                    fc = action.fcurves.new(f'pose.bones["{bone_name}"].location', index=i)
                    fc.keyframe_points.add(count=len(positions))
                    fc.keyframe_points.foreach_set("co",
                                                    [x for co in zip([float(fps*elem + 1) for elem in positions.keys()],
                                                                    [elem[i] for elem in positions.values()]) for x in
                                                    co])
                    fc.group = actiongroup
                    for k in fc.keyframe_points:
                        k.interpolation = "LINEAR"
                    fc.lock = True
                    fcs.append(fc)
                for fc in fcs:
                    fc.update()
                for fc in fcs:
                    fc.lock = False
                    

            if len(scales) != 0:
                fcs = []
                for i in range(3):
                    fc = action.fcurves.new(f'pose.bones["{bone_name}"].scale', index=i)
                    fc.keyframe_points.add(count=len(scales))
                    fc.keyframe_points.foreach_set("co",
                                                   [x for co in zip([float(fps*elem + 1) for elem in scales.keys()],
                                                                    [elem[i] for elem in scales.values()]) for x in
                                                    co])
                    fc.group = actiongroup
                    for k in fc.keyframe_points:
                        k.interpolation = "LINEAR"
                    fc.lock = True
                    fcs.append(fc)
                for fc in fcs:
                    fc.update()
                for fc in fcs:
                    fc.lock = False

        armature.animation_data.action = action
        track = armature.animation_data.nla_tracks.new()
        track.name = track_name
        track.mute = True
        nla_strip = track.strips.new(action.name, action.frame_range[0], action)
        #nla_strip.scale = 24 / animation_data.playback_rate
        #nla_strip.blend_type = "COMBINE"
        armature.animation_data.action = None
        
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.objects.active = prev_obj
