import bpy


class GFSToolsLightProperties(bpy.types.PropertyGroup):
    dtype:  bpy.props.EnumProperty(items=(
            ("TYPE1",      "Type 1",     ""),
            ("SPHERE",     "Sphere",     ""),
            ("HEMISPHERE", "Hemisphere", "")
        ),
        name="Type"
    )
    unk_setting:  bpy.props.BoolProperty(name="Unknown Setting", default=True)
    
    color_1: bpy.props.FloatVectorProperty(name="Color 1", size=4, default=[1., 1., 1., 1.])
    alpha:   bpy.props.FloatProperty(name="Color Alpha", default=1.)
    color_3: bpy.props.FloatVectorProperty(name="Color 3", size=4, default=[1., 1., 1., 1.])
    
    inner_radius:   bpy.props.FloatProperty(name="Inner Radius", default=200.)
    outer_radius:   bpy.props.FloatProperty(name="Outer Radius", default=400.)
    
    # Type 1
    unknown_0x28 : bpy.props.FloatProperty(name="Unknown 0x28", default=0.)
    unknown_0x2C : bpy.props.FloatProperty(name="Unknown 0x2C", default=0.)
    unknown_0x30 : bpy.props.FloatProperty(name="Unknown 0x30", default=1.)
    # Type 2
    unknown_0x34 : bpy.props.FloatProperty(name="Unknown 0x34", default=0.)
    unknown_0x38 : bpy.props.FloatProperty(name="Unknown 0x38", default=0.)
    unknown_0x3C : bpy.props.FloatProperty(name="Unknown 0x3C", default=0.)
    
    unknown_0x48 : bpy.props.FloatProperty(name="Unknown 0x48", default=0.)
    unknown_0x4C : bpy.props.FloatProperty(name="Unknown 0x4C", default=0.)
    unknown_0x50 : bpy.props.FloatProperty(name="Unknown 0x50", default=0.)
    # Type 3
    unknown_0x54 : bpy.props.FloatProperty(name="Unknown 0x54", default=0.)
    unknown_0x58 : bpy.props.FloatProperty(name="Unknown 0x58", default=0.)
    unknown_0x5C : bpy.props.FloatProperty(name="Unknown 0x5C", default=1.)
    
    unknown_0x60 : bpy.props.FloatProperty(name="Unknown 0x60", default=0.1)
    unknown_0x64 : bpy.props.FloatProperty(name="Unknown 0x64", default=0.5)
    unknown_0x68 : bpy.props.FloatProperty(name="Unknown 0x68", default=0.)
    unknown_0x6C : bpy.props.FloatProperty(name="Unknown 0x6C", default=0.)
    unknown_0x70 : bpy.props.FloatProperty(name="Unknown 0x70", default=0.)
    
    unknown_0x7C : bpy.props.FloatProperty(name="Unknown 0x7C", default=0.)
    unknown_0x80 : bpy.props.FloatProperty(name="Unknown 0x80", default=0.)
    unknown_0x84 : bpy.props.FloatProperty(name="Unknown 0x84", default=0.)
    
    flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0",            default=True )
    flag_2:  bpy.props.BoolProperty(name="Unknown Flag 2   (Unused?)", default=False)
    flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3   (Unused?)", default=False)
    flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4   (Unused?)", default=False)
    flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5   (Unused?)", default=False)
    flag_6:  bpy.props.BoolProperty(name="Unknown Flag 6   (Unused?)", default=False)
    flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7   (Unused?)", default=False)
    flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8   (Unused?)", default=False)
    flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9   (Unused?)", default=False)
    flag_10: bpy.props.BoolProperty(name="Unknown Flag 10  (Unused?)", default=False)
    flag_11: bpy.props.BoolProperty(name="Unknown Flag 11  (Unused?)", default=False)
    flag_12: bpy.props.BoolProperty(name="Unknown Flag 12  (Unused?)", default=False)
    flag_13: bpy.props.BoolProperty(name="Unknown Flag 13  (Unused?)", default=False)
    flag_14: bpy.props.BoolProperty(name="Unknown Flag 14  (Unused?)", default=False)
    flag_15: bpy.props.BoolProperty(name="Unknown Flag 15  (Unused?)", default=False)
    flag_16: bpy.props.BoolProperty(name="Unknown Flag 16  (Unused?)", default=False)
    flag_17: bpy.props.BoolProperty(name="Unknown Flag 17  (Unused?)", default=False)
    flag_18: bpy.props.BoolProperty(name="Unknown Flag 18  (Unused?)", default=False)
    flag_19: bpy.props.BoolProperty(name="Unknown Flag 19  (Unused?)", default=False)
    flag_20: bpy.props.BoolProperty(name="Unknown Flag 20  (Unused?)", default=False)
    flag_21: bpy.props.BoolProperty(name="Unknown Flag 21  (Unused?)", default=False)
    flag_22: bpy.props.BoolProperty(name="Unknown Flag 22  (Unused?)", default=False)
    flag_23: bpy.props.BoolProperty(name="Unknown Flag 23  (Unused?)", default=False)
    flag_24: bpy.props.BoolProperty(name="Unknown Flag 24  (Unused?)", default=False)
    flag_25: bpy.props.BoolProperty(name="Unknown Flag 25  (Unused?)", default=False)
    flag_26: bpy.props.BoolProperty(name="Unknown Flag 26  (Unused?)", default=False)
    flag_27: bpy.props.BoolProperty(name="Unknown Flag 27  (Unused?)", default=False)
    flag_28: bpy.props.BoolProperty(name="Unknown Flag 28  (Unused?)", default=False)
    flag_29: bpy.props.BoolProperty(name="Unknown Flag 29  (Unused?)", default=False)
    flag_30: bpy.props.BoolProperty(name="Unknown Flag 30  (Unused?)", default=False)
    flag_31: bpy.props.BoolProperty(name="Unknown Flag 31  (Unused?)", default=False)
