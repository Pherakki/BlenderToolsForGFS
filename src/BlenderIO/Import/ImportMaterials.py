import bpy


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
