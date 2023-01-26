import bpy


class GFSToolsLightProperties(bpy.types.PropertyGroup):
    dtype:  bpy.props.EnumProperty(items=(
            ("TYPE1",      "Type 1",     ""),
            ("SPHERE",     "Sphere",     ""),
            ("HEMISPHERE", "Hemisphere", "")
        ),
        name="Type"
    )
    unk_setting:  bpy.props.BoolProperty(name="Unknown Setting")
    
    color_1: bpy.props.FloatVectorProperty(name="Color 1", size=4)
    color_3: bpy.props.FloatVectorProperty(name="Color 3", size=4)
    
    inner_radius:   bpy.props.FloatProperty(name="Inner Radius")
    outer_radius:   bpy.props.FloatProperty(name="Outer Radius")
    
    # Type 1
    unknown_0x28 : bpy.props.FloatProperty(name="Unknown 0x28")
    unknown_0x2C : bpy.props.FloatProperty(name="Unknown 0x2C")
    unknown_0x30 : bpy.props.FloatProperty(name="Unknown 0x30")
    # Type 2
    unknown_0x34 : bpy.props.FloatProperty(name="Unknown 0x34")
    unknown_0x38 : bpy.props.FloatProperty(name="Unknown 0x38")
    unknown_0x3C : bpy.props.FloatProperty(name="Unknown 0x3C")
    
    unknown_0x48 : bpy.props.FloatProperty(name="Unknown 0x48")
    unknown_0x4C : bpy.props.FloatProperty(name="Unknown 0x4C")
    unknown_0x50 : bpy.props.FloatProperty(name="Unknown 0x50")
    # Type 3
    unknown_0x54 : bpy.props.FloatProperty(name="Unknown 0x54")
    unknown_0x58 : bpy.props.FloatProperty(name="Unknown 0x58")
    unknown_0x5C : bpy.props.FloatProperty(name="Unknown 0x5C")
    
    unknown_0x60 : bpy.props.FloatProperty(name="Unknown 0x60")
    unknown_0x64 : bpy.props.FloatProperty(name="Unknown 0x64")
    unknown_0x68 : bpy.props.FloatProperty(name="Unknown 0x68")
    unknown_0x6C : bpy.props.FloatProperty(name="Unknown 0x6C")
    unknown_0x70 : bpy.props.FloatProperty(name="Unknown 0x70")
    
    unknown_0x7C : bpy.props.FloatProperty(name="Unknown 0x7C")
    unknown_0x80 : bpy.props.FloatProperty(name="Unknown 0x80")
    unknown_0x84 : bpy.props.FloatProperty(name="Unknown 0x84")
    
    flag_0:  bpy.props.BoolProperty(name="Flag 0")
    flag_2:  bpy.props.BoolProperty(name="Flag 2")
    flag_3:  bpy.props.BoolProperty(name="Flag 3")
    flag_4:  bpy.props.BoolProperty(name="Flag 4")
    flag_5:  bpy.props.BoolProperty(name="Flag 5")
    flag_6:  bpy.props.BoolProperty(name="Flag 6")
    flag_7:  bpy.props.BoolProperty(name="Flag 7")
    flag_8:  bpy.props.BoolProperty(name="Flag 8")
    flag_9:  bpy.props.BoolProperty(name="Flag 9")
    flag_10: bpy.props.BoolProperty(name="Flag 10")
    flag_11: bpy.props.BoolProperty(name="Flag 11")
    flag_12: bpy.props.BoolProperty(name="Flag 12")
    flag_13: bpy.props.BoolProperty(name="Flag 13")
    flag_14: bpy.props.BoolProperty(name="Flag 14")
    flag_15: bpy.props.BoolProperty(name="Flag 15")
    flag_16: bpy.props.BoolProperty(name="Flag 16")
    flag_17: bpy.props.BoolProperty(name="Flag 17")
    flag_18: bpy.props.BoolProperty(name="Flag 18")
    flag_19: bpy.props.BoolProperty(name="Flag 19")
    flag_20: bpy.props.BoolProperty(name="Flag 20")
    flag_21: bpy.props.BoolProperty(name="Flag 21")
    flag_22: bpy.props.BoolProperty(name="Flag 22")
    flag_23: bpy.props.BoolProperty(name="Flag 23")
    flag_24: bpy.props.BoolProperty(name="Flag 24")
    flag_25: bpy.props.BoolProperty(name="Flag 25")
    flag_26: bpy.props.BoolProperty(name="Flag 26")
    flag_27: bpy.props.BoolProperty(name="Flag 27")
    flag_28: bpy.props.BoolProperty(name="Flag 28")
    flag_29: bpy.props.BoolProperty(name="Flag 29")
    flag_30: bpy.props.BoolProperty(name="Flag 30")
    flag_31: bpy.props.BoolProperty(name="Flag 31")
