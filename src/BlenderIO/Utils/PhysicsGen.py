import math

import bpy
from mathutils import Matrix

from ..modelUtilsTest.API.Version import bpy_at_least
from .Maths import boneY_to_boneX_matrix, upY_to_upZ_matrix, colY_to_colX_matrix

COLLIDER_MATERIAL_NAME = ".GFSTOOLS_ColliderMaterial"


def make_capsule(n, radius, height):
    # n is the number of verts per quarter
        
    vertices = []
    polys = []
    
    # Hemisphere 1
    v_offset = len(vertices)
    for j in range(n):
        theta = j * 2*math.pi/ (4*n)
        z = radius*math.sin(theta) + height
        for i in range(n*4):
            phi = i * 2*math.pi/ (4*n)
            
            x = radius * math.cos(phi) * math.cos(theta)
            y = radius * math.sin(phi) * math.cos(theta)
            
            vertices.append((x, y, z))
    vertices.append((0., 0., radius + height))

    for j in range(n-1):
        for i in range(n*4 - 1):
            s1 = v_offset + 4*n*j + i
            s2 = v_offset + 4*n*(j+1) + i
            polys.append((s1, s1+1, s2+1, s2))
        
        s1 = v_offset + 4*n*j     + (4*n - 1)
        s2 = v_offset + 4*n*(j+1) + (4*n - 1)
        polys.append((s1, 4*n*j, 4*n*(j+1), s2))
        
    final_idx = len(vertices) - 1
    j_row = v_offset + 4*n*(n-1)
    for i in range(n*4 - 1):
        polys.append((j_row + i, j_row + i + 1, final_idx))
    polys.append((final_idx-1, j_row, final_idx))

    # Hemisphere 2
    v_offset = len(vertices)
    for j in range(n):
        theta = j * 2*math.pi/ (4*n)
        z = - radius*math.sin(theta) - height
        for i in range(n*4):
            phi = i * 2*math.pi/ (4*n)
            
            x = radius * math.cos(phi) * math.cos(theta)
            y = radius * math.sin(phi) * math.cos(theta)
            
            vertices.append((x, y, z))
    vertices.append((0., 0., - radius - height))

    for j in range(n-1):
        for i in range(n*4 - 1):
            s1 = v_offset + 4*n*j + i
            s2 = v_offset + 4*n*(j+1) + i
            polys.append((s1+1, s1, s2, s2+1))
        
        s1 = v_offset + 4*n*j     
        s2 = v_offset + 4*n*(j+1)
        polys.append((s1, s1 + (4*n - 1), s2 + (4*n - 1), s2))
        
    final_idx = len(vertices) - 1
    j_row = v_offset + 4*n*(n-1)
    for i in range(n*4 - 1):
        polys.append((j_row + i + 1, j_row + i, final_idx))
    polys.append((j_row, final_idx-1, final_idx))
    
    # Cylinder body
    for i in range(n*4 - 1):
        s1 = i
        s2 = v_offset + i
        polys.append([s1+1, s1, s2, s2+1])
    s1 = n*4-1
    s2 = v_offset + n*4 - 1
    polys.append([0, s1, s2, v_offset])
    
    return vertices, [], polys


def remake_col_material():
    if COLLIDER_MATERIAL_NAME not in bpy.data.materials:
        col_mat = bpy.data.materials.new(COLLIDER_MATERIAL_NAME)
        remake_col_nodetree(col_mat)

def get_col_material():
    if COLLIDER_MATERIAL_NAME not in bpy.data.materials:
        col_mat = bpy.data.materials.new(COLLIDER_MATERIAL_NAME)
        remake_col_nodetree(col_mat)
    return bpy.data.materials[COLLIDER_MATERIAL_NAME]

def repair_col_material():
    if COLLIDER_MATERIAL_NAME not in bpy.data.materials:
        col_mat = bpy.data.materials.new(COLLIDER_MATERIAL_NAME)
    else:
        col_mat = bpy.data.materials[COLLIDER_MATERIAL_NAME]
    remake_col_nodetree(col_mat)

