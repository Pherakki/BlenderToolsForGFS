import os

import bpy

from ..WarningSystem.Warning import ReportableWarning, ReportableError
from ..Utils.UVMapManagement import is_valid_uv_map, get_uv_idx_from_name
from .Data import dummy_image_data


def export_materials_and_textures(gfs, bpy_material_names, errorlog):
    texture_names = set()
    for bpy_material_name in bpy_material_names:
        bpy_material = bpy.data.materials[bpy_material_name]
        mat_name = bpy_material.name
        
        mat = gfs.add_material(mat_name)
        mat.flag_0              = bpy_material.GFSTOOLS_MaterialProperties.flag_0
        mat.flag_1              = bpy_material.GFSTOOLS_MaterialProperties.flag_1
        mat.enable_specular     = bpy_material.GFSTOOLS_MaterialProperties.enable_specular
        mat.flag_3              = bpy_material.GFSTOOLS_MaterialProperties.flag_3
        mat.use_vertex_colous   = bpy_material.GFSTOOLS_MaterialProperties.vertex_colors
        mat.flag_5              = bpy_material.GFSTOOLS_MaterialProperties.flag_5
        mat.flag_6              = bpy_material.GFSTOOLS_MaterialProperties.flag_6
        mat.enable_uv_animation = bpy_material.GFSTOOLS_MaterialProperties.enable_uv_anims
        mat.enable_emissive     = bpy_material.GFSTOOLS_MaterialProperties.enable_emissive
        mat.flag_9              = bpy_material.GFSTOOLS_MaterialProperties.flag_9
        mat.flag_10             = bpy_material.GFSTOOLS_MaterialProperties.flag_10
        mat.use_light_2         = bpy_material.GFSTOOLS_MaterialProperties.light_2
        mat.purple_wireframe    = bpy_material.GFSTOOLS_MaterialProperties.pwire
        mat.flag_13             = bpy_material.GFSTOOLS_MaterialProperties.flag_13
        mat.receive_shadow      = bpy_material.GFSTOOLS_MaterialProperties.receive_shadow
        mat.cast_shadow         = bpy_material.GFSTOOLS_MaterialProperties.cast_shadow
        mat.flag_18             = bpy_material.GFSTOOLS_MaterialProperties.flag_18
        mat.disable_bloom       = bpy_material.GFSTOOLS_MaterialProperties.disable_bloom
        mat.flag_29             = bpy_material.GFSTOOLS_MaterialProperties.flag_29
        mat.flag_30             = bpy_material.GFSTOOLS_MaterialProperties.flag_30
        mat.flag_31             = bpy_material.GFSTOOLS_MaterialProperties.flag_31

        mat.ambient      = bpy_material.GFSTOOLS_MaterialProperties.ambient
        mat.diffuse      = bpy_material.GFSTOOLS_MaterialProperties.diffuse
        mat.specular     = bpy_material.GFSTOOLS_MaterialProperties.specular
        mat.emissive     = bpy_material.GFSTOOLS_MaterialProperties.emissive
        mat.reflectivity = bpy_material.GFSTOOLS_MaterialProperties.reflectivity
        mat.outline_idx  = bpy_material.GFSTOOLS_MaterialProperties.outline_idx
        mat.draw_method  = bpy_material.GFSTOOLS_MaterialProperties.draw_method
        mat.unknown_0x51 = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x51
        mat.unknown_0x52 = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x52
        mat.unknown_0x53 = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x53
        mat.unknown_0x54 = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x54
        mat.unknown_0x55 = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x55
        mat.unknown_0x56 = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x56
        mat.unknown_0x58 = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x58
        mat.unknown_0x5A = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x5A
        mat.unknown_0x5C = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x5C
        mat.unknown_0x5E = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x5E
        mat.unknown_0x6A = bpy_material.GFSTOOLS_MaterialProperties.unknown_0x6A
        
        mat.disable_backface_culling = int(not bpy_material.use_backface_culling)

        # Export any samplers
        nodes = bpy_material.node_tree.nodes
        texture_names.add(export_texture_node_data(mat_name, "Diffuse Texture",    nodes, mat.set_diffuse_texture   , errorlog))
        texture_names.add(export_texture_node_data(mat_name, "Normal Texture",     nodes, mat.set_normal_texture    , errorlog))
        texture_names.add(export_texture_node_data(mat_name, "Specular Texture",   nodes, mat.set_specular_texture  , errorlog))
        texture_names.add(export_texture_node_data(mat_name, "Reflection Texture", nodes, mat.set_reflection_texture, errorlog))
        texture_names.add(export_texture_node_data(mat_name, "Highlight Texture",  nodes, mat.set_highlight_texture , errorlog))
        texture_names.add(export_texture_node_data(mat_name, "Glow Texture",       nodes, mat.set_glow_texture      , errorlog))
        texture_names.add(export_texture_node_data(mat_name, "Night Texture",      nodes, mat.set_night_texture     , errorlog))
        texture_names.add(export_texture_node_data(mat_name, "Detail Texture",     nodes, mat.set_detail_texture    , errorlog))
        texture_names.add(export_texture_node_data(mat_name, "Shadow Texture",     nodes, mat.set_shadow_texture    , errorlog))
          
        props = bpy_material.GFSTOOLS_MaterialProperties
        
        # Export attributes
        # TOON
        if props.has_toon:
            attr = mat.add_toon_shading_attribute(
                props.toon_colour,
                props.toon_light_threshold,
                props.toon_light_factor,
                props.toon_light_brightness,
                props.toon_shadow_threshold,
                props.toon_shadow_factor
            )
            
            attr.flags.flag_0  = props.toon_ctr_flag_0
            attr.flags.flag_1  = props.toon_ctr_flag_1
            attr.flags.flag_2  = props.toon_ctr_flag_2
            attr.flags.flag_3  = props.toon_ctr_flag_3
            attr.flags.flag_4  = props.toon_ctr_flag_4
            attr.flags.flag_5  = props.toon_ctr_flag_5
            attr.flags.flag_6  = props.toon_ctr_flag_6
            attr.flags.flag_7  = props.toon_ctr_flag_7
            attr.flags.flag_8  = props.toon_ctr_flag_8
            attr.flags.flag_9  = props.toon_ctr_flag_9
            attr.flags.flag_10 = props.toon_ctr_flag_10
            attr.flags.flag_11 = props.toon_ctr_flag_11
            attr.flags.flag_12 = props.toon_ctr_flag_12
            attr.flags.flag_13 = props.toon_ctr_flag_13
            attr.flags.flag_14 = props.toon_ctr_flag_14
            attr.flags.flag_15 = props.toon_ctr_flag_15
            
            attr.data.flags.flag_0  = props.toon_flag_0
            attr.data.flags.flag_1  = props.toon_flag_1
            attr.data.flags.flag_2  = props.toon_flag_2
            attr.data.flags.flag_3  = props.toon_flag_3
            attr.data.flags.flag_4  = props.toon_flag_4
            attr.data.flags.flag_5  = props.toon_flag_5
            attr.data.flags.flag_6  = props.toon_flag_6
            attr.data.flags.flag_7  = props.toon_flag_7
            attr.data.flags.flag_8  = props.toon_flag_8
            attr.data.flags.flag_9  = props.toon_flag_9
            attr.data.flags.flag_10 = props.toon_flag_10
            attr.data.flags.flag_11 = props.toon_flag_11
            attr.data.flags.flag_12 = props.toon_flag_12
            attr.data.flags.flag_13 = props.toon_flag_13
            attr.data.flags.flag_14 = props.toon_flag_14
            attr.data.flags.flag_15 = props.toon_flag_15
            attr.data.flags.flag_16 = props.toon_flag_16
            attr.data.flags.flag_17 = props.toon_flag_17
            attr.data.flags.flag_18 = props.toon_flag_18
            attr.data.flags.flag_19 = props.toon_flag_19
            attr.data.flags.flag_20 = props.toon_flag_20
            attr.data.flags.flag_21 = props.toon_flag_21
            attr.data.flags.flag_22 = props.toon_flag_22
            attr.data.flags.flag_23 = props.toon_flag_23
            attr.data.flags.flag_24 = props.toon_flag_24
            attr.data.flags.flag_25 = props.toon_flag_25
            attr.data.flags.flag_26 = props.toon_flag_26
            attr.data.flags.flag_27 = props.toon_flag_27
            attr.data.flags.flag_28 = props.toon_flag_28
            attr.data.flags.flag_29 = props.toon_flag_29
            attr.data.flags.flag_30 = props.toon_flag_30
            attr.data.flags.flag_31 = props.toon_flag_31
        
        # ATTRIBUTE 1
        if props.has_a1:
            attr = mat.add_attribute_1(
                props.a1_unknown_0x00,
                props.a1_unknown_0x04,
                props.a1_unknown_0x08,
                props.a1_unknown_0x0C,
                props.a1_unknown_0x10,
                props.a1_unknown_0x14,
                props.a1_unknown_0x18,
                props.a1_unknown_0x1C,
                props.a1_unknown_0x20,
                props.a1_unknown_0x24,
                props.a1_unknown_0x28,
                props.a1_unknown_0x2C
            )
            
            attr.flags.flag_0  = props.a1_ctr_flag_0
            attr.flags.flag_1  = props.a1_ctr_flag_1
            attr.flags.flag_2  = props.a1_ctr_flag_2
            attr.flags.flag_3  = props.a1_ctr_flag_3
            attr.flags.flag_4  = props.a1_ctr_flag_4
            attr.flags.flag_5  = props.a1_ctr_flag_5
            attr.flags.flag_6  = props.a1_ctr_flag_6
            attr.flags.flag_7  = props.a1_ctr_flag_7
            attr.flags.flag_8  = props.a1_ctr_flag_8
            attr.flags.flag_9  = props.a1_ctr_flag_9
            attr.flags.flag_10 = props.a1_ctr_flag_10
            attr.flags.flag_11 = props.a1_ctr_flag_11
            attr.flags.flag_12 = props.a1_ctr_flag_12
            attr.flags.flag_13 = props.a1_ctr_flag_13
            attr.flags.flag_14 = props.a1_ctr_flag_14
            attr.flags.flag_15 = props.a1_ctr_flag_15
            
            attr.data.flags.flag_0  = props.a1_flag_0
            attr.data.flags.flag_1  = props.a1_flag_1
            attr.data.flags.flag_2  = props.a1_flag_2
            attr.data.flags.flag_3  = props.a1_flag_3
            attr.data.flags.flag_4  = props.a1_flag_4
            attr.data.flags.flag_5  = props.a1_flag_5
            attr.data.flags.flag_6  = props.a1_flag_6
            attr.data.flags.flag_7  = props.a1_flag_7
            attr.data.flags.flag_8  = props.a1_flag_8
            attr.data.flags.flag_9  = props.a1_flag_9
            attr.data.flags.flag_10 = props.a1_flag_10
            attr.data.flags.flag_11 = props.a1_flag_11
            attr.data.flags.flag_12 = props.a1_flag_12
            attr.data.flags.flag_13 = props.a1_flag_13
            attr.data.flags.flag_14 = props.a1_flag_14
            attr.data.flags.flag_15 = props.a1_flag_15
            attr.data.flags.flag_16 = props.a1_flag_16
            attr.data.flags.flag_17 = props.a1_flag_17
            attr.data.flags.flag_18 = props.a1_flag_18
            attr.data.flags.flag_19 = props.a1_flag_19
            attr.data.flags.flag_20 = props.a1_flag_20
            attr.data.flags.flag_21 = props.a1_flag_21
            attr.data.flags.flag_22 = props.a1_flag_22
            attr.data.flags.flag_23 = props.a1_flag_23
            attr.data.flags.flag_24 = props.a1_flag_24
            attr.data.flags.flag_25 = props.a1_flag_25
            attr.data.flags.flag_26 = props.a1_flag_26
            attr.data.flags.flag_27 = props.a1_flag_27
            attr.data.flags.flag_28 = props.a1_flag_28
            attr.data.flags.flag_29 = props.a1_flag_29
            attr.data.flags.flag_30 = props.a1_flag_30
            attr.data.flags.flag_31 = props.a1_flag_31
       
        # OUTLINE ATTRIBUTE
        if props.has_outline:
            attr = mat.add_outline_attribute(
                props.outline_type,
                props.outline_color
            )
            
            attr.flags.flag_0  = props.outline_ctr_flag_0
            attr.flags.flag_1  = props.outline_ctr_flag_1
            attr.flags.flag_2  = props.outline_ctr_flag_2
            attr.flags.flag_3  = props.outline_ctr_flag_3
            attr.flags.flag_4  = props.outline_ctr_flag_4
            attr.flags.flag_5  = props.outline_ctr_flag_5
            attr.flags.flag_6  = props.outline_ctr_flag_6
            attr.flags.flag_7  = props.outline_ctr_flag_7
            attr.flags.flag_8  = props.outline_ctr_flag_8
            attr.flags.flag_9  = props.outline_ctr_flag_9
            attr.flags.flag_10 = props.outline_ctr_flag_10
            attr.flags.flag_11 = props.outline_ctr_flag_11
            attr.flags.flag_12 = props.outline_ctr_flag_12
            attr.flags.flag_13 = props.outline_ctr_flag_13
            attr.flags.flag_14 = props.outline_ctr_flag_14
            attr.flags.flag_15 = props.outline_ctr_flag_15 
       
        # ATTRIBUTE 3
        if props.has_a3:
            attr = mat.add_attribute_3(
                props.a3_unknown_0x00,
                props.a3_unknown_0x04,
                props.a3_unknown_0x08,
                props.a3_unknown_0x0C,
                props.a3_unknown_0x10,
                props.a3_unknown_0x14,
                props.a3_unknown_0x18,
                props.a3_unknown_0x1C,
                props.a3_unknown_0x20,
                props.a3_unknown_0x24,
                props.a3_unknown_0x28,
                props.a3_unknown_0x2C
            )
            
            attr.flags.flag_0  = props.a3_ctr_flag_0
            attr.flags.flag_1  = props.a3_ctr_flag_1
            attr.flags.flag_2  = props.a3_ctr_flag_2
            attr.flags.flag_3  = props.a3_ctr_flag_3
            attr.flags.flag_4  = props.a3_ctr_flag_4
            attr.flags.flag_5  = props.a3_ctr_flag_5
            attr.flags.flag_6  = props.a3_ctr_flag_6
            attr.flags.flag_7  = props.a3_ctr_flag_7
            attr.flags.flag_8  = props.a3_ctr_flag_8
            attr.flags.flag_9  = props.a3_ctr_flag_9
            attr.flags.flag_10 = props.a3_ctr_flag_10
            attr.flags.flag_11 = props.a3_ctr_flag_11
            attr.flags.flag_12 = props.a3_ctr_flag_12
            attr.flags.flag_13 = props.a3_ctr_flag_13
            attr.flags.flag_14 = props.a3_ctr_flag_14
            attr.flags.flag_15 = props.a3_ctr_flag_15
            
            attr.data.flags.flag_0  = props.a3_flag_0
            attr.data.flags.flag_1  = props.a3_flag_1
            attr.data.flags.flag_2  = props.a3_flag_2
            attr.data.flags.flag_3  = props.a3_flag_3
            attr.data.flags.flag_4  = props.a3_flag_4
            attr.data.flags.flag_5  = props.a3_flag_5
            attr.data.flags.flag_6  = props.a3_flag_6
            attr.data.flags.flag_7  = props.a3_flag_7
            attr.data.flags.flag_8  = props.a3_flag_8
            attr.data.flags.flag_9  = props.a3_flag_9
            attr.data.flags.flag_10 = props.a3_flag_10
            attr.data.flags.flag_11 = props.a3_flag_11
            attr.data.flags.flag_12 = props.a3_flag_12
            attr.data.flags.flag_13 = props.a3_flag_13
            attr.data.flags.flag_14 = props.a3_flag_14
            attr.data.flags.flag_15 = props.a3_flag_15
            attr.data.flags.flag_16 = props.a3_flag_16
            attr.data.flags.flag_17 = props.a3_flag_17
            attr.data.flags.flag_18 = props.a3_flag_18
            attr.data.flags.flag_19 = props.a3_flag_19
            attr.data.flags.flag_20 = props.a3_flag_20
            attr.data.flags.flag_21 = props.a3_flag_21
            attr.data.flags.flag_22 = props.a3_flag_22
            attr.data.flags.flag_23 = props.a3_flag_23
            attr.data.flags.flag_24 = props.a3_flag_24
            attr.data.flags.flag_25 = props.a3_flag_25
            attr.data.flags.flag_26 = props.a3_flag_26
            attr.data.flags.flag_27 = props.a3_flag_27
            attr.data.flags.flag_28 = props.a3_flag_28
            attr.data.flags.flag_29 = props.a3_flag_29
            attr.data.flags.flag_30 = props.a3_flag_30
            attr.data.flags.flag_31 = props.a3_flag_31
        
        # ATTRIBUTE 4
        if props.has_a4:
            attr = mat.add_attribute_4(
                props.a4_unknown_0x00,
                props.a4_unknown_0x04,
                props.a4_unknown_0x08,
                props.a4_unknown_0x0C,
                props.a4_unknown_0x10,
                props.a4_unknown_0x14,
                props.a4_unknown_0x18,
                props.a4_unknown_0x1C,
                props.a4_unknown_0x20,
                props.a4_unknown_0x24,
                props.a4_unknown_0x28,
                props.a4_unknown_0x2C,
                props.a4_unknown_0x30,
                props.a4_unknown_0x34,
                props.a4_unknown_0x38,
                props.a4_unknown_0x3C,
                props.a4_unknown_0x40,
                props.a4_unknown_0x44,
                props.a4_unknown_0x45,
                props.a4_unknown_0x49
            )
                        
            attr.flags.flag_0  = props.a4_ctr_flag_0
            attr.flags.flag_1  = props.a4_ctr_flag_1
            attr.flags.flag_2  = props.a4_ctr_flag_2
            attr.flags.flag_3  = props.a4_ctr_flag_3
            attr.flags.flag_4  = props.a4_ctr_flag_4
            attr.flags.flag_5  = props.a4_ctr_flag_5
            attr.flags.flag_6  = props.a4_ctr_flag_6
            attr.flags.flag_7  = props.a4_ctr_flag_7
            attr.flags.flag_8  = props.a4_ctr_flag_8
            attr.flags.flag_9  = props.a4_ctr_flag_9
            attr.flags.flag_10 = props.a4_ctr_flag_10
            attr.flags.flag_11 = props.a4_ctr_flag_11
            attr.flags.flag_12 = props.a4_ctr_flag_12
            attr.flags.flag_13 = props.a4_ctr_flag_13
            attr.flags.flag_14 = props.a4_ctr_flag_14
            attr.flags.flag_15 = props.a4_ctr_flag_15
            
            attr.data.flags.flag_0  = props.a4_flag_0
            attr.data.flags.flag_1  = props.a4_flag_1
            attr.data.flags.flag_2  = props.a4_flag_2
            attr.data.flags.flag_3  = props.a4_flag_3
            attr.data.flags.flag_4  = props.a4_flag_4
            attr.data.flags.flag_5  = props.a4_flag_5
            attr.data.flags.flag_6  = props.a4_flag_6
            attr.data.flags.flag_7  = props.a4_flag_7
            attr.data.flags.flag_8  = props.a4_flag_8
            attr.data.flags.flag_9  = props.a4_flag_9
            attr.data.flags.flag_10 = props.a4_flag_10
            attr.data.flags.flag_11 = props.a4_flag_11
            attr.data.flags.flag_12 = props.a4_flag_12
            attr.data.flags.flag_13 = props.a4_flag_13
            attr.data.flags.flag_14 = props.a4_flag_14
            attr.data.flags.flag_15 = props.a4_flag_15
            attr.data.flags.flag_16 = props.a4_flag_16
            attr.data.flags.flag_17 = props.a4_flag_17
            attr.data.flags.flag_18 = props.a4_flag_18
            attr.data.flags.flag_19 = props.a4_flag_19
            attr.data.flags.flag_20 = props.a4_flag_20
            attr.data.flags.flag_21 = props.a4_flag_21
            attr.data.flags.flag_22 = props.a4_flag_22
            attr.data.flags.flag_23 = props.a4_flag_23
            attr.data.flags.flag_24 = props.a4_flag_24
            attr.data.flags.flag_25 = props.a4_flag_25
            attr.data.flags.flag_26 = props.a4_flag_26
            attr.data.flags.flag_27 = props.a4_flag_27
            attr.data.flags.flag_28 = props.a4_flag_28
            attr.data.flags.flag_29 = props.a4_flag_29
            attr.data.flags.flag_30 = props.a4_flag_30
            attr.data.flags.flag_31 = props.a4_flag_31
        
        # Attribute 5
        if props.has_a5:
            attr = mat.add_attribute_5(
                props.a5_unknown_0x00,
                props.a5_unknown_0x04,
                props.a5_unknown_0x08,
                props.a5_unknown_0x0C,
                props.a5_unknown_0x10,
                props.a5_unknown_0x14,
                props.a5_unknown_0x18,
                props.a5_unknown_0x1C,
                props.a5_unknown_0x20,
                props.a5_unknown_0x24,
                props.a5_unknown_0x28,
                props.a5_unknown_0x2C,
                props.a5_unknown_0x30
            )
            
            attr.flags.flag_0  = props.a5_ctr_flag_0
            attr.flags.flag_1  = props.a5_ctr_flag_1
            attr.flags.flag_2  = props.a5_ctr_flag_2
            attr.flags.flag_3  = props.a5_ctr_flag_3
            attr.flags.flag_4  = props.a5_ctr_flag_4
            attr.flags.flag_5  = props.a5_ctr_flag_5
            attr.flags.flag_6  = props.a5_ctr_flag_6
            attr.flags.flag_7  = props.a5_ctr_flag_7
            attr.flags.flag_8  = props.a5_ctr_flag_8
            attr.flags.flag_9  = props.a5_ctr_flag_9
            attr.flags.flag_10 = props.a5_ctr_flag_10
            attr.flags.flag_11 = props.a5_ctr_flag_11
            attr.flags.flag_12 = props.a5_ctr_flag_12
            attr.flags.flag_13 = props.a5_ctr_flag_13
            attr.flags.flag_14 = props.a5_ctr_flag_14
            attr.flags.flag_15 = props.a5_ctr_flag_15
            
            attr.data.flags.flag_0  = props.a5_flag_0
            attr.data.flags.flag_1  = props.a5_flag_1
            attr.data.flags.flag_2  = props.a5_flag_2
            attr.data.flags.flag_3  = props.a5_flag_3
            attr.data.flags.flag_4  = props.a5_flag_4
            attr.data.flags.flag_5  = props.a5_flag_5
            attr.data.flags.flag_6  = props.a5_flag_6
            attr.data.flags.flag_7  = props.a5_flag_7
            attr.data.flags.flag_8  = props.a5_flag_8
            attr.data.flags.flag_9  = props.a5_flag_9
            attr.data.flags.flag_10 = props.a5_flag_10
            attr.data.flags.flag_11 = props.a5_flag_11
            attr.data.flags.flag_12 = props.a5_flag_12
            attr.data.flags.flag_13 = props.a5_flag_13
            attr.data.flags.flag_14 = props.a5_flag_14
            attr.data.flags.flag_15 = props.a5_flag_15
            attr.data.flags.flag_16 = props.a5_flag_16
            attr.data.flags.flag_17 = props.a5_flag_17
            attr.data.flags.flag_18 = props.a5_flag_18
            attr.data.flags.flag_19 = props.a5_flag_19
            attr.data.flags.flag_20 = props.a5_flag_20
            attr.data.flags.flag_21 = props.a5_flag_21
            attr.data.flags.flag_22 = props.a5_flag_22
            attr.data.flags.flag_23 = props.a5_flag_23
            attr.data.flags.flag_24 = props.a5_flag_24
            attr.data.flags.flag_25 = props.a5_flag_25
            attr.data.flags.flag_26 = props.a5_flag_26
            attr.data.flags.flag_27 = props.a5_flag_27
            attr.data.flags.flag_28 = props.a5_flag_28
            attr.data.flags.flag_29 = props.a5_flag_29
            attr.data.flags.flag_30 = props.a5_flag_30
            attr.data.flags.flag_31 = props.a5_flag_31
        
        # Attribute 6
        if props.has_a6:
            attr = mat.add_attribute_6(
                props.a6_unknown_0x00,
                props.a6_unknown_0x04,
                props.a6_unknown_0x08
            )
            
            attr.flags.flag_0  = props.a6_ctr_flag_0
            attr.flags.flag_1  = props.a6_ctr_flag_1
            attr.flags.flag_2  = props.a6_ctr_flag_2
            attr.flags.flag_3  = props.a6_ctr_flag_3
            attr.flags.flag_4  = props.a6_ctr_flag_4
            attr.flags.flag_5  = props.a6_ctr_flag_5
            attr.flags.flag_6  = props.a6_ctr_flag_6
            attr.flags.flag_7  = props.a6_ctr_flag_7
            attr.flags.flag_8  = props.a6_ctr_flag_8
            attr.flags.flag_9  = props.a6_ctr_flag_9
            attr.flags.flag_10 = props.a6_ctr_flag_10
            attr.flags.flag_11 = props.a6_ctr_flag_11
            attr.flags.flag_12 = props.a6_ctr_flag_12
            attr.flags.flag_13 = props.a6_ctr_flag_13
            attr.flags.flag_14 = props.a6_ctr_flag_14
            attr.flags.flag_15 = props.a6_ctr_flag_15
        
        # Attribute 7
        if props.has_a7:
            attr = mat.add_attribute_7()
            
            attr.flags.flag_0  = props.a7_ctr_flag_0
            attr.flags.flag_1  = props.a7_ctr_flag_1
            attr.flags.flag_2  = props.a7_ctr_flag_2
            attr.flags.flag_3  = props.a7_ctr_flag_3
            attr.flags.flag_4  = props.a7_ctr_flag_4
            attr.flags.flag_5  = props.a7_ctr_flag_5
            attr.flags.flag_6  = props.a7_ctr_flag_6
            attr.flags.flag_7  = props.a7_ctr_flag_7
            attr.flags.flag_8  = props.a7_ctr_flag_8
            attr.flags.flag_9  = props.a7_ctr_flag_9
            attr.flags.flag_10 = props.a7_ctr_flag_10
            attr.flags.flag_11 = props.a7_ctr_flag_11
            attr.flags.flag_12 = props.a7_ctr_flag_12
            attr.flags.flag_13 = props.a7_ctr_flag_13
            attr.flags.flag_14 = props.a7_ctr_flag_14
            attr.flags.flag_15 = props.a7_ctr_flag_15
        
    # Export textures
    if None in texture_names:
        texture_names.remove(None)
    texture_names = sorted(texture_names)
    for texture_name in texture_names:
        export_texture(gfs, texture_name, errorlog)


