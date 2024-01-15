import bpy
from mathutils import Vector

from ..Data import dummy_image_data
from ..Utils.UVMapManagement import make_uv_map_name


class NodePositioningData:
    def __init__(self):
        self.tex_count = 0
        
def format_texindex(idx):
    if 0 <= idx < 7:
        return str(idx)
    else:
        return "None"


def import_materials(gfs, textures, errorlog):
    materials = {}

    # Load materials
    for mat in gfs.materials:
        bpy_material = bpy.data.materials.new(mat.name)
        materials[mat.name] = (bpy_material, mat)
        
        bpy_material.use_nodes = True
        
        nodes = bpy_material.node_tree.nodes
        connect = bpy_material.node_tree.links.new
        
        # Construct basic output
        nodes.clear()
        bsdf_node = nodes.new("ShaderNodeBsdfPrincipled")
        output_node = nodes.new("ShaderNodeOutputMaterial")
        output_node.location = (280, 0)
        connect(bsdf_node.outputs[0], output_node.inputs[0])
        
        
        node_pos_data = NodePositioningData()
        node = add_texture_to_material_node(bpy_material, bsdf_node, node_pos_data, textures, "Diffuse Texture", mat.diffuse_texture, mat.texture_indices_1.diffuse,   errorlog)
        if node is not None:
            connect(node.outputs["Color"], bsdf_node.inputs["Base Color"])
        
        add_texture_to_material_node(bpy_material, bsdf_node, node_pos_data, textures, "Normal Texture",     mat.normal_texture,     mat.texture_indices_1.normal,     errorlog)
        add_texture_to_material_node(bpy_material, bsdf_node, node_pos_data, textures, "Specular Texture",   mat.specular_texture,   mat.texture_indices_1.specular,   errorlog)
        add_texture_to_material_node(bpy_material, bsdf_node, node_pos_data, textures, "Reflection Texture", mat.reflection_texture, mat.texture_indices_1.reflection, errorlog)
        add_texture_to_material_node(bpy_material, bsdf_node, node_pos_data, textures, "Highlight Texture",  mat.highlight_texture,  mat.texture_indices_1.highlight,  errorlog)
        add_texture_to_material_node(bpy_material, bsdf_node, node_pos_data, textures, "Glow Texture",       mat.glow_texture,       mat.texture_indices_1.glow,       errorlog)
        add_texture_to_material_node(bpy_material, bsdf_node, node_pos_data, textures, "Night Texture",      mat.night_texture,      mat.texture_indices_1.night,      errorlog)
        add_texture_to_material_node(bpy_material, bsdf_node, node_pos_data, textures, "Detail Texture",     mat.detail_texture,     mat.texture_indices_1.detail,     errorlog)
        add_texture_to_material_node(bpy_material, bsdf_node, node_pos_data, textures, "Shadow Texture",     mat.shadow_texture,     mat.texture_indices_1.shadow,     errorlog)


        # Register currently-unrepresentable data
        # Can hopefully remove a few of these when a standardised material
        # shader node tree can be built...
        props = bpy_material.GFSTOOLS_MaterialProperties
        props.flag_0          = mat.flag_0
        props.flag_1          = mat.flag_1
        props.enable_specular = mat.enable_specular
        props.flag_3          = mat.flag_3
        props.vertex_colors   = mat.use_vertex_colors
        props.flag_5          = mat.flag_5
        props.flag_6          = mat.flag_6
        props.enable_uv_anims = mat.enable_uv_animation
        props.enable_emissive = mat.enable_emissive
        props.flag_9          = mat.flag_9
        props.flag_10         = mat.flag_10
        props.light_2         = mat.use_light_2
        props.pwire           = mat.purple_wireframe
        props.flag_13         = mat.flag_13
        props.receive_shadow  = mat.receive_shadow
        props.cast_shadow     = mat.cast_shadow
        props.flag_18         = mat.flag_18
        props.disable_bloom   = mat.disable_bloom
        props.flag_29         = mat.flag_29
        props.flag_30         = mat.flag_30
        props.flag_31         = mat.flag_31
        
        props.ambient      = mat.ambient
        props.diffuse      = mat.diffuse
        props.specular     = mat.specular
        props.emissive     = mat.emissive
        props.reflectivity = mat.reflectivity
        props.outline_idx  = mat.outline_idx
        props.draw_method  = mat.draw_method
        props.unknown_0x51 = mat.unknown_0x51
        props.unknown_0x52 = mat.unknown_0x52
        props.unknown_0x53 = mat.unknown_0x53
        props.unknown_0x54 = mat.unknown_0x54
        props.unknown_0x55 = mat.unknown_0x55
        props.unknown_0x56 = mat.unknown_0x56
        props.unknown_0x58 = mat.unknown_0x58
        props.unknown_0x5A = mat.unknown_0x5A
        props.unknown_0x5C = mat.unknown_0x5C
        props.unknown_0x5E = mat.unknown_0x5E
        props.unknown_0x6A = mat.unknown_0x6A
        
        # props.diffuse_uv_in     = format_texindex(mat.texture_indices_1.diffuse)
        props.diffuse_uv_out    = format_texindex(mat.texture_indices_2.diffuse)
        # props.normal_uv_in      = format_texindex(mat.texture_indices_1.normal)
        props.normal_uv_out     = format_texindex(mat.texture_indices_2.normal)
        # props.specular_uv_in    = format_texindex(mat.texture_indices_1.specular)
        props.specular_uv_out   = format_texindex(mat.texture_indices_2.specular)
        # props.reflection_uv_in  = format_texindex(mat.texture_indices_1.reflection)
        props.reflection_uv_out = format_texindex(mat.texture_indices_2.reflection)
        # props.highlight_uv_in   = format_texindex(mat.texture_indices_1.highlight)
        props.highlight_uv_out  = format_texindex(mat.texture_indices_2.highlight)
        # props.glow_uv_in        = format_texindex(mat.texture_indices_1.glow)
        props.glow_uv_out       = format_texindex(mat.texture_indices_2.glow)
        # props.night_uv_in       = format_texindex(mat.texture_indices_1.night)
        props.night_uv_out      = format_texindex(mat.texture_indices_2.night)
        # props.detail_uv_in      = format_texindex(mat.texture_indices_1.detail)
        props.detail_uv_out     = format_texindex(mat.texture_indices_2.detail)
        # props.shadow_uv_in      = format_texindex(mat.texture_indices_1.shadow)
        props.shadow_uv_out     = format_texindex(mat.texture_indices_2.shadow)
        
        bpy_material.use_backface_culling = not bool(mat.disable_backface_culling)
        
        for attr in mat.attributes:
            if attr.ID == 0:
                ctr = attr.data
                
                bpy_material.GFSTOOLS_MaterialProperties.has_toon = True
                
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_0  = attr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_1  = attr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_2  = attr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_3  = attr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_4  = attr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_5  = attr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_6  = attr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_7  = attr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_8  = attr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_9  = attr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_10 = attr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_11 = attr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_12 = attr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_13 = attr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_14 = attr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.toon_ctr_flag_15 = attr.flags.flag_15
                
                bpy_material.GFSTOOLS_MaterialProperties.toon_colour           = ctr.colour
                bpy_material.GFSTOOLS_MaterialProperties.toon_light_threshold  = ctr.light_threshold
                bpy_material.GFSTOOLS_MaterialProperties.toon_light_factor     = ctr.light_factor
                bpy_material.GFSTOOLS_MaterialProperties.toon_light_brightness = ctr.light_brightness
                bpy_material.GFSTOOLS_MaterialProperties.toon_shadow_threshold = ctr.shadow_threshold
                bpy_material.GFSTOOLS_MaterialProperties.toon_shadow_factor    = ctr.shadow_factor
                
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_0   = ctr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_1   = ctr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_2   = ctr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_3   = ctr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_4   = ctr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_5   = ctr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_6   = ctr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_7   = ctr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_8   = ctr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_9   = ctr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_10  = ctr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_11  = ctr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_12  = ctr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_13  = ctr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_14  = ctr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_15  = ctr.flags.flag_15
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_16  = ctr.flags.flag_16
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_17  = ctr.flags.flag_17
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_18  = ctr.flags.flag_18
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_19  = ctr.flags.flag_19
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_20  = ctr.flags.flag_20
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_21  = ctr.flags.flag_21
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_22  = ctr.flags.flag_22
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_23  = ctr.flags.flag_23
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_24  = ctr.flags.flag_24
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_25  = ctr.flags.flag_25
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_26  = ctr.flags.flag_26
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_27  = ctr.flags.flag_27
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_28  = ctr.flags.flag_28
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_29  = ctr.flags.flag_29
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_30  = ctr.flags.flag_30
                bpy_material.GFSTOOLS_MaterialProperties.toon_flag_31  = ctr.flags.flag_31
            
            elif attr.ID == 1:
                ctr = attr.data
                
                bpy_material.GFSTOOLS_MaterialProperties.has_a1 = True
                
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_0  = attr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_1  = attr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_2  = attr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_3  = attr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_4  = attr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_5  = attr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_6  = attr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_7  = attr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_8  = attr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_9  = attr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_10 = attr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_11 = attr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_12 = attr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_13 = attr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_14 = attr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.a1_ctr_flag_15 = attr.flags.flag_15
                
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x00 = ctr.unknown_0x00
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x04 = ctr.unknown_0x04
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x08 = ctr.unknown_0x08
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x0C = ctr.unknown_0x0C
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x10 = ctr.unknown_0x10
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x14 = ctr.unknown_0x14
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x18 = ctr.unknown_0x18
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x1C = ctr.unknown_0x1C
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x20 = ctr.unknown_0x20
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x24 = ctr.unknown_0x24
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x28 = ctr.unknown_0x28
                bpy_material.GFSTOOLS_MaterialProperties.a1_unknown_0x2C = ctr.unknown_0x2C
                
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_0   = ctr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_1   = ctr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_2   = ctr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_3   = ctr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_4   = ctr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_5   = ctr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_6   = ctr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_7   = ctr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_8   = ctr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_9   = ctr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_10  = ctr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_11  = ctr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_12  = ctr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_13  = ctr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_14  = ctr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_15  = ctr.flags.flag_15
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_16  = ctr.flags.flag_16
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_17  = ctr.flags.flag_17
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_18  = ctr.flags.flag_18
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_19  = ctr.flags.flag_19
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_20  = ctr.flags.flag_20
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_21  = ctr.flags.flag_21
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_22  = ctr.flags.flag_22
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_23  = ctr.flags.flag_23
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_24  = ctr.flags.flag_24
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_25  = ctr.flags.flag_25
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_26  = ctr.flags.flag_26
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_27  = ctr.flags.flag_27
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_28  = ctr.flags.flag_28
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_29  = ctr.flags.flag_29
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_30  = ctr.flags.flag_30
                bpy_material.GFSTOOLS_MaterialProperties.a1_flag_31  = ctr.flags.flag_31
            
            elif attr.ID == 2:
                ctr = attr.data
                
                bpy_material.GFSTOOLS_MaterialProperties.has_outline = True
                
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_0  = attr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_1  = attr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_2  = attr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_3  = attr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_4  = attr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_5  = attr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_6  = attr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_7  = attr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_8  = attr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_9  = attr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_10 = attr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_11 = attr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_12 = attr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_13 = attr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_14 = attr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.outline_ctr_flag_15 = attr.flags.flag_15
                
                bpy_material.GFSTOOLS_MaterialProperties.outline_type  = ctr.type
                bpy_material.GFSTOOLS_MaterialProperties.outline_color = ctr.colour
                
            elif attr.ID == 3:
                ctr = attr.data
                
                bpy_material.GFSTOOLS_MaterialProperties.has_a3 = True
                
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_0  = attr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_1  = attr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_2  = attr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_3  = attr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_4  = attr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_5  = attr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_6  = attr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_7  = attr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_8  = attr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_9  = attr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_10 = attr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_11 = attr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_12 = attr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_13 = attr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_14 = attr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.a3_ctr_flag_15 = attr.flags.flag_15
                
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x00 = ctr.unknown_0x00
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x04 = ctr.unknown_0x04
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x08 = ctr.unknown_0x08
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x0C = ctr.unknown_0x0C
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x10 = ctr.unknown_0x10
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x14 = ctr.unknown_0x14
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x18 = ctr.unknown_0x18
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x1C = ctr.unknown_0x1C
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x20 = ctr.unknown_0x20
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x24 = ctr.unknown_0x24
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x28 = ctr.unknown_0x28
                bpy_material.GFSTOOLS_MaterialProperties.a3_unknown_0x2C = ctr.unknown_0x2C
                
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_0   = ctr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_1   = ctr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_2   = ctr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_3   = ctr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_4   = ctr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_5   = ctr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_6   = ctr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_7   = ctr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_8   = ctr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_9   = ctr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_10  = ctr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_11  = ctr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_12  = ctr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_13  = ctr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_14  = ctr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_15  = ctr.flags.flag_15
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_16  = ctr.flags.flag_16
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_17  = ctr.flags.flag_17
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_18  = ctr.flags.flag_18
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_19  = ctr.flags.flag_19
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_20  = ctr.flags.flag_20
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_21  = ctr.flags.flag_21
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_22  = ctr.flags.flag_22
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_23  = ctr.flags.flag_23
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_24  = ctr.flags.flag_24
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_25  = ctr.flags.flag_25
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_26  = ctr.flags.flag_26
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_27  = ctr.flags.flag_27
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_28  = ctr.flags.flag_28
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_29  = ctr.flags.flag_29
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_30  = ctr.flags.flag_30
                bpy_material.GFSTOOLS_MaterialProperties.a3_flag_31  = ctr.flags.flag_31
                
            elif attr.ID == 4:
                ctr = attr.data
                
                bpy_material.GFSTOOLS_MaterialProperties.has_a4 = True
                
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_0  = attr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_1  = attr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_2  = attr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_3  = attr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_4  = attr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_5  = attr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_6  = attr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_7  = attr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_8  = attr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_9  = attr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_10 = attr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_11 = attr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_12 = attr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_13 = attr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_14 = attr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.a4_ctr_flag_15 = attr.flags.flag_15
                
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x00 = ctr.unknown_0x00
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x04 = ctr.unknown_0x04
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x08 = ctr.unknown_0x08
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x0C = ctr.unknown_0x0C
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x10 = ctr.unknown_0x10
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x14 = ctr.unknown_0x14
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x18 = ctr.unknown_0x18
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x1C = ctr.unknown_0x1C
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x20 = ctr.unknown_0x20
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x24 = ctr.unknown_0x24
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x28 = ctr.unknown_0x28
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x2C = ctr.unknown_0x2C
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x30 = ctr.unknown_0x30
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x34 = ctr.unknown_0x34
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x38 = ctr.unknown_0x38
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x3C = ctr.unknown_0x3C
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x40 = ctr.unknown_0x40
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x44 = ctr.unknown_0x44
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x45 = ctr.unknown_0x45
                bpy_material.GFSTOOLS_MaterialProperties.a4_unknown_0x49 = ctr.unknown_0x49
                
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_0   = ctr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_1   = ctr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_2   = ctr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_3   = ctr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_4   = ctr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_5   = ctr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_6   = ctr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_7   = ctr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_8   = ctr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_9   = ctr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_10  = ctr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_11  = ctr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_12  = ctr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_13  = ctr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_14  = ctr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_15  = ctr.flags.flag_15
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_16  = ctr.flags.flag_16
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_17  = ctr.flags.flag_17
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_18  = ctr.flags.flag_18
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_19  = ctr.flags.flag_19
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_20  = ctr.flags.flag_20
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_21  = ctr.flags.flag_21
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_22  = ctr.flags.flag_22
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_23  = ctr.flags.flag_23
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_24  = ctr.flags.flag_24
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_25  = ctr.flags.flag_25
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_26  = ctr.flags.flag_26
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_27  = ctr.flags.flag_27
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_28  = ctr.flags.flag_28
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_29  = ctr.flags.flag_29
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_30  = ctr.flags.flag_30
                bpy_material.GFSTOOLS_MaterialProperties.a4_flag_31  = ctr.flags.flag_31
            
            elif attr.ID == 5:
                ctr = attr.data
                
                bpy_material.GFSTOOLS_MaterialProperties.has_a5 = True
                
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_0  = attr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_1  = attr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_2  = attr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_3  = attr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_4  = attr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_5  = attr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_6  = attr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_7  = attr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_8  = attr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_9  = attr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_10 = attr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_11 = attr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_12 = attr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_13 = attr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_14 = attr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.a5_ctr_flag_15 = attr.flags.flag_15
                
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x00 = ctr.unknown_0x00
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x04 = ctr.unknown_0x04
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x08 = ctr.unknown_0x08
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x0C = ctr.unknown_0x0C
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x10 = ctr.unknown_0x10
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x14 = ctr.unknown_0x14
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x18 = ctr.unknown_0x18
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x1C = ctr.unknown_0x1C
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x20 = ctr.unknown_0x20
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x24 = ctr.unknown_0x24
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x28 = ctr.unknown_0x28
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x2C = ctr.unknown_0x2C
                bpy_material.GFSTOOLS_MaterialProperties.a5_unknown_0x30 = ctr.unknown_0x30
                
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_0   = ctr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_1   = ctr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_2   = ctr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_3   = ctr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_4   = ctr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_5   = ctr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_6   = ctr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_7   = ctr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_8   = ctr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_9   = ctr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_10  = ctr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_11  = ctr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_12  = ctr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_13  = ctr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_14  = ctr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_15  = ctr.flags.flag_15
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_16  = ctr.flags.flag_16
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_17  = ctr.flags.flag_17
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_18  = ctr.flags.flag_18
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_19  = ctr.flags.flag_19
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_20  = ctr.flags.flag_20
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_21  = ctr.flags.flag_21
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_22  = ctr.flags.flag_22
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_23  = ctr.flags.flag_23
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_24  = ctr.flags.flag_24
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_25  = ctr.flags.flag_25
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_26  = ctr.flags.flag_26
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_27  = ctr.flags.flag_27
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_28  = ctr.flags.flag_28
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_29  = ctr.flags.flag_29
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_30  = ctr.flags.flag_30
                bpy_material.GFSTOOLS_MaterialProperties.a5_flag_31  = ctr.flags.flag_31
            
            elif attr.ID == 6:
                ctr = attr.data
                
                bpy_material.GFSTOOLS_MaterialProperties.has_a6 = True
                
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_0  = attr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_1  = attr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_2  = attr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_3  = attr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_4  = attr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_5  = attr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_6  = attr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_7  = attr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_8  = attr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_9  = attr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_10 = attr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_11 = attr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_12 = attr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_13 = attr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_14 = attr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.a6_ctr_flag_15 = attr.flags.flag_15
                
                bpy_material.GFSTOOLS_MaterialProperties.a6_unknown_0x00 = ctr.unknown_0x00
                bpy_material.GFSTOOLS_MaterialProperties.a6_unknown_0x04 = ctr.unknown_0x04
                bpy_material.GFSTOOLS_MaterialProperties.a6_unknown_0x08 = ctr.unknown_0x08
                            
            elif attr.ID == 7:
                ctr = attr.data
                
                bpy_material.GFSTOOLS_MaterialProperties.has_a7 = True
                
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_0  = attr.flags.flag_0
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_1  = attr.flags.flag_1
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_2  = attr.flags.flag_2
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_3  = attr.flags.flag_3
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_4  = attr.flags.flag_4
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_5  = attr.flags.flag_5
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_6  = attr.flags.flag_6
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_7  = attr.flags.flag_7
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_8  = attr.flags.flag_8
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_9  = attr.flags.flag_9
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_10 = attr.flags.flag_10
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_11 = attr.flags.flag_11
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_12 = attr.flags.flag_12
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_13 = attr.flags.flag_13
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_14 = attr.flags.flag_14
                bpy_material.GFSTOOLS_MaterialProperties.a7_ctr_flag_15 = attr.flags.flag_15
                
    return materials