def remake_col_nodetree(col_mat):
    col_mat.use_nodes = True
    col_mat.node_tree.nodes.clear()
    col_mat.node_tree.links.clear()
    
    nodes = col_mat.node_tree.nodes
    links = col_mat.node_tree.links
    connect = links.new
    
    # Node setup
    node = nodes.new("ShaderNodeBsdfPrincipled")
    node.inputs["Base Color"].default_value = [0.0, 1.0, 0.4, 1.0]
    node.inputs["Alpha"].default_value = 0.2
    node.location = (0, 0)
    
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (300, 0)
    
    # Connect them up
    connect(node.outputs["BSDF"], out.inputs["Surface"])
    
    # Material properties
    col_mat.use_backface_culling = True
    col_mat.blend_method = "BLEND"


def make_collider_mesh(collider_name, mat, height, radius, is_capsule):
    bpy_mesh = bpy.data.meshes.new(name=collider_name)
    bpy_mesh_object = bpy.data.objects.new(collider_name, bpy_mesh)
    rebuild_collider(bpy_mesh, radius, height, is_capsule)
    
    bpy.context.collection.objects.link(bpy_mesh_object)
    bpy_mesh_object.active_material = mat
    return bpy_mesh_object

if bpy_at_least(4, 1, 0):
    def rebuild_collider(bpy_mesh, radius, height, is_capsule):
        complexity = 4
        
        bpy_mesh.clear_geometry()
        bpy_mesh.from_pydata(*make_capsule(complexity, radius, is_capsule*height/2))
        for poly in bpy_mesh.polygons:
            poly.use_smooth = True
else:
    def rebuild_collider(bpy_mesh, radius, height, is_capsule):
        complexity = 4
        
        bpy_mesh.clear_geometry()
        bpy_mesh.from_pydata(*make_capsule(complexity, radius, is_capsule*height/2))
        bpy_mesh.use_auto_smooth = True
        for poly in bpy_mesh.polygons:
            poly.use_smooth = True


def make_collider(has_name, dtype, height, radius, ibpm, parent_bone, armature):
    # Get parent bone data
    if parent_bone is None:
        bone = None
    else:
        bone = armature.data.bones.get(parent_bone)

    if bone is None:
        parent_matrix = upY_to_upZ_matrix @ armature.matrix_world    
        collider_name = f".Collider_{armature.name}"
    else:
        parent_matrix = armature.matrix_world @ bone.matrix_local @ boneY_to_boneX_matrix.inverted()
        collider_name = f".Collider_{parent_bone}_{armature.name}"
        
    remake_col_material()
    
    # Build collider
    collider = make_collider_mesh(collider_name, bpy.data.materials[COLLIDER_MATERIAL_NAME], height, radius, dtype=="Capsule")
    collider.data.GFSTOOLS_ColliderProperties["height"] = height
    collider.data.GFSTOOLS_ColliderProperties["radius"] = radius
    collider.data.GFSTOOLS_ColliderProperties.dtype     = dtype
    collider.data.GFSTOOLS_ColliderProperties.detached  = (not has_name) and (bone is None)
    collider.data.GFSTOOLS_MeshProperties.dtype = "COLLIDER"
    
    ibpm = Matrix([ibpm[0:4], ibpm[4:8], ibpm[8:12], ibpm[12:16]])
    ibpmr = ibpm.transposed() # Inverse Mesh Relative Bind Pose matrix
    t, r, s = ibpmr.decompose()
    ibpmr = Matrix.Translation(t) @ r.to_matrix().to_4x4()
    
    if bone is None:
        collider.parent = armature
    else:
        collider.parent = armature
        collider.parent_type = "BONE"
        collider.parent_bone = parent_bone
    
    collider.matrix_world = parent_matrix @ ibpmr @ colY_to_colX_matrix

    return collider
