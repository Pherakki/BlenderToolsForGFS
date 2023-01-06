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


        # Register currently-unrepresentable data
        # Can hopefully remove a few of these when a standardised material
        # shader node tree can be built...
        bpy_material.GFSTOOLS_MaterialProperties.flag_0 = mat.flag_0
        bpy_material.GFSTOOLS_MaterialProperties.flag_1 = mat.flag_1
        bpy_material.GFSTOOLS_MaterialProperties.flag_2 = mat.flag_2
        bpy_material.GFSTOOLS_MaterialProperties.vertex_colors = mat.use_vertex_colors
        bpy_material.GFSTOOLS_MaterialProperties.flag_5 = mat.flag_5
        bpy_material.GFSTOOLS_MaterialProperties.flag_6 = mat.flag_6
        bpy_material.GFSTOOLS_MaterialProperties.light_1 = mat.use_light_1
        bpy_material.GFSTOOLS_MaterialProperties.flag_8 = mat.flag_8
        bpy_material.GFSTOOLS_MaterialProperties.flag_9 = mat.flag_9
        bpy_material.GFSTOOLS_MaterialProperties.flag_10 = mat.flag_10
        bpy_material.GFSTOOLS_MaterialProperties.light_2 = mat.use_light_2
        bpy_material.GFSTOOLS_MaterialProperties.pwire = mat.purple_wireframe
        bpy_material.GFSTOOLS_MaterialProperties.flag_13 = mat.flag_13
        bpy_material.GFSTOOLS_MaterialProperties.receive_shadow = mat.receive_shadow
        bpy_material.GFSTOOLS_MaterialProperties.cast_shadow = mat.cast_shadow
        bpy_material.GFSTOOLS_MaterialProperties.flag_17 = mat.flag_17
        bpy_material.GFSTOOLS_MaterialProperties.flag_18 = mat.flag_18
        bpy_material.GFSTOOLS_MaterialProperties.disable_bloom = mat.disable_bloom
        bpy_material.GFSTOOLS_MaterialProperties.flag_29 = mat.flag_29
        bpy_material.GFSTOOLS_MaterialProperties.flag_30 = mat.flag_30
        bpy_material.GFSTOOLS_MaterialProperties.flag_31 = mat.flag_31
        
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

def add_texture_to_material_node(bpy_material, name, texture):
    nodes = bpy_material.node_tree.nodes
    if texture is not None:
        node = nodes.new('ShaderNodeTexImage')
        node.name = name
        node.label = name
        node.image = bpy.data.images[texture.name.string]
        
        # node["GFSTOOLS_unknown_0x04"] = texture.unknown_0x04
        # node["GFSTOOLS_unknown_0x08"] = texture.unknown_0x08
        # node["GFSTOOLS_has_texture_filtering"] = texture.has_texture_filtering
        # node["GFSTOOLS_unknown_0x0A"] = texture.unknown_0x0A
        # node["GFSTOOLS_unknown_0x0B"] = texture.unknown_0x0B
        # node["GFSTOOLS_unknown_0x0C"] = texture.unknown_0x0C
        
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x04 = texture.unknown_0x04
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x08 = texture.unknown_0x08
        node.GFSTOOLS_TextureRefPanelProperties.has_texture_filtering = texture.has_texture_filtering
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x0A = texture.unknown_0x0A
        node.GFSTOOLS_TextureRefPanelProperties.unknown_0x0B = texture.unknown_0x0B
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
        
        return node
    return None
