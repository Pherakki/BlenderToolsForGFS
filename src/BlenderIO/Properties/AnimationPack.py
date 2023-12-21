from collections import defaultdict

import bpy

from ..Preferences import get_preferences
from .Animations import poll_lookat_action
from ..modelUtilsTest.Misc.ID import new_unique_name
from .MixIns.Version import GFSVersionedProperty
from .GFSProperties import GFSToolsGenericProperty
from .Animations import BlobProperty, AnimBoundingBoxProps
from ..Utils.Animation import gapnames_from_nlatrack, gapnames_to_nlatrack, is_anim_restpose


class NLAStripWrapper(bpy.types.PropertyGroup):
    name:                bpy.props.StringProperty(name="Name", default="New Strip")
    frame_start_ui:      bpy.props.FloatProperty(default=1.)
    action_frame_start:  bpy.props.FloatProperty()
    action_frame_end:    bpy.props.FloatProperty()
    scale:               bpy.props.FloatProperty(default=1.)
    repeat:              bpy.props.FloatProperty(default=1.)
    action: bpy.props.PointerProperty(type=bpy.types.Action)

    def from_action(self, action):
        self.name                = action.name
        self.frame_start_ui      = 1.
        self.action_frame_start, \
        self.action_frame_end    = action.frame_range
        self.scale               = 1.
        self.repeat              = 1.
        self.action              = action

    def from_nla_strip(self, nla_strip):
        self.name                = nla_strip.name
        self.frame_start_ui      = nla_strip.frame_start_ui
        self.action_frame_start  = nla_strip.action_frame_start
        self.action_frame_end    = nla_strip.action_frame_end
        self.scale               = nla_strip.scale
        self.repeat              = nla_strip.repeat
        self.action              = nla_strip.action
    
    def to_nla_strip(self, nla_track):
        nla_strip = nla_track.strips.new(self.name,
                                         1,
                                         self.action)
        
        nla_strip.frame_start_ui     = self.frame_start_ui
        nla_strip.action_frame_start = self.action_frame_start
        nla_strip.action_frame_end   = self.action_frame_end
        nla_strip.scale              = self.scale
        nla_strip.repeat             = self.repeat


class NLATrackWrapper(bpy.types.PropertyGroup):
    name:   bpy.props.StringProperty(name="Name", default="New Track")
    strips: bpy.props.CollectionProperty(type=NLAStripWrapper)


class BaseTypedAnimation:
    obj_name: bpy.props.StringProperty(name="Name", default="")
    strips: bpy.props.CollectionProperty(type=NLAStripWrapper)

    def from_nla_track(self, nla_track, object_name):
        self.obj_name = object_name
        self.strips.clear()
        for nla_strip in nla_track.strips:
            prop_strip = self.strips.add()
            prop_strip.from_nla_strip(nla_strip)

    def to_nla_track(self, bpy_animation_data, gap_name, anim_type, anim_name):
        track = bpy_animation_data.nla_tracks.new()
        track.name = gapnames_to_nlatrack(gap_name, anim_type, anim_name)
        track.mute = True
        # Import strips in reverse start order so they don't bump into each
        # other when they get shifted to the correct position in the track
        for prop_strip in reversed(sorted(self.strips, key=lambda strip: strip.frame_start_ui)):
            prop_strip.to_nla_strip(track)
        return track


class NodeAnimationProperties(BaseTypedAnimation, bpy.types.PropertyGroup):
    compress: bpy.props.BoolProperty(name="Compress", default=True)

    def from_action(self, action):
        self.obj_name = ""
        self.strips.clear()
        prop_strip = self.strips.add()
        prop_strip.from_action(action)


class MaterialAnimationProperties(BaseTypedAnimation, bpy.types.PropertyGroup):
    pass


class CameraAnimationProperties(BaseTypedAnimation, bpy.types.PropertyGroup):
    pass


class Type4AnimationProperties(BaseTypedAnimation, bpy.types.PropertyGroup):
    pass


class MorphAnimationProperties(BaseTypedAnimation, bpy.types.PropertyGroup):
    pass


def ShowMessageBox(message="", title="Message Box", icon='INFO'):
    """
    https://blender.stackexchange.com/a/110112
    """
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def define_name_getter(setter):
    def getter(self):
        if self.get("name") is None:
            self["name"] = ""
            setter(self, "New Animation")
        return self["name"]

    return getter


