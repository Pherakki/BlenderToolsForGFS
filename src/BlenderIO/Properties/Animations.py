import bpy

from .GFSProperties import GFSToolsGenericProperty

    
def find_anims_of_type(self, context, anim_type):
    if context.active_object is None:
        return []
    if context.active_object.type != "ARMATURE":
        return []
    if context.active_object.animation_data is None:
        return []
    
    out = []
    for track in context.active_object.animation_data.nla_tracks:
        if len(track.strips) == 0:
            continue
        
        strip = track.strips[0]
        props = strip.action.GFSTOOLS_AnimationProperties
        if props.category == anim_type:
            out.append((track.name, track.name, ""))
    return out


def find_blendscales(self, context):
    return find_anims_of_type(self, context, "BLENDSCALE")

def find_lookats(self, context):
    return find_anims_of_type(self, context, "LOOKAT")

def update_category(self, context):
    if context.active_nla_strip is None:
        return
    
    action = context.active_nla_strip.action
    props = action.GFSTOOLS_AnimationProperties
    
    if props.autocorrect_action:
        print("TODO: UPDATE THE CATEGORY!")
        
class GFSToolsAnimationProperties(bpy.types.PropertyGroup):   
    autocorrect_action: bpy.props.BoolProperty(name="Auto-correct Actions", 
                                               description="Automatically set the keyframe interpolation and strip blending that will show how the animations looks in-game when selecting a category for the animation",
                                               default=False)
    category: bpy.props.EnumProperty(items=[
            ("NORMAL",     "Normal",      "Standard Animation"                                             ),
            ("BLEND",      "Blend",       "Animations combined channel-by-channel with Standard Animations"),
            ("BLENDSCALE", "Blend Scale", "Scale animations to be added to a Standard Animation scale"     ),
            ("LOOKAT",     "Look At",     "Special Blend animations used for looking up/down/left/right"   )
        ],
        update=update_category
    )

    
    # Common properties
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
    
    unimported_tracks: bpy.props.StringProperty(name="HiddenUnimportedTracks", default="", options={"HIDDEN"})
    
    # Only for Normal animations
    has_lookat_anims:    bpy.props.BoolProperty("LookAt Anims")
    lookat_right:        bpy.props.EnumProperty(name="LookAt Right", items=find_lookats)
    lookat_left:         bpy.props.EnumProperty(name="LookAt Left",  items=find_lookats)
    lookat_up:           bpy.props.EnumProperty(name="LookAt Up",    items=find_lookats)
    lookat_down:         bpy.props.EnumProperty(name="LookAt Down",  items=find_lookats)
    lookat_right_factor: bpy.props.FloatProperty(name="LookAt Right Factor")
    lookat_left_factor:  bpy.props.FloatProperty(name="LookAt Left Factor")
    lookat_up_factor:    bpy.props.FloatProperty(name="LookAt Up Factor")
    lookat_down_factor:  bpy.props.FloatProperty(name="LookAt Down Factor")
    
    # Only for Blend and LookAt animations
    has_scale_action:   bpy.props.BoolProperty("Has Scale Channel")
    blend_scale_action: bpy.props.EnumProperty(name="Scale Channel", items=find_blendscales)

    properties:          bpy.props.CollectionProperty(name="Properties", type=GFSToolsGenericProperty)
    active_property_idx: bpy.props.IntProperty(options={'HIDDEN'})
