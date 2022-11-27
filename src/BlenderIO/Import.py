import array
import os
import math

import bpy
from bpy_extras.io_utils import ImportHelper
from mathutils import Matrix, Quaternion, Vector

# Replace with GFSInterface when it's written
from ..FileFormats.GFS.GFSBinary import GFS0Binary


def vec_roll_to_mat3(vec, roll):
    """
    https://blender.stackexchange.com/a/38337
    """
    target = Vector((0, 0.1, 0))
    nor = vec.normalized()
    axis = target.cross(nor)
    if axis.dot(axis) > 10**-10:
        axis.normalize()
        theta = target.angle(nor)
        bMatrix = Matrix.Rotation(theta, 3, axis)
    else:
        updown = 1 if target.dot(nor) > 0 else -1
        bMatrix = Matrix.Scale(updown, 3)
        bMatrix[2][2] = 1.0

    rMatrix = Matrix.Rotation(roll, 3, nor)
    mat = rMatrix @ bMatrix
    return mat


def mat3_to_vec_roll(mat):
    """
    https://blender.stackexchange.com/a/38337
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


    filter_glob: bpy.props.StringProperty(
                                             default="*.GMD",
                                             options={'HIDDEN'},
                                         )
    
    def import_file(self, context, filepath):
        bpy.ops.object.select_all(action='DESELECT')

        gfs = GFS0Binary()
        gfs.read(filepath)
        
        texture_paths  = import_textures(gfs)
        material_names = import_materials(gfs)
        model          = import_model(gfs, os.path.split(filepath)[1].split('.')[0])
            
        return {'FINISHED'}
    
    #@handle_errors
    def execute(self, context):
        self.import_file(context, self.filepath)

        return {'FINISHED'}

def import_textures(gfs):
    texture_paths = []

    # Get container
    tex_ctr = None
    for ctr in gfs.containers:
        if ctr.type == 0x000100FC:
            tex_ctr = ctr
            break
    
    # Dump textures
    if tex_ctr is not None:
        os.makedirs("tex", exist_ok=True)
        for tex in ctr.data:
            with open("tex/" + tex.name, 'wb') as F:
                F.write(tex.data)
            texture_paths.append(os.getcwd() + "/tex/" + tex.name)
            bpy.data.images.load(os.getcwd() + "/tex/" + tex.name)
    return texture_paths
    
def import_materials(gfs):
    material_names = []

    # Get container
    mat_ctr = None
    for ctr in gfs.containers:
        if ctr.type == 0x000100FB:
            mat_ctr = ctr
            break
    
    # Load materials
    if mat_ctr is not None:
        for mat in ctr.data:
            bpy_material = bpy.data.materials.new(mat.name)
            material_names.append(bpy_material.name)
            
            bpy_material.use_nodes = True
            
            nodes = bpy_material.node_tree.nodes
            connect = bpy_material.node_tree.links.new
            bsdf_node = nodes.get('Principled BSDF')
            
            node = add_texture_to_material_node(nodes, "Diffuse Texture", mat.diffuse_texture)
            if node is not None:
                connect(node.outputs["Color"], bsdf_node.inputs["Base Color"])
            
            add_texture_to_material_node(nodes, "Normal Texture", mat.normal_texture)
            add_texture_to_material_node(nodes, "Specular Texture", mat.specular_texture)
            add_texture_to_material_node(nodes, "Reflection Texture", mat.reflection_texture)
            add_texture_to_material_node(nodes, "Highlight Texture", mat.highlight_texture)
            add_texture_to_material_node(nodes, "Glow Texture", mat.glow_texture)
            add_texture_to_material_node(nodes, "Night Texture", mat.night_texture)
            add_texture_to_material_node(nodes, "Detail Texture", mat.detail_texture)
            add_texture_to_material_node(nodes, "Shadow Texture", mat.shadow_texture)     

    return material_names

def add_texture_to_material_node(nodes, name, texture):
    if texture is not None:
        node = nodes.new('ShaderNodeTexImage')
        node.name = name
        node.label = name
        node.image = bpy.data.images[texture.name]
        return node
        
def import_model(gfs, name):
    material_names = []

    # Get container
    model_ctr = None
    for ctr in gfs.containers:
        if ctr.type == 0x00010003:
            model_ctr = ctr
            break
        
    # Load materials
    if model_ctr is not None:
        model = model_ctr.data
        armature_name = "Armature"
        armature = bpy.data.objects.new(armature_name, bpy.data.armatures.new(armature_name))
        bpy.context.collection.objects.link(armature)
        
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        list_of_bones = []
        meshes = []
        build_nodes(name, meshes, list_of_bones, -1, armature, model.nodes[0], Matrix.Identity(4))
        bpy.ops.object.mode_set(mode='OBJECT')


def build_nodes(name, meshes, list_of_bones, parent, armature, node, parent_transform):
    position = Matrix.Translation(node.position)
    rotation = Quaternion([node.rotation[3], *node.rotation[0:3]]).to_matrix().to_4x4()
    scale = Matrix.Diagonal([*node.scale, 1])
    
    matrix = parent_transform @ (position @ rotation @ scale)

    bone_name = node.name
    bone = armature.data.edit_bones.new(bone_name)

    tail, roll = mat3_to_vec_roll(matrix.to_3x3())
    tail *= 10  # Make this scale with the model size in the future, for convenience
    
    list_of_bones.append(bone)
    bone.head = Vector([0., 0., 0.])
    bone.tail = Vector([0., 1., 0.])
    
    pos_vector = matrix.to_translation()
    bone.head = pos_vector
    bone.tail = pos_vector + tail
    bone.roll = roll

    if parent != -1:
        bone.parent = list_of_bones[parent]

    for attachment in node.attachments:
        if attachment.type == 4:
            import_mesh(name, meshes, attachment.data, armature, matrix)

    idx = len(list_of_bones) - 1
    
    for child in node.children:
        build_nodes(name, meshes, list_of_bones, idx, armature, child, matrix)
    
def import_mesh(name, meshes, mesh, armature, matrix):
    meshobj_name = f"{name}_{len(meshes)}"
    bpy_mesh = bpy.data.meshes.new(name=meshobj_name)
    bpy_mesh_object = bpy.data.objects.new(meshobj_name, bpy_mesh)
    meshes.append(bpy_mesh_object)
    
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
    bpy_mesh.transform(matrix)
    bpy_mesh.update()
    
    bpy.context.view_layer.objects.active = armature
        
def add_uv_map(bpy_mesh, texcoords, name):
    if texcoords[0] is not None:
        uv_layer = bpy_mesh.uv_layers.new(name=name, do_init=True)
        for loop_idx, loop in enumerate(bpy_mesh.loops):
            uv_layer.data[loop_idx].uv = texcoords[loop.vertex_index]