def define_name_setter(lookup_name):
    def setter(self, value):
        if value == "":
            return

        bpy_armature = self.id_data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        gap = mprops.get_selected_gap()
        collection = getattr(gap, lookup_name)()

        try:
            while value in collection:
                value = new_unique_name(value, collection, max_idx=999, separator=".")
        except ValueError:
            return

        self["name"] = value

    return setter


def define_lookat_getter(id_name):
    def getter(self):
        if self.get(id_name) is None:
            self[id_name] = ""
        return self[id_name]
    return getter


def define_lookat_setter(id_name):
    def setter(self, value):
        if value == "":
            self[id_name] = value
            return

        if value == self.name:
            ShowMessageBox("Cannot assign an animation as its own LookAt animation",
                           "Circular LookAt Reference",
                           "ERROR")
            return

        bpy_armature = self.id_data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        gap = mprops.get_selected_gap()

        lookat_anims = gap.lookat_anims_as_dict()
        idx = lookat_anims.get(value, -1)
        if idx > -1:
            prop_lookat = gap.test_lookat_anims[idx]
            if not check_lookats(gap.test_lookat_anims, lookat_anims, prop_lookat, self.name):
                ShowMessageBox(f"Assigning '{value}' to '{self.name}' would cause a circular LookAt reference.",
                               "Circular LookAt Reference",
                               "ERROR")
                return
        else:
            ShowMessageBox(f"CRITICAL INTERNAL ERROR - LOOKAT ANIMATION '{value}' DOES NOT EXIST!",
                           "CRITICAL INTERNAL ERROR",
                           "ERROR")
            return

        self[id_name] = value

    return setter


def check_lookats(lookat_collection, lookat_anims, prop_anim, root_anim_name):
    if not prop_anim.has_lookat_anims:
        return True

    for lookat_name in [prop_anim.test_lookat_left,
                        prop_anim.test_lookat_up,
                        prop_anim.test_lookat_right,
                        prop_anim.test_lookat_down]:

        if lookat_name == root_anim_name:
            return False

        idx = lookat_anims.get(lookat_name, -1)
        if idx > -1:
            prop_lookat = lookat_collection[idx]
            if not check_lookats(lookat_collection, lookat_anims, prop_lookat, root_anim_name):
                return False

    return True


