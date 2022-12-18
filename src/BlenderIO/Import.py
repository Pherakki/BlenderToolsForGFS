import array
import os
import math
import tempfile

import bpy
import bmesh
from bpy_extras.io_utils import ImportHelper
from mathutils import Matrix, Quaternion, Vector

from ..FileFormats.GFS.GFSInterface import GFSInterface
from .Utils.ErrorPopup import handle_errors


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


    # filter_glob: bpy.props.StringProperty(
    #                                          default="*.GMD",
    #                                          options={'HIDDEN'},
    #                                      )
    
    def import_file(self, context, filepath):
        bpy.ops.object.select_all(action='DESELECT')

        gfs = GFSInterface.from_file(filepath)
        
        textures  = import_textures(gfs)
        materials = import_materials(gfs, textures)
        model     = import_model(gfs, os.path.split(filepath)[1].split('.')[0])
            
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
        
        bpy_material[name] = texture.unknowns
        
        return node
    return None
        
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
        bpy_bone.tail = Vector([0., 1., 0.])
        
        pos_vector = matrix.to_translation()
        bpy_bone.head = pos_vector
        bpy_bone.tail = pos_vector + tail
        bpy_bone.roll = roll
        
        list_of_bones[i] = bpy_bone
        bone_transforms[i] = matrix
        
    for i, mesh in enumerate(gfs.meshes):
        import_mesh("mesh", i, mesh, list_of_bones, armature, list_of_bones[mesh.node])
        
    # Cameras, Lights, EPL...
        
    bpy.ops.object.mode_set(mode='OBJECT')
        
    # Reset state
    bpy.context.view_layer.objects.active = initial_obj


def import_mesh(name, idx, mesh, bpy_bones, armature, bpy_bone):
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
    
    constraint = bpy_mesh_object.constraints.new("CHILD_OF")
    constraint.target = armature
    constraint.subtarget = bpy_bone.name
    
    
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