def export_texture(gfs, texture_name, errorlog):
    # Retreive image data block from Blender
    if texture_name == "dummy" and texture_name not in bpy.data.images:
        gfs.add_texture("dummy", dummy_image_data, 1, 1, 0, 0)
        return
    else:
        bpy_image = bpy.data.images[texture_name]
    
    # Check that the image is a file; if it is then we can just
    # embed it in the model
    # If it isn't... need to convert it to DDS, which we won't support currently
    if bpy_image.type != "FILE" and bpy_image.type != "IMAGE":
        errorlog.log_error(ReportableError(f"Cannot currently export non-file and non-packed textures: {bpy_image.name} {bpy_image.type}"))
    
    # Check if the file is packed in the blend or external;
    # get data depending on which is the case
    image_data = None
    if bpy_image.packed_file is None:
        img_path = os.path.abspath(bpy_image.filepath_raw)
        if len(bpy_image.filepath_raw) and os.path.isfile(img_path):
            with open(bpy_image.filepath_raw, 'rb') as F:
                image_data = F.read()
        else:
            errorlog.log_error(ReportableError(f"Attempted to export image '{bpy_image.name}', but it has an invalid filepath: '{img_path}. You may be able to export if you pack all images into Blender instead of referring to external files.'"))
    else:
        image_data = bpy_image.packed_file.data
        
    # Check that it's a DDS
    # Not sure what to do with non-DDS data currently
    # Should add support later
    if image_data[:4] != b"DDS ":
        errorlog.log_warning_message(f"Attempted to export image '{bpy_image.name}', but it is not a DDS texture. This will be replaced with a dummy texture.")
        image_data = dummy_image_data
    
    tex_names = set(tex.name for tex in gfs.textures)
    if texture_name not in tex_names:
        props = bpy_image.GFSTOOLS_ImageProperties
        gfs.add_texture(texture_name, image_data, props.unknown_1, props.unknown_2, props.unknown_3, props.unknown_4)
    
        