class AnimationPropertiesBase:
    is_active: bpy.props.BoolProperty(name="Active", default=False)  # Only used for blend/lookats

    category: bpy.props.EnumProperty(items=[
            ("NORMAL",     "Normal",      "Standard Animation"                                             ),
            ("BLEND",      "Blend",       "Animations combined channel-by-channel with Standard Animations"),
            ("LOOKAT",     "Look At",     "Special Blend animations used for looking up/down/left/right"   )
        ],
        #update=update_category,
        name="Category"
    )

    epls:                bpy.props.CollectionProperty(name="EPLs",
                                                     type=BlobProperty,
                                                     options={'HIDDEN'})
    
    # Common properties
    flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0", default=True) # Enable node anims?
    flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1", default=False) # Enable material anims?
    flag_2:  bpy.props.BoolProperty(name="Unknown Flag 2", default=False) # Enable camera anims?
    flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3", default=False) # Enable morph anims?
    flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4", default=False) # Enable type 5 anims?
    flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5 (Unused?)", default=False)
    flag_6:  bpy.props.BoolProperty(name="Unknown Flag 6 (Unused?)", default=False)
    flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7 (Unused?)", default=False)
    flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8 (Unused?)", default=False)
    flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9 (Unused?)", default=False)
    flag_10: bpy.props.BoolProperty(name="Unknown Flag 10 (Unused?)", default=False)
    flag_11: bpy.props.BoolProperty(name="Unknown Flag 11 (Unused?)", default=False)
    flag_12: bpy.props.BoolProperty(name="Unknown Flag 12 (Unused?)", default=False)
    flag_13: bpy.props.BoolProperty(name="Unknown Flag 13 (Unused?)", default=False)
    flag_14: bpy.props.BoolProperty(name="Unknown Flag 14 (Unused?)", default=False)
    flag_15: bpy.props.BoolProperty(name="Unknown Flag 15 (Unused?)", default=False)
    flag_16: bpy.props.BoolProperty(name="Unknown Flag 16 (Unused?)", default=False)
    flag_17: bpy.props.BoolProperty(name="Unknown Flag 17 (Unused?)", default=False)
    flag_18: bpy.props.BoolProperty(name="Unknown Flag 18 (Unused?)", default=False)
    flag_19: bpy.props.BoolProperty(name="Unknown Flag 19 (Unused?)", default=False)
    flag_20: bpy.props.BoolProperty(name="Unknown Flag 20 (Unused?)", default=False)
    flag_21: bpy.props.BoolProperty(name="Unknown Flag 21 (Unused?)", default=False)
    flag_22: bpy.props.BoolProperty(name="Unknown Flag 22 (Unused?)", default=False)
    flag_24: bpy.props.BoolProperty(name="Unknown Flag 24 (Unused?)", default=False)
    flag_26: bpy.props.BoolProperty(name="Unknown Flag 26 (Unused?)", default=False)
    flag_27: bpy.props.BoolProperty(name="Unknown Flag 27 (Unused?)", default=False)
    
    bounding_box:    bpy.props.PointerProperty(type=AnimBoundingBoxProps)
    
    # Only for Normal animations
    has_lookat_anims:    bpy.props.BoolProperty(name="LookAt Anims")
    lookat_right_factor: bpy.props.FloatProperty(name="LookAt Right Factor")
    lookat_left_factor:  bpy.props.FloatProperty(name="LookAt Left Factor")
    lookat_up_factor:    bpy.props.FloatProperty(name="LookAt Up Factor")
    lookat_down_factor:  bpy.props.FloatProperty(name="LookAt Down Factor")

    properties:          bpy.props.CollectionProperty(name="Properties", type=GFSToolsGenericProperty)
    active_property_idx: bpy.props.IntProperty(options={'HIDDEN'})

    # Animation Data
    has_node_animation:        bpy.props.BoolProperty(name="Has Node Animation", default=True)
    has_blendscale_animation:  bpy.props.BoolProperty(name="Has Scale Animation", default=False)
    node_animation:            bpy.props.PointerProperty(type=NodeAnimationProperties)
    blendscale_node_animation: bpy.props.PointerProperty(type=NodeAnimationProperties)
    material_animations:       bpy.props.CollectionProperty(type=MaterialAnimationProperties)
    camera_animations:         bpy.props.CollectionProperty(type=CameraAnimationProperties)
    type4_animations:          bpy.props.CollectionProperty(type=Type4AnimationProperties)
    morph_animations:          bpy.props.CollectionProperty(type=MorphAnimationProperties)
    unimported_tracks:         bpy.props.StringProperty(name="HiddenUnimportedTracks", default="", options={"HIDDEN"})


