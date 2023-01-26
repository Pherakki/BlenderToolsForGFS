import bpy


class GFSToolsTextureRefPanelProperties(bpy.types.PropertyGroup):
    # def update_unknown_0x04(self, context):
    #     print("UPDATING")
    
    enable_anims: bpy.props.BoolProperty(name="Animatable", default=False)#update=update_unknown_0x04)
    unknown_0x08: bpy.props.IntProperty(default=1)
    has_texture_filtering: bpy.props.BoolProperty(name="Filter Texture", default=True)
    unknown_0x0A: bpy.props.IntProperty(default=0) # 0, 1, 2
    unknown_0x0B: bpy.props.IntProperty(default=0) # 0, 1, 2
    unknown_0x0C: bpy.props.FloatProperty(default=1.) # -1, 0, 1, 1.3, 2, 5
    unknown_0x10: bpy.props.FloatProperty(default=-0.) # -1, 0
    unknown_0x14: bpy.props.FloatProperty(default=0.)
    unknown_0x18: bpy.props.FloatProperty(default=0.)
    unknown_0x1C: bpy.props.FloatProperty(default=0.) # 0, 1
    unknown_0x20: bpy.props.FloatProperty(default=0.) # -1, 0, 1, 2, 4, 5
    unknown_0x24: bpy.props.FloatProperty(default=0.)
    unknown_0x28: bpy.props.FloatProperty(default=0.)
    unknown_0x2C: bpy.props.FloatProperty(default=0.)
    unknown_0x30: bpy.props.FloatProperty(default=0.)
    unknown_0x34: bpy.props.FloatProperty(default=0.)
    unknown_0x38: bpy.props.FloatProperty(default=0.)
    unknown_0x3C: bpy.props.FloatProperty(default=0.)
    unknown_0x40: bpy.props.FloatProperty(default=0.)
    unknown_0x44: bpy.props.FloatProperty(default=0.)
    unknown_0x48: bpy.props.FloatProperty(default=0.)