def add_texture_to_material_node(bpy_material, bsdf_node, node_pos_data, textures, name, texture, texcoord_id, errorlog):
    nodes = bpy_material.node_tree.nodes
    reference_pos = bsdf_node.location
    if texture is not None:
        node = nodes.new('ShaderNodeTexImage')
        node.name = name
        node.label = name
        
        tex_name = texture.name.string
        if tex_name in textures:
            node.image = textures[tex_name]
        else:
            errorlog.log_warning_message(f"Texture file '{tex_name}' for slot '{name}' on material '{bpy_material.name}' does not exist inside the file. Falling back to a dummy texture.")
            make_dummy_img_if_doesnt_exist()
            node.image = bpy.data.images["dummy"]
        
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x04 = texture.unknown_0x04
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x08 = texture.unknown_0x08
        node.GFSTOOLS_TextureRefPanelProperties.has_texture_filtering = texture.has_texture_filtering
        node.GFSTOOLS_TextureRefPanelProperties.wrap_mode_u  = texture.wrap_mode_u
        node.GFSTOOLS_TextureRefPanelProperties.wrap_mode_v  = texture.wrap_mode_v
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x0C = texture.unknown_0x0C[0]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x10 = texture.unknown_0x0C[1]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x14 = texture.unknown_0x0C[2]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x18 = texture.unknown_0x0C[3]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x1C = texture.unknown_0x0C[4]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x20 = texture.unknown_0x0C[5]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x24 = texture.unknown_0x0C[6]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x28 = texture.unknown_0x0C[7]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x2C = texture.unknown_0x0C[8]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x30 = texture.unknown_0x0C[9]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x34 = texture.unknown_0x0C[10]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x38 = texture.unknown_0x0C[11]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x3C = texture.unknown_0x0C[12]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x40 = texture.unknown_0x0C[13]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x44 = texture.unknown_0x0C[14]
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x48 = texture.unknown_0x0C[15]
        
        connect = bpy_material.node_tree.links.new
        uv_map_node = nodes.new("ShaderNodeUVMap")
        uv_map_node.uv_map = make_uv_map_name(texcoord_id)
        connect(uv_map_node.outputs["UV"], node.inputs["Vector"])
        
        node.location        = reference_pos - Vector([240 + 50, 0]) - Vector([0, node_pos_data.tex_count*(277 + 50)])
        uv_map_node.location = node.location - Vector([150 + 50, 0]) - Vector([0, 170])
        
        node_pos_data.tex_count += 1
        
        return node
    return None


def make_dummy_img_if_doesnt_exist():
    import os
    
    if "dummy" not in bpy.data.images:
        filepath = os.path.join(bpy.app.tempdir, "dummy.dds")
        # Try/finally seems to prevent a race condition between Blender and 
        # Python forming
        try:
            with open(filepath, 'wb') as F:
                F.write(dummy_image_data)
            img = bpy.data.images.load(filepath)
            img.pack()
            img.filepath_raw = "dummy.dds"
            
            img.GFSTOOLS_ImageProperties.unknown_1 = 1
            img.GFSTOOLS_ImageProperties.unknown_2 = 1
            img.GFSTOOLS_ImageProperties.unknown_3 = 0
            img.GFSTOOLS_ImageProperties.unknown_4 = 0
        finally:
            os.remove(filepath)
        