def export_texture_node_data(mat_name, name, nodes, create_sampler, errorlog):
    if name in nodes:
        tex_node = nodes[name]
        if tex_node.type != "TEX_IMAGE":
            errorlog.log_error(f"Node '{name}' on material '{mat_name}' is not an Image Texture node")
            return None
        
        connections = tex_node.inputs["Vector"].links
        
        if tex_node.image is None:
            image_name = "dummy"
            errorlog.log_warning_message(f"No image found for image texture node '{name}' on material '{mat_name}'. Defaulting to a dummy texture.")
        else:
            image_name = tex_node.image.name
        
        tex_idx = None
        if len(connections):
            uv_node = connections[0].from_socket.node
            if uv_node.type == "UVMAP":
                uv_map_name = uv_node.uv_map
                if is_valid_uv_map(uv_map_name):
                    proposed_tex_idx = get_uv_idx_from_name(uv_map_name)
                    if proposed_tex_idx < 8:
                        tex_idx = proposed_tex_idx
                    else:
                        errorlog.log_warning(ReportableWarning(f"Image texture node '{name}' is linked to the UV Map '{uv_map_name}', but this is not a valid UV map name (must be a number between 0-7 prefixed with 'UV', e.g. UV3). Defaulting to UV map 0."))
                else:
                    errorlog.log_warning(ReportableWarning(f"Image texture node '{name}' is linked to the UV Map '{uv_map_name}', but this is not a valid UV map name (must be a number between 0-7 prefixed with 'UV', e.g. UV3). Defaulting to UV map 0."))
            else:
                errorlog.log_warning(ReportableWarning(f"Image texture node '{name}' has an input vector, but it does not come from a UV Map node. Defaulting to UV map 0."))
        else:
            errorlog.log_warning(ReportableWarning(f"Image texture node '{name}' does not have an input UV map. Defaulting to UV map 0."))
        if tex_idx is None:
            tex_idx = 0
            
        # THIS IS WRONG
        # tex_idx_1 and tex_idx_2 CAN BE DIFFERENT IN SOME RARE CASES!!!
        create_sampler(tex_idx, tex_idx, image_name,
            tex_node.GFSTOOLS_TextureRefPanelProperties.enable_anims,
            tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x08,
            tex_node.GFSTOOLS_TextureRefPanelProperties.has_texture_filtering,
            tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x0A,
            tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x0B,
            [
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x0C,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x10,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x14,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x18,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x1C,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x20,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x24,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x28,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x2C,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x30,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x34,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x38,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x3C,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x40,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x44,
                tex_node.GFSTOOLS_TextureRefPanelProperties.unknown_0x48
            ]
        )
        
        return image_name
    return None