class GFSToolsMaterialProperties(bpy.types.PropertyGroup):
    flag_0:          bpy.props.BoolProperty(name="Flag 0",               default=True )
    flag_1:          bpy.props.BoolProperty(name="Flag 1",               default=True )
    enable_specular: bpy.props.BoolProperty(name="Enable Specular",      default=False)
    flag_3:          bpy.props.BoolProperty(name="Flag 3",               default=False)
    vertex_colors:   bpy.props.BoolProperty(name="Enable Vertex Colors", default=False)
    flag_5:          bpy.props.BoolProperty(name="Flag 5",               default=True )
    flag_6:          bpy.props.BoolProperty(name="Flag 6",               default=False)
    enable_uv_anims: bpy.props.BoolProperty(name="Enable UV Anims",      default=False)
    enable_emissive: bpy.props.BoolProperty(name="Enable Emissive",      default=False)
    flag_9:          bpy.props.BoolProperty(name="Flag 9",               default=False)
    flag_10:         bpy.props.BoolProperty(name="Flag 10",              default=False)
    light_2:         bpy.props.BoolProperty(name="Use Light 2",          default=True )
    pwire:           bpy.props.BoolProperty(name="Purple Wireframe",     default=False)
    flag_13:         bpy.props.BoolProperty(name="Flag 13",              default=False)
    receive_shadow:  bpy.props.BoolProperty(name="Receive Shadow",       default=False)
    cast_shadow:     bpy.props.BoolProperty(name="Cast Shadow",          default=False)
    flag_17:         bpy.props.BoolProperty(name="Flag 17",              default=False)
    flag_18:         bpy.props.BoolProperty(name="Flag 18",              default=False)
    disable_bloom:   bpy.props.BoolProperty(name="Disable Bloom",        default=False)
    flag_29:         bpy.props.BoolProperty(name="Flag 29",              default=False)
    flag_30:         bpy.props.BoolProperty(name="Flag 30",              default=False)
    flag_31:         bpy.props.BoolProperty(name="Flag 31",              default=False)
    
    ambient:         bpy.props.FloatVectorProperty(name="Ambient Color",  size=4, default=(1., 1., 1., 1.))
    diffuse:         bpy.props.FloatVectorProperty(name="Diffuse Color",  size=4, default=(1., 1., 1., 1.))
    specular:        bpy.props.FloatVectorProperty(name="Specular Color", size=4, default=(1., 1., 1., 1.))
    emissive:        bpy.props.FloatVectorProperty(name="Emissive Color", size=4, default=(1., 1., 1., 1.))
    reflectivity:    bpy.props.FloatProperty(name="Reflectivity", default=0.)
    outline_idx:     bpy.props.FloatProperty(name="Outline Idx.", default=0.)
    draw_method:     bpy.props.IntProperty("Draw Method", default=0, min=0, max=6) # Change to enum later
    unknown_0x51:    bpy.props.BoolProperty("Unknown 0x51", default=True)
    unknown_0x52:    bpy.props.IntProperty("Unknown 0x52", default=0, min=0, max=255)
    unknown_0x53:    bpy.props.BoolProperty("Unknown 0x53", default=True)
    unknown_0x54:    bpy.props.IntProperty("Unknown 0x54", default=0, min=0, max=255)
    unknown_0x55:    bpy.props.IntProperty("Unknown 0x55", default=1, min=1, max=3) # Change to enum later
    unknown_0x56:    bpy.props.IntProperty("Unknown 0x56", default=0, min=0, max=65535) # Some kind of 8-bit flag?!
    unknown_0x58:    bpy.props.IntProperty("Unknown 0x58", default=0, min=0, max=7) # Change to enum later?
    unknown_0x5A:    bpy.props.IntProperty("Unknown 0x5A", default=1, min=-32768, max=32767) # Flags?
    unknown_0x5C:    bpy.props.IntProperty("Unknown 0x5C", default=0, min=-32768, max=32767) # Flags?
    unknown_0x5E:    bpy.props.IntProperty("Unknown 0x5E", default=0, min=-32768, max=32767) # Flags?
    unknown_0x68:    bpy.props.IntProperty("Unknown 0x68", default=0, min=-32768, max=32767) # Never used
    unknown_0x6A:    bpy.props.IntProperty("Unknown 0x6A", default=-1, min=-2147483648, max=2147483647) # Always -1

    ##################
    # TOON ATTRIBUTE #
    ##################
    
    has_toon:  bpy.props.BoolProperty(name="Active")
    
    toon_colour:           bpy.props.FloatVectorProperty(name="Color", default=[1., 1., 1., 1.], size=4)
    toon_light_threshold:  bpy.props.FloatProperty(name="Light Threshold")
    toon_light_factor:     bpy.props.FloatProperty(name="Light Factor")
    toon_light_brightness: bpy.props.FloatProperty(name="Light Brightness")
    toon_shadow_threshold: bpy.props.FloatProperty(name="Shadow Threshold")
    toon_shadow_factor:    bpy.props.FloatProperty(name="Shadow Factor")
    
    toon_ctr_flag_0:  bpy.props.BoolProperty(name="Attr. Flag 0")
    toon_ctr_flag_1:  bpy.props.BoolProperty(name="Attr. Flag 1")
    toon_ctr_flag_2:  bpy.props.BoolProperty(name="Attr. Flag 2")
    toon_ctr_flag_3:  bpy.props.BoolProperty(name="Attr. Flag 3")
    toon_ctr_flag_4:  bpy.props.BoolProperty(name="Attr. Flag 4")
    toon_ctr_flag_5:  bpy.props.BoolProperty(name="Attr. Flag 5")
    toon_ctr_flag_6:  bpy.props.BoolProperty(name="Attr. Flag 6")
    toon_ctr_flag_7:  bpy.props.BoolProperty(name="Attr. Flag 7")
    toon_ctr_flag_8:  bpy.props.BoolProperty(name="Attr. Flag 8")
    toon_ctr_flag_9:  bpy.props.BoolProperty(name="Attr. Flag 9")
    toon_ctr_flag_10: bpy.props.BoolProperty(name="Attr. Flag 10")
    toon_ctr_flag_11: bpy.props.BoolProperty(name="Attr. Flag 11")
    toon_ctr_flag_12: bpy.props.BoolProperty(name="Attr. Flag 12")
    toon_ctr_flag_13: bpy.props.BoolProperty(name="Attr. Flag 13")
    toon_ctr_flag_14: bpy.props.BoolProperty(name="Attr. Flag 14")
    toon_ctr_flag_15: bpy.props.BoolProperty(name="Attr. Flag 15")
    
    toon_flag_0:  bpy.props.BoolProperty(name="Flag 0")
    toon_flag_1:  bpy.props.BoolProperty(name="Flag 1")
    toon_flag_2:  bpy.props.BoolProperty(name="Flag 2")
    toon_flag_3:  bpy.props.BoolProperty(name="Flag 3")
    toon_flag_4:  bpy.props.BoolProperty(name="Flag 4")
    toon_flag_5:  bpy.props.BoolProperty(name="Flag 5")
    toon_flag_6:  bpy.props.BoolProperty(name="Flag 6")
    toon_flag_7:  bpy.props.BoolProperty(name="Flag 7")
    toon_flag_8:  bpy.props.BoolProperty(name="Flag 8")
    toon_flag_9:  bpy.props.BoolProperty(name="Flag 9")
    toon_flag_10: bpy.props.BoolProperty(name="Flag 10")
    toon_flag_11: bpy.props.BoolProperty(name="Flag 11")
    toon_flag_12: bpy.props.BoolProperty(name="Flag 12")
    toon_flag_13: bpy.props.BoolProperty(name="Flag 13")
    toon_flag_14: bpy.props.BoolProperty(name="Flag 14")
    toon_flag_15: bpy.props.BoolProperty(name="Flag 15")
    toon_flag_16: bpy.props.BoolProperty(name="Flag 16")
    toon_flag_17: bpy.props.BoolProperty(name="Flag 17")
    toon_flag_18: bpy.props.BoolProperty(name="Flag 18")
    toon_flag_19: bpy.props.BoolProperty(name="Flag 19")
    toon_flag_20: bpy.props.BoolProperty(name="Flag 20")
    toon_flag_21: bpy.props.BoolProperty(name="Flag 21")
    toon_flag_22: bpy.props.BoolProperty(name="Flag 22")
    toon_flag_23: bpy.props.BoolProperty(name="Flag 23")
    toon_flag_24: bpy.props.BoolProperty(name="Flag 24")
    toon_flag_25: bpy.props.BoolProperty(name="Flag 25")
    toon_flag_26: bpy.props.BoolProperty(name="Flag 26")
    toon_flag_27: bpy.props.BoolProperty(name="Flag 27")
    toon_flag_28: bpy.props.BoolProperty(name="Flag 28")
    toon_flag_29: bpy.props.BoolProperty(name="Flag 29")
    toon_flag_30: bpy.props.BoolProperty(name="Flag 30")
    toon_flag_31: bpy.props.BoolProperty(name="Flag 31")
  
    ####################
    # ATTRIBUTE TYPE 1 #
    ####################
    
    has_a1:  bpy.props.BoolProperty(name="Active")
    
    a1_unknown_0x00:       bpy.props.FloatProperty(name="unknown 0x00")
    a1_unknown_0x04:       bpy.props.FloatProperty(name="unknown 0x04")
    a1_unknown_0x08:       bpy.props.FloatProperty(name="unknown 0x08")
    a1_unknown_0x0C:       bpy.props.FloatProperty(name="unknown 0x0C")
    a1_unknown_0x10:       bpy.props.FloatProperty(name="unknown 0x10")
    a1_unknown_0x14:       bpy.props.FloatProperty(name="unknown 0x14")
    a1_unknown_0x18:       bpy.props.FloatProperty(name="unknown 0x18")
    a1_unknown_0x1C:       bpy.props.FloatProperty(name="unknown 0x1C")
    a1_unknown_0x20:       bpy.props.FloatProperty(name="unknown 0x20")
    a1_unknown_0x24:       bpy.props.FloatProperty(name="unknown 0x24")
    a1_unknown_0x28:       bpy.props.FloatProperty(name="unknown 0x28")
    a1_unknown_0x2C:       bpy.props.FloatProperty(name="unknown 0x2C")
    
    a1_ctr_flag_0:  bpy.props.BoolProperty(name="Attr. Flag 0")
    a1_ctr_flag_1:  bpy.props.BoolProperty(name="Attr. Flag 1")
    a1_ctr_flag_2:  bpy.props.BoolProperty(name="Attr. Flag 2")
    a1_ctr_flag_3:  bpy.props.BoolProperty(name="Attr. Flag 3")
    a1_ctr_flag_4:  bpy.props.BoolProperty(name="Attr. Flag 4")
    a1_ctr_flag_5:  bpy.props.BoolProperty(name="Attr. Flag 5")
    a1_ctr_flag_6:  bpy.props.BoolProperty(name="Attr. Flag 6")
    a1_ctr_flag_7:  bpy.props.BoolProperty(name="Attr. Flag 7")
    a1_ctr_flag_8:  bpy.props.BoolProperty(name="Attr. Flag 8")
    a1_ctr_flag_9:  bpy.props.BoolProperty(name="Attr. Flag 9")
    a1_ctr_flag_10: bpy.props.BoolProperty(name="Attr. Flag 10")
    a1_ctr_flag_11: bpy.props.BoolProperty(name="Attr. Flag 11")
    a1_ctr_flag_12: bpy.props.BoolProperty(name="Attr. Flag 12")
    a1_ctr_flag_13: bpy.props.BoolProperty(name="Attr. Flag 13")
    a1_ctr_flag_14: bpy.props.BoolProperty(name="Attr. Flag 14")
    a1_ctr_flag_15: bpy.props.BoolProperty(name="Attr. Flag 15")
    
    a1_flag_0:  bpy.props.BoolProperty(name="Flag 0")
    a1_flag_1:  bpy.props.BoolProperty(name="Flag 1")
    a1_flag_2:  bpy.props.BoolProperty(name="Flag 2")
    a1_flag_3:  bpy.props.BoolProperty(name="Flag 3")
    a1_flag_4:  bpy.props.BoolProperty(name="Flag 4")
    a1_flag_5:  bpy.props.BoolProperty(name="Flag 5")
    a1_flag_6:  bpy.props.BoolProperty(name="Flag 6")
    a1_flag_7:  bpy.props.BoolProperty(name="Flag 7")
    a1_flag_8:  bpy.props.BoolProperty(name="Flag 8")
    a1_flag_9:  bpy.props.BoolProperty(name="Flag 9")
    a1_flag_10: bpy.props.BoolProperty(name="Flag 10")
    a1_flag_11: bpy.props.BoolProperty(name="Flag 11")
    a1_flag_12: bpy.props.BoolProperty(name="Flag 12")
    a1_flag_13: bpy.props.BoolProperty(name="Flag 13")
    a1_flag_14: bpy.props.BoolProperty(name="Flag 14")
    a1_flag_15: bpy.props.BoolProperty(name="Flag 15")
    a1_flag_16: bpy.props.BoolProperty(name="Flag 16")
    a1_flag_17: bpy.props.BoolProperty(name="Flag 17")
    a1_flag_18: bpy.props.BoolProperty(name="Flag 18")
    a1_flag_19: bpy.props.BoolProperty(name="Flag 19")
    a1_flag_20: bpy.props.BoolProperty(name="Flag 20")
    a1_flag_21: bpy.props.BoolProperty(name="Flag 21")
    a1_flag_22: bpy.props.BoolProperty(name="Flag 22")
    a1_flag_23: bpy.props.BoolProperty(name="Flag 23")
    a1_flag_24: bpy.props.BoolProperty(name="Flag 24")
    a1_flag_25: bpy.props.BoolProperty(name="Flag 25")
    a1_flag_26: bpy.props.BoolProperty(name="Flag 26")
    a1_flag_27: bpy.props.BoolProperty(name="Flag 27")
    a1_flag_28: bpy.props.BoolProperty(name="Flag 28")
    a1_flag_29: bpy.props.BoolProperty(name="Flag 29")
    a1_flag_30: bpy.props.BoolProperty(name="Flag 30")
    a1_flag_31: bpy.props.BoolProperty(name="Flag 31")
    
    #####################
    # OUTLINE ATTRIBUTE #
    #####################
    has_outline:   bpy.props.BoolProperty(name="Active")
    # Should replace outline_type with an enum when all types are known
    # These should also have a max of 2**32 - 1, but blender doesn't offer
    # an unsigned int type
    outline_type:  bpy.props.IntProperty(name="Type",  min=0, max=(2**31) - 1)
    outline_color: bpy.props.IntProperty(name="Color", min=0, max=(2**31) - 1)
    
    outline_ctr_flag_0:  bpy.props.BoolProperty(name="Attr. Flag 0")
    outline_ctr_flag_1:  bpy.props.BoolProperty(name="Attr. Flag 1")
    outline_ctr_flag_2:  bpy.props.BoolProperty(name="Attr. Flag 2")
    outline_ctr_flag_3:  bpy.props.BoolProperty(name="Attr. Flag 3")
    outline_ctr_flag_4:  bpy.props.BoolProperty(name="Attr. Flag 4")
    outline_ctr_flag_5:  bpy.props.BoolProperty(name="Attr. Flag 5")
    outline_ctr_flag_6:  bpy.props.BoolProperty(name="Attr. Flag 6")
    outline_ctr_flag_7:  bpy.props.BoolProperty(name="Attr. Flag 7")
    outline_ctr_flag_8:  bpy.props.BoolProperty(name="Attr. Flag 8")
    outline_ctr_flag_9:  bpy.props.BoolProperty(name="Attr. Flag 9")
    outline_ctr_flag_10: bpy.props.BoolProperty(name="Attr. Flag 10")
    outline_ctr_flag_11: bpy.props.BoolProperty(name="Attr. Flag 11")
    outline_ctr_flag_12: bpy.props.BoolProperty(name="Attr. Flag 12")
    outline_ctr_flag_13: bpy.props.BoolProperty(name="Attr. Flag 13")
    outline_ctr_flag_14: bpy.props.BoolProperty(name="Attr. Flag 14")
    outline_ctr_flag_15: bpy.props.BoolProperty(name="Attr. Flag 15")
    
    ####################
    # ATTRIBUTE TYPE 3 #
    ####################
    
    has_a3:  bpy.props.BoolProperty(name="Active")
    
    a3_unknown_0x00:       bpy.props.FloatProperty(name="unknown 0x00")
    a3_unknown_0x04:       bpy.props.FloatProperty(name="unknown 0x04")
    a3_unknown_0x08:       bpy.props.FloatProperty(name="unknown 0x08")
    a3_unknown_0x0C:       bpy.props.FloatProperty(name="unknown 0x0C")
    a3_unknown_0x10:       bpy.props.FloatProperty(name="unknown 0x10")
    a3_unknown_0x14:       bpy.props.FloatProperty(name="unknown 0x14")
    a3_unknown_0x18:       bpy.props.FloatProperty(name="unknown 0x18")
    a3_unknown_0x1C:       bpy.props.FloatProperty(name="unknown 0x1C")
    a3_unknown_0x20:       bpy.props.FloatProperty(name="unknown 0x20")
    a3_unknown_0x24:       bpy.props.FloatProperty(name="unknown 0x24")
    a3_unknown_0x28:       bpy.props.FloatProperty(name="unknown 0x28")
    a3_unknown_0x2C:       bpy.props.FloatProperty(name="unknown 0x2C")
    
    a3_ctr_flag_0:  bpy.props.BoolProperty(name="Attr. Flag 0")
    a3_ctr_flag_1:  bpy.props.BoolProperty(name="Attr. Flag 1")
    a3_ctr_flag_2:  bpy.props.BoolProperty(name="Attr. Flag 2")
    a3_ctr_flag_3:  bpy.props.BoolProperty(name="Attr. Flag 3")
    a3_ctr_flag_4:  bpy.props.BoolProperty(name="Attr. Flag 4")
    a3_ctr_flag_5:  bpy.props.BoolProperty(name="Attr. Flag 5")
    a3_ctr_flag_6:  bpy.props.BoolProperty(name="Attr. Flag 6")
    a3_ctr_flag_7:  bpy.props.BoolProperty(name="Attr. Flag 7")
    a3_ctr_flag_8:  bpy.props.BoolProperty(name="Attr. Flag 8")
    a3_ctr_flag_9:  bpy.props.BoolProperty(name="Attr. Flag 9")
    a3_ctr_flag_10: bpy.props.BoolProperty(name="Attr. Flag 10")
    a3_ctr_flag_11: bpy.props.BoolProperty(name="Attr. Flag 11")
    a3_ctr_flag_12: bpy.props.BoolProperty(name="Attr. Flag 12")
    a3_ctr_flag_13: bpy.props.BoolProperty(name="Attr. Flag 13")
    a3_ctr_flag_14: bpy.props.BoolProperty(name="Attr. Flag 14")
    a3_ctr_flag_15: bpy.props.BoolProperty(name="Attr. Flag 15")
    
    a3_flag_0:  bpy.props.BoolProperty(name="Flag 0")
    a3_flag_1:  bpy.props.BoolProperty(name="Flag 1")
    a3_flag_2:  bpy.props.BoolProperty(name="Flag 2")
    a3_flag_3:  bpy.props.BoolProperty(name="Flag 3")
    a3_flag_4:  bpy.props.BoolProperty(name="Flag 4")
    a3_flag_5:  bpy.props.BoolProperty(name="Flag 5")
    a3_flag_6:  bpy.props.BoolProperty(name="Flag 6")
    a3_flag_7:  bpy.props.BoolProperty(name="Flag 7")
    a3_flag_8:  bpy.props.BoolProperty(name="Flag 8")
    a3_flag_9:  bpy.props.BoolProperty(name="Flag 9")
    a3_flag_10: bpy.props.BoolProperty(name="Flag 10")
    a3_flag_11: bpy.props.BoolProperty(name="Flag 11")
    a3_flag_12: bpy.props.BoolProperty(name="Flag 12")
    a3_flag_13: bpy.props.BoolProperty(name="Flag 13")
    a3_flag_14: bpy.props.BoolProperty(name="Flag 14")
    a3_flag_15: bpy.props.BoolProperty(name="Flag 15")
    a3_flag_16: bpy.props.BoolProperty(name="Flag 16")
    a3_flag_17: bpy.props.BoolProperty(name="Flag 17")
    a3_flag_18: bpy.props.BoolProperty(name="Flag 18")
    a3_flag_19: bpy.props.BoolProperty(name="Flag 19")
    a3_flag_20: bpy.props.BoolProperty(name="Flag 20")
    a3_flag_21: bpy.props.BoolProperty(name="Flag 21")
    a3_flag_22: bpy.props.BoolProperty(name="Flag 22")
    a3_flag_23: bpy.props.BoolProperty(name="Flag 23")
    a3_flag_24: bpy.props.BoolProperty(name="Flag 24")
    a3_flag_25: bpy.props.BoolProperty(name="Flag 25")
    a3_flag_26: bpy.props.BoolProperty(name="Flag 26")
    a3_flag_27: bpy.props.BoolProperty(name="Flag 27")
    a3_flag_28: bpy.props.BoolProperty(name="Flag 28")
    a3_flag_29: bpy.props.BoolProperty(name="Flag 29")
    a3_flag_30: bpy.props.BoolProperty(name="Flag 30")
    a3_flag_31: bpy.props.BoolProperty(name="Flag 31")
    
    ####################
    # ATTRIBUTE TYPE 4 #
    ####################
    
    has_a4:  bpy.props.BoolProperty(name="Active")
    
    a4_unknown_0x00:       bpy.props.FloatProperty(name="unknown 0x00")
    a4_unknown_0x04:       bpy.props.FloatProperty(name="unknown 0x04")
    a4_unknown_0x08:       bpy.props.FloatProperty(name="unknown 0x08")
    a4_unknown_0x0C:       bpy.props.FloatProperty(name="unknown 0x0C")
    a4_unknown_0x10:       bpy.props.FloatProperty(name="unknown 0x10")
    a4_unknown_0x14:       bpy.props.FloatProperty(name="unknown 0x14")
    a4_unknown_0x18:       bpy.props.FloatProperty(name="unknown 0x18")
    a4_unknown_0x1C:       bpy.props.FloatProperty(name="unknown 0x1C")
    a4_unknown_0x20:       bpy.props.FloatProperty(name="unknown 0x20")
    a4_unknown_0x24:       bpy.props.FloatProperty(name="unknown 0x24")
    a4_unknown_0x28:       bpy.props.FloatProperty(name="unknown 0x28")
    a4_unknown_0x2C:       bpy.props.FloatProperty(name="unknown 0x2C")
    a4_unknown_0x30:       bpy.props.FloatProperty(name="unknown 0x30")
    a4_unknown_0x34:       bpy.props.FloatProperty(name="unknown 0x34")
    a4_unknown_0x38:       bpy.props.FloatProperty(name="unknown 0x38")
    a4_unknown_0x3C:       bpy.props.FloatProperty(name="unknown 0x3C")
    a4_unknown_0x40:       bpy.props.FloatProperty(name="unknown 0x40")
    a4_unknown_0x44:       bpy.props.IntProperty(name="unknown 0x44", min=0, max=(2**8 - 1))
    a4_unknown_0x45:       bpy.props.FloatProperty(name="unknown 0x45")
    a4_unknown_0x49:       bpy.props.FloatProperty(name="unknown 0x49")
    
    a4_ctr_flag_0:  bpy.props.BoolProperty(name="Attr. Flag 0")
    a4_ctr_flag_1:  bpy.props.BoolProperty(name="Attr. Flag 1")
    a4_ctr_flag_2:  bpy.props.BoolProperty(name="Attr. Flag 2")
    a4_ctr_flag_3:  bpy.props.BoolProperty(name="Attr. Flag 3")
    a4_ctr_flag_4:  bpy.props.BoolProperty(name="Attr. Flag 4")
    a4_ctr_flag_5:  bpy.props.BoolProperty(name="Attr. Flag 5")
    a4_ctr_flag_6:  bpy.props.BoolProperty(name="Attr. Flag 6")
    a4_ctr_flag_7:  bpy.props.BoolProperty(name="Attr. Flag 7")
    a4_ctr_flag_8:  bpy.props.BoolProperty(name="Attr. Flag 8")
    a4_ctr_flag_9:  bpy.props.BoolProperty(name="Attr. Flag 9")
    a4_ctr_flag_10: bpy.props.BoolProperty(name="Attr. Flag 10")
    a4_ctr_flag_11: bpy.props.BoolProperty(name="Attr. Flag 11")
    a4_ctr_flag_12: bpy.props.BoolProperty(name="Attr. Flag 12")
    a4_ctr_flag_13: bpy.props.BoolProperty(name="Attr. Flag 13")
    a4_ctr_flag_14: bpy.props.BoolProperty(name="Attr. Flag 14")
    a4_ctr_flag_15: bpy.props.BoolProperty(name="Attr. Flag 15")
    
    a4_flag_0:  bpy.props.BoolProperty(name="Flag 0")
    a4_flag_1:  bpy.props.BoolProperty(name="Flag 1")
    a4_flag_2:  bpy.props.BoolProperty(name="Flag 2")
    a4_flag_3:  bpy.props.BoolProperty(name="Flag 3")
    a4_flag_4:  bpy.props.BoolProperty(name="Flag 4")
    a4_flag_5:  bpy.props.BoolProperty(name="Flag 5")
    a4_flag_6:  bpy.props.BoolProperty(name="Flag 6")
    a4_flag_7:  bpy.props.BoolProperty(name="Flag 7")
    a4_flag_8:  bpy.props.BoolProperty(name="Flag 8")
    a4_flag_9:  bpy.props.BoolProperty(name="Flag 9")
    a4_flag_10: bpy.props.BoolProperty(name="Flag 10")
    a4_flag_11: bpy.props.BoolProperty(name="Flag 11")
    a4_flag_12: bpy.props.BoolProperty(name="Flag 12")
    a4_flag_13: bpy.props.BoolProperty(name="Flag 13")
    a4_flag_14: bpy.props.BoolProperty(name="Flag 14")
    a4_flag_15: bpy.props.BoolProperty(name="Flag 15")
    a4_flag_16: bpy.props.BoolProperty(name="Flag 16")
    a4_flag_17: bpy.props.BoolProperty(name="Flag 17")
    a4_flag_18: bpy.props.BoolProperty(name="Flag 18")
    a4_flag_19: bpy.props.BoolProperty(name="Flag 19")
    a4_flag_20: bpy.props.BoolProperty(name="Flag 20")
    a4_flag_21: bpy.props.BoolProperty(name="Flag 21")
    a4_flag_22: bpy.props.BoolProperty(name="Flag 22")
    a4_flag_23: bpy.props.BoolProperty(name="Flag 23")
    a4_flag_24: bpy.props.BoolProperty(name="Flag 24")
    a4_flag_25: bpy.props.BoolProperty(name="Flag 25")
    a4_flag_26: bpy.props.BoolProperty(name="Flag 26")
    a4_flag_27: bpy.props.BoolProperty(name="Flag 27")
    a4_flag_28: bpy.props.BoolProperty(name="Flag 28")
    a4_flag_29: bpy.props.BoolProperty(name="Flag 29")
    a4_flag_30: bpy.props.BoolProperty(name="Flag 30")
    a4_flag_31: bpy.props.BoolProperty(name="Flag 31")
    
    ####################
    # ATTRIBUTE TYPE 5 #
    ####################
    
    has_a5:  bpy.props.BoolProperty(name="Active")
    
    a5_unknown_0x00:       bpy.props.IntProperty(name="unknown 0x00")
    a5_unknown_0x04:       bpy.props.IntProperty(name="unknown 0x04")
    a5_unknown_0x08:       bpy.props.FloatProperty(name="unknown 0x08")
    a5_unknown_0x0C:       bpy.props.FloatProperty(name="unknown 0x0C")
    a5_unknown_0x10:       bpy.props.FloatProperty(name="unknown 0x10")
    a5_unknown_0x14:       bpy.props.FloatProperty(name="unknown 0x14")
    a5_unknown_0x18:       bpy.props.FloatProperty(name="unknown 0x18")
    a5_unknown_0x1C:       bpy.props.FloatProperty(name="unknown 0x1C")
    a5_unknown_0x20:       bpy.props.FloatProperty(name="unknown 0x20")
    a5_unknown_0x24:       bpy.props.FloatProperty(name="unknown 0x24")
    a5_unknown_0x28:       bpy.props.FloatProperty(name="unknown 0x28")
    a5_unknown_0x2C:       bpy.props.FloatProperty(name="unknown 0x2C")
    a5_unknown_0x30:       bpy.props.FloatProperty(name="unknown 0x30")
    
    a5_ctr_flag_0:  bpy.props.BoolProperty(name="Attr. Flag 0")
    a5_ctr_flag_1:  bpy.props.BoolProperty(name="Attr. Flag 1")
    a5_ctr_flag_2:  bpy.props.BoolProperty(name="Attr. Flag 2")
    a5_ctr_flag_3:  bpy.props.BoolProperty(name="Attr. Flag 3")
    a5_ctr_flag_4:  bpy.props.BoolProperty(name="Attr. Flag 4")
    a5_ctr_flag_5:  bpy.props.BoolProperty(name="Attr. Flag 5")
    a5_ctr_flag_6:  bpy.props.BoolProperty(name="Attr. Flag 6")
    a5_ctr_flag_7:  bpy.props.BoolProperty(name="Attr. Flag 7")
    a5_ctr_flag_8:  bpy.props.BoolProperty(name="Attr. Flag 8")
    a5_ctr_flag_9:  bpy.props.BoolProperty(name="Attr. Flag 9")
    a5_ctr_flag_10: bpy.props.BoolProperty(name="Attr. Flag 10")
    a5_ctr_flag_11: bpy.props.BoolProperty(name="Attr. Flag 11")
    a5_ctr_flag_12: bpy.props.BoolProperty(name="Attr. Flag 12")
    a5_ctr_flag_13: bpy.props.BoolProperty(name="Attr. Flag 13")
    a5_ctr_flag_14: bpy.props.BoolProperty(name="Attr. Flag 14")
    a5_ctr_flag_15: bpy.props.BoolProperty(name="Attr. Flag 15")
    
    a5_flag_0:  bpy.props.BoolProperty(name="Flag 0")
    a5_flag_1:  bpy.props.BoolProperty(name="Flag 1")
    a5_flag_2:  bpy.props.BoolProperty(name="Flag 2")
    a5_flag_3:  bpy.props.BoolProperty(name="Flag 3")
    a5_flag_4:  bpy.props.BoolProperty(name="Flag 4")
    a5_flag_5:  bpy.props.BoolProperty(name="Flag 5")
    a5_flag_6:  bpy.props.BoolProperty(name="Flag 6")
    a5_flag_7:  bpy.props.BoolProperty(name="Flag 7")
    a5_flag_8:  bpy.props.BoolProperty(name="Flag 8")
    a5_flag_9:  bpy.props.BoolProperty(name="Flag 9")
    a5_flag_10: bpy.props.BoolProperty(name="Flag 10")
    a5_flag_11: bpy.props.BoolProperty(name="Flag 11")
    a5_flag_12: bpy.props.BoolProperty(name="Flag 12")
    a5_flag_13: bpy.props.BoolProperty(name="Flag 13")
    a5_flag_14: bpy.props.BoolProperty(name="Flag 14")
    a5_flag_15: bpy.props.BoolProperty(name="Flag 15")
    a5_flag_16: bpy.props.BoolProperty(name="Flag 16")
    a5_flag_17: bpy.props.BoolProperty(name="Flag 17")
    a5_flag_18: bpy.props.BoolProperty(name="Flag 18")
    a5_flag_19: bpy.props.BoolProperty(name="Flag 19")
    a5_flag_20: bpy.props.BoolProperty(name="Flag 20")
    a5_flag_21: bpy.props.BoolProperty(name="Flag 21")
    a5_flag_22: bpy.props.BoolProperty(name="Flag 22")
    a5_flag_23: bpy.props.BoolProperty(name="Flag 23")
    a5_flag_24: bpy.props.BoolProperty(name="Flag 24")
    a5_flag_25: bpy.props.BoolProperty(name="Flag 25")
    a5_flag_26: bpy.props.BoolProperty(name="Flag 26")
    a5_flag_27: bpy.props.BoolProperty(name="Flag 27")
    a5_flag_28: bpy.props.BoolProperty(name="Flag 28")
    a5_flag_29: bpy.props.BoolProperty(name="Flag 29")
    a5_flag_30: bpy.props.BoolProperty(name="Flag 30")
    a5_flag_31: bpy.props.BoolProperty(name="Flag 31")
    
    ####################
    # ATTRIBUTE TYPE 6 #
    ####################
    
    has_a6:  bpy.props.BoolProperty(name="Active")
    
    a6_unknown_0x00:       bpy.props.IntProperty(name="unknown 0x00")
    a6_unknown_0x04:       bpy.props.IntProperty(name="unknown 0x04")
    a6_unknown_0x08:       bpy.props.IntProperty(name="unknown 0x08")
    
    a6_ctr_flag_0:  bpy.props.BoolProperty(name="Attr. Flag 0")
    a6_ctr_flag_1:  bpy.props.BoolProperty(name="Attr. Flag 1")
    a6_ctr_flag_2:  bpy.props.BoolProperty(name="Attr. Flag 2")
    a6_ctr_flag_3:  bpy.props.BoolProperty(name="Attr. Flag 3")
    a6_ctr_flag_4:  bpy.props.BoolProperty(name="Attr. Flag 4")
    a6_ctr_flag_5:  bpy.props.BoolProperty(name="Attr. Flag 5")
    a6_ctr_flag_6:  bpy.props.BoolProperty(name="Attr. Flag 6")
    a6_ctr_flag_7:  bpy.props.BoolProperty(name="Attr. Flag 7")
    a6_ctr_flag_8:  bpy.props.BoolProperty(name="Attr. Flag 8")
    a6_ctr_flag_9:  bpy.props.BoolProperty(name="Attr. Flag 9")
    a6_ctr_flag_10: bpy.props.BoolProperty(name="Attr. Flag 10")
    a6_ctr_flag_11: bpy.props.BoolProperty(name="Attr. Flag 11")
    a6_ctr_flag_12: bpy.props.BoolProperty(name="Attr. Flag 12")
    a6_ctr_flag_13: bpy.props.BoolProperty(name="Attr. Flag 13")
    a6_ctr_flag_14: bpy.props.BoolProperty(name="Attr. Flag 14")
    a6_ctr_flag_15: bpy.props.BoolProperty(name="Attr. Flag 15")
    
    ####################
    # ATTRIBUTE TYPE 7 #
    ####################
    
    has_a7:  bpy.props.BoolProperty(name="Active")
    
    a7_ctr_flag_0:  bpy.props.BoolProperty(name="Attr. Flag 0")
    a7_ctr_flag_1:  bpy.props.BoolProperty(name="Attr. Flag 1")
    a7_ctr_flag_2:  bpy.props.BoolProperty(name="Attr. Flag 2")
    a7_ctr_flag_3:  bpy.props.BoolProperty(name="Attr. Flag 3")
    a7_ctr_flag_4:  bpy.props.BoolProperty(name="Attr. Flag 4")
    a7_ctr_flag_5:  bpy.props.BoolProperty(name="Attr. Flag 5")
    a7_ctr_flag_6:  bpy.props.BoolProperty(name="Attr. Flag 6")
    a7_ctr_flag_7:  bpy.props.BoolProperty(name="Attr. Flag 7")
    a7_ctr_flag_8:  bpy.props.BoolProperty(name="Attr. Flag 8")
    a7_ctr_flag_9:  bpy.props.BoolProperty(name="Attr. Flag 9")
    a7_ctr_flag_10: bpy.props.BoolProperty(name="Attr. Flag 10")
    a7_ctr_flag_11: bpy.props.BoolProperty(name="Attr. Flag 11")
    a7_ctr_flag_12: bpy.props.BoolProperty(name="Attr. Flag 12")
    a7_ctr_flag_13: bpy.props.BoolProperty(name="Attr. Flag 13")
    a7_ctr_flag_14: bpy.props.BoolProperty(name="Attr. Flag 14")
    a7_ctr_flag_15: bpy.props.BoolProperty(name="Attr. Flag 15")
