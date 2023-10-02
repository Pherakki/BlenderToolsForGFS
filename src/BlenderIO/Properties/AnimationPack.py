import bpy

from .Animations import poll_lookat_action


class NLAStripWrapper(bpy.types.PropertyGroup):
    start_frame: bpy.props.IntProperty()
    clip_start:  bpy.props.IntProperty()
    clip_end:    bpy.props.IntProperty()
    action: bpy.props.PointerProperty(type=bpy.types.Action)
    

class NLATrackWrapper(bpy.types.PropertyGroup):
    strips: bpy.props.CollectionProperty(type=NLAStripWrapper)

    
class GFSToolsAnimationPackProperties(bpy.types.PropertyGroup):
    flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0 (Unused?)")
    flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1 (Unused?)")
    flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3") # Enable morph anims?
    flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4 (Unused?)")
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
    flag_23: bpy.props.BoolProperty(name="Unknown Flag 23 (Unused?)")
    flag_24: bpy.props.BoolProperty(name="Unknown Flag 24 (Unused?)")
    flag_25: bpy.props.BoolProperty(name="Unknown Flag 25 (Unused?)")
    flag_26: bpy.props.BoolProperty(name="Unknown Flag 26 (Unused?)")
    flag_27: bpy.props.BoolProperty(name="Unknown Flag 27 (Unused?)")
    flag_28: bpy.props.BoolProperty(name="Unknown Flag 28 (Unused?)")
    flag_29: bpy.props.BoolProperty(name="Unknown Flag 29 (Unused?)")
    flag_30: bpy.props.BoolProperty(name="Unknown Flag 30 (Unused?)")
    flag_31: bpy.props.BoolProperty(name="Unknown Flag 31 (Unused?)")
    
    has_lookat_anims: bpy.props.BoolProperty(name="Has LookAt Anims")
    lookat_right:        bpy.props.PointerProperty(name="LookAt Right", type=bpy.types.Action, poll=poll_lookat_action)
    lookat_left:         bpy.props.PointerProperty(name="LookAt Left",  type=bpy.types.Action, poll=poll_lookat_action)
    lookat_up:           bpy.props.PointerProperty(name="LookAt Up",    type=bpy.types.Action, poll=poll_lookat_action)
    lookat_down:         bpy.props.PointerProperty(name="LookAt Down",  type=bpy.types.Action, poll=poll_lookat_action)
    lookat_right_factor: bpy.props.FloatProperty(name="LookAt Right Factor")
    lookat_left_factor:  bpy.props.FloatProperty(name="LookAt Left Factor")
    lookat_up_factor:    bpy.props.FloatProperty(name="LookAt Up Factor")
    lookat_down_factor:  bpy.props.FloatProperty(name="LookAt Down Factor")

    animations: bpy.props.CollectionProperty(type=NLATrackWrapper)