class AnimationProperties(AnimationPropertiesBase, bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")#, get=define_name_getter("anims_as_dict"), set=define_name_setter("anims_as_dict"))
    test_lookat_right:        bpy.props.StringProperty(name="LookAt Right", default="")
    test_lookat_left:         bpy.props.StringProperty(name="LookAt Left",  default="")
    test_lookat_up:           bpy.props.StringProperty(name="LookAt Up",    default="")
    test_lookat_down:         bpy.props.StringProperty(name="LookAt Down",  default="")


class BlendAnimationProperties(AnimationPropertiesBase, bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")#, get=define_name_getter("blend_anims_as_dict"), set=define_name_setter("blend_anims_as_dict"))
    test_lookat_right:        bpy.props.StringProperty(name="LookAt Right", default="")
    test_lookat_left:         bpy.props.StringProperty(name="LookAt Left",  default="")
    test_lookat_up:           bpy.props.StringProperty(name="LookAt Up",    default="")
    test_lookat_down:         bpy.props.StringProperty(name="LookAt Down",  default="")


class LookAtAnimationProperties(AnimationPropertiesBase, bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")#, get=define_name_getter("lookat_anims_as_dict"), set=define_name_setter("lookat_anims_as_dict"))
    test_lookat_right:        bpy.props.StringProperty(name="LookAt Right", default="", get=define_lookat_getter("test_lookat_right"), set=define_lookat_setter("test_lookat_right"))
    test_lookat_left:         bpy.props.StringProperty(name="LookAt Left",  default="", get=define_lookat_getter("test_lookat_left"),  set=define_lookat_setter("test_lookat_left") )
    test_lookat_up:           bpy.props.StringProperty(name="LookAt Up",    default="", get=define_lookat_getter("test_lookat_up"),    set=define_lookat_setter("test_lookat_up")   )
    test_lookat_down:         bpy.props.StringProperty(name="LookAt Down",  default="", get=define_lookat_getter("test_lookat_down"),  set=define_lookat_setter("test_lookat_down"))


def gap_name_getter(self):
    setter = gap_name_setter

    if get_preferences().developer_mode and get_preferences().wip_animation_import:
        if self.get("name") is None:
            self["name"] = setter(self, "New Pack")
    return self["name"]


def gap_name_setter(self, value):
    if get_preferences().developer_mode and get_preferences().wip_animation_import:
        if value == "":
            return

        bpy_armature = self.id_data
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        gaps = mprops.gaps_as_dict()

        try:
            while value in gaps:
                value = new_unique_name(value, gaps, max_idx=999, separator=".")
        except ValueError:
            return

    self["name"] = value



class GFSToolsAnimationPackProperties(GFSVersionedProperty, bpy.types.PropertyGroup):
    is_active: bpy.props.BoolProperty(name="Active", default=False)
    name:    bpy.props.StringProperty(name="Name", default="New Pack")#, get=gap_name_getter, set=gap_name_setter)
    flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0 (Unused?)")
    flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1 (Unused?)")
    flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3", default=True) # Enable morph anims?
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

    animations:            bpy.props.CollectionProperty(type=NLATrackWrapper)
    active_anim_idx:       bpy.props.IntProperty(default=-1)
    test_anims:            bpy.props.CollectionProperty(type=AnimationProperties)
    test_anims_idx:        bpy.props.IntProperty(default=-1)
    test_blend_anims:      bpy.props.CollectionProperty(type=BlendAnimationProperties)
    test_blend_anims_idx:  bpy.props.IntProperty(default=-1)
    test_lookat_anims:     bpy.props.CollectionProperty(type=LookAtAnimationProperties)
    test_lookat_anims_idx: bpy.props.IntProperty(default=-1)

    test_lookat_right:        bpy.props.StringProperty(name="LookAt Right", default="")
    test_lookat_left:         bpy.props.StringProperty(name="LookAt Left",  default="")
    test_lookat_up:           bpy.props.StringProperty(name="LookAt Up",    default="")
    test_lookat_down:         bpy.props.StringProperty(name="LookAt Down",  default="")

    ERROR_TEMPLATE = "CRITICAL INTERNAL ERROR: INVALID {msg} ANIMATION INDEX '{idx}'"

    def get_anim(self, collection, idx, msg="list index out of range"):
        if not len(collection):
            return None
        elif idx == -1:
            return None
        elif idx < len(collection):
            return collection[idx]
        else:
            raise IndexError(msg)

    def _internal_get_anim(self, collection, idx, msg):
        err_msg = self.ERROR_TEMPLATE.format(msg=msg, idx=idx)
        return self.get_anim(collection, idx, err_msg)

    def get_selected_anim(self):
        return self._internal_get_anim(self.test_anims, self.test_anims_idx, "SELECTED")

    def get_active_anim(self):
        return self._internal_get_anim(self.test_anims, self.active_anim_idx, "ACTIVE")

    def store_animation_pack(self, bpy_armature_object):
        gap_props = self
        
        gap_props.animations.clear()
        if bpy_armature_object.animation_data is None:
            return

        for nla_track in bpy_armature_object.animation_data.nla_tracks:
            if is_anim_restpose(nla_track):
                continue
            
            prop_track = gap_props.animations.add()
            prop_track.name = nla_track.name
            
            for nla_strip in nla_track.strips:
                prop_strip = prop_track.strips.add()
                prop_strip.from_nla_strip(nla_strip)
    
    def restore_animation_pack(self, bpy_armature_object):
        gap_props = self
        
        self.remove_animations_from(bpy_armature_object)
        
        for prop_track in gap_props.animations:
            nla_track = bpy_armature_object.animation_data.nla_tracks.new()
            nla_track.name = prop_track.name
            nla_track.mute = True
            # Import strips in reverse start order so they don't bump into each
            # other when they get shifted to the correct position in the track
            for prop_strip in reversed(sorted(prop_track.strips, key=lambda strip: strip.frame_start_ui)):
                prop_strip.to_nla_strip(nla_track)

    @classmethod
    def remove_animations_from(cls, bpy_object):
        if bpy_object.animation_data is None:
            return
        
        ad = bpy_object.animation_data
        for nla_track in list(ad.nla_tracks):
            if is_anim_restpose(nla_track):
                continue
            
            ad.nla_tracks.remove(nla_track)
            
    def rename_unique(self, collection):
        self.name = new_unique_name(self.name, collection, separator=".")

    ###########
    # NEW API #
    ###########
    class NLAOrganizerStruct:
        def __init__(self):
            self.node_nla = None
            self.node_scale_nla = None
            self.material_nlas = []
            self.camera_nlas = []
            self.type4_nlas = []
            self.morph_nlas = []

    def is_track_tagged_as_this_pack(self, nla_track):
        gap_name, anim_type, anim_name = gapnames_from_nlatrack(nla_track)
        return gap_name == self.name

    def relevant_nla_to_list(self, bpy_object):
        if bpy_object.animation_data is None:
            return

        ad = bpy_object.animation_data
        valid_tracks = []
        names = defaultdict(lambda: 0)
        for nla_track in ad.nla_tracks:
            if self.is_track_tagged_as_this_pack(nla_track) and not is_anim_restpose(nla_track):
                valid_tracks.append(nla_track)
                names[nla_track.name] += 1

        # Data validation - make sure there are no duplicate tracks
        duplicate_tracks = {nm: count for nm, count in names.items() if count > 1}
        if len(duplicate_tracks):
            newline = "\n"
            ShowMessageBox(f"Duplicate animation names for GAP '{self.name}':{newline.join(list(duplicate_tracks.keys()))}\nRemove duplicates to pack the GAP.")
            return None

        return valid_tracks

    def get_selected_base_anim(self):
        return self._internal_get_anim(self.test_anims, self.test_anims_idx, "SELECTED BASE")

    def anims_as_dict(self):
        out = {}
        for i, anim in enumerate(self.test_anims):
            out[anim.name] = i
        return out

    def get_selected_blend_anim(self):
        return self._internal_get_anim(self.test_blend_anims, self.test_blend_anims_idx, "SELECTED BLEND")

    def blend_anims_as_dict(self):
        out = {}
        for i, anim in enumerate(self.test_blend_anims):
            out[anim.name] = i
        return out

    def get_selected_lookat_anim(self):
        return self._internal_get_anim(self.test_lookat_anims, self.test_lookat_anims_idx, "SELECTED LOOKAT")

    def lookat_anims_as_dict(self):
        out = {}
        for i, anim in enumerate(self.test_lookat_anims):
            out[anim.name] = i
        return out

    def set_anim_keyframes(self, nla_organizer, prop_anim, bpy_object):
        if nla_organizer.node_nla is not None:
            prop_anim.has_node_animation = True
            prop_anim.node_animation.from_nla_track(nla_organizer.node_nla, bpy_object.name)
        else:
            prop_anim.has_node_animation = False
            prop_anim.node_animation.strips.clear()
        if nla_organizer.node_scale_nla is not None:
            prop_anim.has_blendscale_animation = True
            prop_anim.blendscale_node_animation.from_nla_track(nla_organizer.node_scale_nla, bpy_object.name)
        else:
            prop_anim.has_blendscale_animation = False
            prop_anim.blendscale_node_animation.strips.clear()

        # if anim_name in gap_anims:
        #     gap_anim = gap_anims[anim_name]
        #     for elem in ["material_animations", "camera_animations", "type4_animations", "morph_animations"]:
        #         gap_elems = getattr(gap_anim, elem)
        #         prop_elems = getattr(prop_anim, elem)
        #         for elem_anim in gap_elems:
        #             prop_elem_anim = prop_elems.add()
        #             prop_elem_anim.from_nla_track(elem_anim, elem_anim.name)
        #     prop_anim.unimported_tracks = gap_anim.unimported_tracks

    def locate_anim_index(self, anim_collection, anim_name):
        for i, anim in enumerate(anim_collection):
            if anim.name == anim_name:
                return i
        return -1

    def update_animation_subset(self, bpy_object, nla_packets, existing_anim_names, prop_anim_collection):
        for i, (anim_name, org) in enumerate(nla_packets.items()):
            if anim_name in existing_anim_names:
                old_index = self.locate_anim_index(prop_anim_collection, anim_name)
                prop_anim = prop_anim_collection[old_index]
            else:
                prop_anim = prop_anim_collection.add()
                prop_anim.name = anim_name
                old_index = len(prop_anim_collection)-1
            self.set_anim_keyframes(org, prop_anim, bpy_object)
            prop_anim_collection.move(old_index, i)

        new_collection_size = len(existing_anim_names)
        current_collection_size = len(prop_anim_collection)
        for _ in range(current_collection_size-new_collection_size):
            prop_anim_collection.remove(new_collection_size)

    def update_from_nla(self, bpy_object):
        if bpy_object.animation_data is None:
            return

        nla_tracks = self.relevant_nla_to_list(bpy_object)
        if nla_tracks is None:
            return False

        normal_nlas = defaultdict(self.NLAOrganizerStruct)
        blend_nlas  = defaultdict(self.NLAOrganizerStruct)
        lookat_nlas = defaultdict(self.NLAOrganizerStruct)

        # Package NLAs into combined Animations
        for nla_track in nla_tracks:
            _, category, anim_name = gapnames_from_nlatrack(nla_track)
            if category == "NORMAL":
                normal_nlas[anim_name].node_nla = nla_track
            elif category == "BLEND":
                blend_nlas[anim_name].node_nla = nla_track
            elif category == "BLENDSCALE":
                blend_nlas[anim_name].node_scale_nla = nla_track
            elif category == "LOOKAT":
                lookat_nlas[anim_name].node_nla = nla_track
            elif category == "LOOKATSCALE":
                lookat_nlas[anim_name].node_scale_nla = nla_track
            else:
                ShowMessageBox(f"Unknown animation type '{category}'. Set to a valid type to deactivate the GAP.")
                return False

        self.update_animation_subset(bpy_object, normal_nlas, self.anims_as_dict(), self.test_anims)
        self.test_anims_idx = 0 if len(self.test_anims) else -1

        self.update_animation_subset(bpy_object, blend_nlas, self.blend_anims_as_dict(), self.test_blend_anims)
        self.test_blend_anims_idx = 0 if len(self.test_blend_anims) else -1

        self.update_animation_subset(bpy_object, lookat_nlas, self.lookat_anims_as_dict(), self.test_lookat_anims)
        self.test_lookat_anims_idx = 0 if len(self.test_lookat_anims) else -1

        return True

    def remove_from_nla(self, bpy_object):
        if bpy_object.animation_data is None:
            return

        ad = bpy_object.animation_data
        for nla_track in list(ad.nla_tracks):
            if self.is_track_tagged_as_this_pack(nla_track) and not is_anim_restpose(nla_track):
                ad.nla_tracks.remove(nla_track)

    def add_to_nla(self, bpy_object):
        if bpy_object.animation_data is None:
            bpy_object.animation_data_create()

        ad = bpy_object.animation_data
        # Normal anims
        for prop_anim in self.test_anims:
            track = prop_anim.node_animation.to_nla_track(ad, self.name, "NORMAL", prop_anim.name)
            for strip in track.strips:
                strip.blend_type = "REPLACE"

        # Blend anims
        for prop_anim in self.test_blend_anims:
            if prop_anim.has_node_animation:
                track = prop_anim.node_animation.to_nla_track(ad, self.name, "BLEND", prop_anim.name)
                for strip in track.strips:
                    strip.blend_type = "COMBINE"
            if prop_anim.has_blendscale_animation:
                track = prop_anim.blendscale_node_animation.to_nla_track(ad, self.name, "BLENDSCALE", prop_anim.name)
                for strip in track.strips:
                    strip.blend_type = "ADD"

        # Lookat Anims
        for prop_anim in self.test_lookat_anims:
            if prop_anim.has_node_animation:
                track = prop_anim.node_animation.to_nla_track(ad, self.name, "LOOKAT", prop_anim.name)
                for strip in track.strips:
                    strip.blend_type = "COMBINE"
            if prop_anim.has_blendscale_animation:
                track = prop_anim.blendscale_node_animation.to_nla_track(ad, self.name, "LOOKATSCALE", prop_anim.name)
                for strip in track.strips:
                    strip.blend_type = "ADD"
