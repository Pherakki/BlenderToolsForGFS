import bpy

from .Animations import poll_lookat_action


class NLAStripWrapper(bpy.types.PropertyGroup):
    name:                bpy.props.StringProperty(name="Name", default="New Strip")
    frame_start_ui:      bpy.props.FloatProperty()
    action_frame_start:  bpy.props.FloatProperty()
    action_frame_end:    bpy.props.FloatProperty()
    scale:               bpy.props.FloatProperty()
    repeat:              bpy.props.FloatProperty()
    action: bpy.props.PointerProperty(type=bpy.types.Action)
    

class NLATrackWrapper(bpy.types.PropertyGroup):
    name:   bpy.props.StringProperty(name="Name", default="New Track")
    strips: bpy.props.CollectionProperty(type=NLAStripWrapper)

    
class GFSToolsAnimationPackProperties(bpy.types.PropertyGroup):
    name:    bpy.props.StringProperty(name="Name", default="New Pack")
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
    
    @staticmethod
    def get_active_external_gap(bpy_armature_object):
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        gaps = mprops.external_animation_packs
        current_gap = gaps[mprops.external_animation_pack_idx]
        return current_gap
    
    def store_animation_pack(self, bpy_armature_object):
        gap_props = self
        
        gap_props.animations.clear()
        if bpy_armature_object.animation_data is None:
            return
    
        for nla_track in bpy_armature_object.animation_data.nla_tracks:
            prop_track = gap_props.animations.add()
            prop_track.name = nla_track.name
            
            for nla_strip in nla_track.strips:
                prop_strip = prop_track.strips.add()
                prop_strip.name                = nla_strip.name
                prop_strip.frame_start_ui      = nla_strip.frame_start_ui
                prop_strip.action_frame_start  = nla_strip.action_frame_start
                prop_strip.action_frame_end    = nla_strip.action_frame_end
                prop_strip.scale               = nla_strip.scale
                prop_strip.repeat              = nla_strip.repeat
                prop_strip.action              = nla_strip.action
                
    
    def restore_animation_pack(self, bpy_armature_object):
        gap_props = self
        
        bpy_armature_object.animation_data_clear()
        bpy_armature_object.animation_data_create()
        
        for prop_track in gap_props.animations:
            nla_track = bpy_armature_object.animation_data.nla_tracks.new(name=prop_track.name)
            
            for prop_strip in prop_track.strips:
                nla_strip = nla_track.strips.new(prop_strip.name,
                                                 1,
                                                 prop_strip.action)
                
                nla_strip.frame_start_ui     = prop_strip.frame_start_ui
                nla_strip.action_frame_start = prop_strip.action_frame_start
                nla_strip.action_frame_end   = prop_strip.action_frame_end
                nla_strip.scale              = prop_strip.scale
                nla_strip.repeat             = prop_strip.repeat
