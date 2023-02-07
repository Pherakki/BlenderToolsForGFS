import bpy


class GFSToolsAnimationProperties(bpy.types.PropertyGroup):
    is_blend:   bpy.props.BoolProperty(name="Is Blend", options={"HIDDEN"})
    is_lookat:  bpy.props.BoolProperty(name="Is LookAt", options={"HIDDEN"})
    
    flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0") # Enable node anims?
    flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1") # Enable material anims?
    flag_2:  bpy.props.BoolProperty(name="Unknown Flag 2") # Enable camera anims?
    flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3") # Enable morph anims?
    flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4") # Enable type 5 anims?
    flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5 (Unused?)")
    flag_6:  bpy.props.BoolProperty(name="Unknown Flag 6 (Unused?)")
    flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7 (Unused?)")
    flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8 (Unused?)")
    flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9 (Unused?)")
    flag_10: bpy.props.BoolProperty(name="Unknown Flag 10 (Unused?)")
    flag_11: bpy.props.BoolProperty(name="Unknown Flag 11 (Unused?)")
    flag_12: bpy.props.BoolProperty(name="Unknown Flag 12 (Unused?)")
    flag_13: bpy.props.BoolProperty(name="Unknown Flag 13 (Unused?)")
    flag_14: bpy.props.BoolProperty(name="Unknown Flag 14 (Unused?)")
    flag_15: bpy.props.BoolProperty(name="Unknown Flag 15 (Unused?)")
    flag_16: bpy.props.BoolProperty(name="Unknown Flag 16 (Unused?)")
    flag_17: bpy.props.BoolProperty(name="Unknown Flag 17 (Unused?)")
    flag_18: bpy.props.BoolProperty(name="Unknown Flag 18 (Unused?)")
    flag_19: bpy.props.BoolProperty(name="Unknown Flag 19 (Unused?)")
    flag_20: bpy.props.BoolProperty(name="Unknown Flag 20 (Unused?)")
    flag_21: bpy.props.BoolProperty(name="Unknown Flag 21 (Unused?)")
    flag_22: bpy.props.BoolProperty(name="Unknown Flag 22 (Unused?)")
    flag_24: bpy.props.BoolProperty(name="Unknown Flag 24 (Unused?)")
    flag_26: bpy.props.BoolProperty(name="Unknown Flag 26 (Unused?)")
    flag_27: bpy.props.BoolProperty(name="Unknown Flag 27 (Unused?)")
    
    has_extra_track = bpy.props.BoolProperty(name="Extra Track")
    extra_track_name = bpy.props.StringProperty(name="Extra Track Name")
    
    has_lookat_anims = bpy.props.BoolProperty("LookAt Anims")
    lookat_right = bpy.props.StringProperty(name="LookAt Right")
    lookat_left  = bpy.props.StringProperty(name="LookAt Left")
    lookat_up    = bpy.props.StringProperty(name="LookAt Up")
    lookat_down  = bpy.props.StringProperty(name="LookAt Down")
    lookat_right_factor = bpy.props.FloatProperty(name="LookAt Right Factor")
    lookat_left_factor  = bpy.props.FloatProperty(name="LookAt Left Factor")
    lookat_up_factor    = bpy.props.FloatProperty(name="LookAt Up Factor")
    lookat_down_factor  = bpy.props.FloatProperty(name="LookAt Down Factor")
