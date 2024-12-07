from ..CommonStructures.CustomProperty import GFSProperty
from .Binary import AnimationBinary, LookAtAnimationsBinary
from .Binary.AnimController import AnimationControllerBinary
from .Binary.AnimTrack import AnimationTrackBinary
from .Binary.AnimTrack import KeyframeType3
from .Binary.AnimTrack import KeyframeType4
from .Binary.AnimTrack import KeyframeType5
from .Binary.AnimTrack import AmbientRGB
from .Binary.AnimTrack import DiffuseRGB
from .Binary.AnimTrack import SpecularRGB
from .Binary.AnimTrack import SpecularPower
from .Binary.AnimTrack import KeyframeType10
from .Binary.AnimTrack import KeyframeType11
from .Binary.AnimTrack import Opacity
from .Binary.AnimTrack import Tex0UV
from .Binary.AnimTrack import EmissiveRGB
from .Binary.AnimTrack import KeyframeType15
from .Binary.AnimTrack import Tex1UV
from .Binary.AnimTrack import Tex0UVSnap
from .Binary.AnimTrack import CameraFOV
from .Binary.AnimTrack import CameraRoll
from .Binary.AnimTrack import OpacitySnap
from .Binary.AnimTrack import KeyframeType29
from .Binary.AnimTrack import KeyframeType30
from .Binary.AnimTrack import Tex1UVSnap
from .Binary.AnimationBinary import EPLEntry
from .NodeAnimation import NodeAnimation

import numpy as np


def align(pos, alignment):
    return (alignment - (pos % alignment)) % alignment

def roundup(pos, alignment):
    return pos + align(pos, alignment)


class LookAtAnimationsInterface:
    def __init__(self):
        self.right = None
        self.right_factor = 0.
        self.left = None
        self.left_factor = 0.
        self.up = None
        self.up_factor = 0.
        self.down = None
        self.down_factor = 0.
        
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        instance.right = AnimationInterface.from_binary(binary.right)
        instance.left  = AnimationInterface.from_binary(binary.left)
        instance.up    = AnimationInterface.from_binary(binary.up)
        instance.down  = AnimationInterface.from_binary(binary.down)
        
        instance.right_factor = binary.right_factor
        instance.left_factor  = binary.left_factor
        instance.up_factor    = binary.up_factor
        instance.down_factor  = binary.down_factor
        
        return instance
        
    def to_binary(self, model_binary, old_node_id_to_new_node_id_map, version):
        binary = LookAtAnimationsBinary()
        binary.right = self.right.to_binary(model_binary, old_node_id_to_new_node_id_map, version)
        binary.left  = self.left.to_binary(model_binary, old_node_id_to_new_node_id_map, version)
        binary.up    = self.up.to_binary(model_binary, old_node_id_to_new_node_id_map, version)
        binary.down  = self.down.to_binary(model_binary, old_node_id_to_new_node_id_map, version)
        
        binary.right_factor = self.right_factor
        binary.left_factor  = self.left_factor
        binary.up_factor    = self.up_factor
        binary.down_factor  = self.down_factor
        
        return binary
             

class AnimationInterface:
    def __init__(self):
        self.node_animations     = []
        self.material_animations = []
        self.camera_animations   = []
        self.morph_animations    = []
        self.unknown_animations  = []
        
        self.epls                  = []
        self.lookat_animations     = None
        self.extra_track_data      = None
        self.keep_bounding_box     = False
        self.speed = None
        self.properties = []
        self.overrides  = AnimationOverrides()
        
        # These are *sometimes* set?
        # Only set on non-blend animations?!?!?!?!
        self.flag_0 = False
        self.flag_1 = False
        self.flag_2 = False
        self.flag_3 = False
        self.flag_4 = False
        
        # These are all always false
        self.flag_5  = False
        self.flag_6  = False
        self.flag_7  = False
        self.flag_8  = False
        self.flag_9  = False
        self.flag_10 = False
        self.flag_11 = False
        self.flag_12 = False
        self.flag_13 = False
        self.flag_14 = False
        self.flag_15 = False
        self.flag_16 = False
        self.flag_17 = False
        self.flag_18 = False
        self.flag_19 = False
        self.flag_20 = False
        self.flag_21 = False
        self.flag_22 = False
        self.flag_24 = False
        self.flag_26 = False
        self.flag_27 = False
    
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        
        for controller_binary in binary.controllers:
            if controller_binary.type == 1:
                instance.node_animations.append    (NodeAnimation.from_controller(controller_binary))
            elif controller_binary.type == 2:
                instance.material_animations.append(cls._import_material_animation_binary(controller_binary))
            elif controller_binary.type == 3:
                instance.camera_animations.append  (cls._import_camera_animation_binary  (controller_binary))
            elif controller_binary.type == 4:
                instance.morph_animations.append   (cls._import_morph_animation_binary   (controller_binary))
            elif controller_binary.type == 5:
                instance.unknown_animations.append (cls._import_unknown_animation_binary (controller_binary))
            else:
                raise NotImplementedError(f"Unknown Controller Type: {controller_binary.type}")
                
        if binary.flags.has_lookat_anims:
            instance.lookat_animations = LookAtAnimationsInterface.from_binary(binary.lookat_animations)
        if binary.flags.has_epls:
            instance.epls = binary.epls.data
        instance.extra_track_data                = binary.extra_track_data
        instance.keep_bounding_box               = binary.flags.has_bounding_box
        instance.overrides.bounding_box.max_dims = binary.bounding_box_max_dims
        instance.overrides.bounding_box.min_dims = binary.bounding_box_min_dims
        instance.speed                           = binary.speed
        instance.properties = [GFSProperty.from_binary(prop) for prop in binary.properties.data]
        
        # These should be removable...?
        # Maybe these say which channels are activated..?!
        instance.flag_0 = binary.flags.has_node_anims
        instance.flag_1 = binary.flags.has_material_anims
        instance.flag_2 = binary.flags.has_camera_anims
        instance.flag_3 = binary.flags.has_morph_anims
        instance.flag_4 = binary.flags.has_type_5_anims

        # These should all be false
        instance.flag_5  = binary.flags.flag_5
        instance.flag_6  = binary.flags.flag_6
        instance.flag_7  = binary.flags.flag_7
        instance.flag_8  = binary.flags.flag_8
        instance.flag_9  = binary.flags.flag_9
        instance.flag_10 = binary.flags.flag_10
        instance.flag_11 = binary.flags.flag_11
        instance.flag_12 = binary.flags.flag_12
        instance.flag_13 = binary.flags.flag_13
        instance.flag_14 = binary.flags.flag_14
        instance.flag_15 = binary.flags.flag_15
        instance.flag_16 = binary.flags.flag_16
        instance.flag_17 = binary.flags.flag_17
        instance.flag_18 = binary.flags.flag_18
        instance.flag_19 = binary.flags.flag_19
        instance.flag_20 = binary.flags.flag_20
        instance.flag_21 = binary.flags.flag_21
        instance.flag_22 = binary.flags.flag_22
        instance.flag_24 = binary.flags.flag_24
        instance.flag_26 = binary.flags.flag_26
        instance.flag_27 = binary.flags.flag_27
        
        return instance
        
    @staticmethod
    def _import_material_animation_binary(controller_binary):
        anim = MaterialAnimation(controller_binary.target_id,
                                 controller_binary.target_name.string)

        for track_binary in controller_binary.tracks:
            if   track_binary.keyframe_type == 6:  anim.ambient_rgb  = {f: [kf.r, kf.g, kf.b]                                                    for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 7:  anim.diffuse_rgb  = {f: [kf.r, kf.g, kf.b]                                                    for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 8:  anim.specular_rgb = {f: [kf.r, kf.g, kf.b]                                                    for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 9:  anim.specular_power = {f: kf.unknown                                                            for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 11: anim.unknown_11   = {f: kf.unknown                                                            for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 12: anim.opacity      = {f: kf.opacity                                                            for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 13: anim.tex0_uv      = {f: [kf.translate_u, kf.translate_v, kf.scale_u, kf.scale_v, kf.rotation] for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 14: anim.emissive_rgb = {f: [kf.r, kf.g, kf.b]                                                    for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 15: anim.unknown_15   = {f: kf.unknown                                                            for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 20: anim.tex1_uv      = {f: [kf.translate_u, kf.translate_v, kf.scale_u, kf.scale_v, kf.rotation] for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 21: anim.tex0_uv_snap = {f: [kf.translate_u, kf.translate_v, kf.scale_u, kf.scale_v, kf.rotation] for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 25: anim.opacity_snap = {f: kf.opacity                                                      for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 29: anim.unknown_29   = {f: kf.unknown                                                            for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 30: anim.unknown_30   = {f: kf.unknown_float                                                      for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 36: anim.tex1_uv_snap = {f: [kf.translate_u, kf.translate_v, kf.scale_u, kf.scale_v, kf.rotation] for f, kf in zip(track_binary.frames, track_binary.values)}
            else: raise NotImplementedError("fNo instruction to convert keyframe type '{track_binary.keyframe_type}' to a Material Animation exists")
        
        return anim

    @staticmethod
    def _import_camera_animation_binary(controller_binary):
        anim = CameraAnimation(controller_binary.target_id,
                               controller_binary.target_name.string)
            
        for track_binary in controller_binary.tracks:
            if track_binary.keyframe_type == 23:
                anim.fov = {f: kf.camera_fov for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 24:
                anim.roll = {f: kf.roll for f, kf in zip(track_binary.frames, track_binary.values)}
            else:
                raise NotImplementedError(f"No instruction to convert keyframe type '{track_binary.keyframe_type}' to a Camera Animation exists")

        return anim

    @staticmethod
    def _import_morph_animation_binary(controller_binary):
        anim = MorphAnimation(controller_binary.target_id,
                              controller_binary.target_name.string)
            
        for track_binary in controller_binary.tracks:
            if track_binary.keyframe_type == 3:
                anim.unknown = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            else:
                raise NotImplementedError(f"No instruction to convert keyframe type '{track_binary.keyframe_type}' to a Morph Animation exists")
    
        return anim

    @staticmethod
    def _import_unknown_animation_binary(controller_binary):
        anim = UnknownAnimation(controller_binary.target_id,
                                controller_binary.target_name.string)
        
        for track_binary in controller_binary.tracks:
            if track_binary.keyframe_type == 5:
                anim.unknown = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            else:
                raise NotImplementedError(f"No instruction to convert keyframe type '{track_binary.keyframe_type}' to a Morph Animation exists")
    
        return anim
    
    def to_binary(self, model_binary, old_node_id_to_new_node_id_map, version):
        binary = AnimationBinary()
        
        binary.flags.has_node_anims     = len(self.node_animations)
        binary.flags.has_material_anims = len(self.material_animations)
        binary.flags.has_camera_anims   = len(self.camera_animations)
        binary.flags.has_morph_anims    = len(self.morph_animations)
        binary.flags.has_type_5_aninms  = len(self.unknown_animations)
        
        binary.flags.has_node_anims     = self.flag_0
        binary.flags.has_material_anims = self.flag_1
        binary.flags.has_camera_anims   = self.flag_2
        binary.flags.has_morph_anims    = self.flag_3
        binary.flags.has_type_5_anims   = self.flag_4
        
        
        binary.flags.flag_5             = self.flag_5
        binary.flags.flag_6             = self.flag_6
        binary.flags.flag_7             = self.flag_7
        binary.flags.flag_8             = self.flag_8
        binary.flags.flag_9             = self.flag_9
        binary.flags.flag_10            = self.flag_10
        binary.flags.flag_11            = self.flag_11
        binary.flags.flag_12            = self.flag_12
        binary.flags.flag_13            = self.flag_13
        binary.flags.flag_14            = self.flag_14
        binary.flags.flag_15            = self.flag_15
        binary.flags.flag_16            = self.flag_16
        binary.flags.flag_17            = self.flag_17
        binary.flags.flag_18            = self.flag_18
        binary.flags.flag_19            = self.flag_19
        binary.flags.flag_20            = self.flag_20
        binary.flags.flag_21            = self.flag_21
        binary.flags.flag_22            = self.flag_22
        binary.flags.has_properties     = len(self.properties)
        binary.flags.flag_24            = self.flag_24
        binary.flags.has_speed          = self.speed is not None
        binary.flags.flag_26            = self.flag_26
        binary.flags.flag_27            = self.flag_27
        binary.flags.has_epls           = len(self.epls)
        binary.flags.has_lookat_anims   = self.lookat_animations     is not None
        binary.flags.has_bounding_box   = self.keep_bounding_box
        binary.flags.has_extra_data     = self.extra_track_data      is not None

        if binary.flags.has_epls:
            binary.epls.data            = self.epls
            binary.epls.count           = len(self.epls)
        if binary.flags.has_lookat_anims:
            binary.lookat_animations = self.lookat_animations.to_binary(model_binary, old_node_id_to_new_node_id_map, version)
        binary.extra_track_data      = self.extra_track_data
        binary.speed                 = self.speed
        binary.properties.data       = [prop.to_binary() for prop in self.properties]
        binary.properties.count      = len(self.properties)
        
        # Order of controllers here is probably done in global node order...
        binary.controllers.extend([a.to_controller(old_node_id_to_new_node_id_map, version) for a in self.node_animations]) # Nodes are first
        binary.controllers.extend([a.to_controller() for a in self.camera_animations  ]) # Then cameras - SOMETIMES MIXED WITH NODES?!
        binary.controllers.extend([a.to_controller() for a in self.material_animations]) # Then materials
        binary.controllers.extend([a.to_controller() for a in self.morph_animations   ]) # Then... ??
        binary.controllers.extend([a.to_controller() for a in self.unknown_animations ])
        
        # Calculate duration
        tracks = [track for ctlr in binary.controllers for track in ctlr.tracks]
        if len(tracks):
            if all(len(track.frames) == 1 for track in tracks) and version > 0x02000000:
                binary.duration = 1/24
            else:
                st_track_frames = [track.frames[ 0] for track in tracks]
                ed_track_frames = [track.frames[-1] for track in tracks]
                binary.duration = max(ed_track_frames) - min(st_track_frames)
        else:
            binary.duration = 0

        # Chuck stuff into the binary
        binary.controller_count = len(binary.controllers)
        if version > 0x02000000:
            # Calculate size of the animation buffer
            animation_buffer_size = 0
            for controller in binary.controllers:
                animation_buffer_size += roundup(len(controller.target_name.string) + 1, 0x10)
                for track in controller.tracks:
                    if track.keyframe_count > 0:
                        animation_buffer_size += roundup(track.keyframe_count*4, 0x10)
                        animation_buffer_size += roundup(track.keyframe_count*4*track.values[0].size(), 0x10)
            if binary.extra_track_data is not None:
                track = binary.extra_track_data.track
                if track.keyframe_count > 0:
                    animation_buffer_size += roundup(track.keyframe_count*4, 0x10)
                    animation_buffer_size += roundup(track.keyframe_count*4*track.values[0].size(), 0x10)
        
            binary.track_count      = len(tracks)
            binary.anim_buffer_size = animation_buffer_size
        
        if self.keep_bounding_box:
            bounding_box = self.overrides.bounding_box
            if bounding_box.enabled:
                binary.bounding_box_max_dims = bounding_box.max_dims
                binary.bounding_box_min_dims = bounding_box.min_dims
            else:
                binary.autocalc_bounding_box(model_binary)
        
        return binary
    
    def add_node_animation(self, node_idx, node_name):
        self.node_animations.append(NodeAnimation(node_idx, node_name))
        return self.node_animations[-1]
    
    def add_material_animation(self, material_idx, material_name):
        self.material_animations.append(MaterialAnimation())
        return
        
    def add_lookat_animations(self, up_factor, down_factor, left_factor, right_factor):
        self.lookat_animations = LookAtAnimationsInterface()
        la_a = self.lookat_animations
        la_a.up    = AnimationInterface()
        la_a.down  = AnimationInterface()
        la_a.left  = AnimationInterface()
        la_a.right = AnimationInterface()
        
        la_a.up_factor    = up_factor
        la_a.down_factor  = down_factor
        la_a.left_factor  = left_factor
        la_a.right_factor = right_factor
        
        return la_a.up, la_a.down, la_a.left, la_a.right
    
    def add_property(self, name, dtype, data):
        prop = GFSProperty()
        prop.name = name
        prop.type = dtype
        prop.data = data
        self.properties.append(prop)
        return prop

    def add_epl(self, binary):
        self.epls.append(binary)


class MaterialAnimation:
    def __init__(self, id, name):
        self.name = name
        self.id   = id
        
        self.snap_tex0_uvs = False
        self.snap_tex1_uvs = False
        self.snap_opacity  = False
        
        self.ambient_rgb  = {}
        self.diffuse_rgb  = {}
        self.specular_rgb = {}
        self.specular_power = {}
        self.unknown_11   = {}
        self.opacity      = {}
        self.tex0_uv      = {}
        self.emissive_rgb = {}
        self.unknown_15   = {}
        self.tex1_uv      = {}
        self.tex0_uv_snap = {}
        self.opacity_snap = {}
        self.unknown_29   = {}
        self.unknown_30   = {}
        self.tex1_uv_snap = {}

    def to_controller(self):
        tracks = []
        for dataset, keyframe_type in [
                (self.ambient_rgb,    AmbientRGB    ),
                (self.diffuse_rgb,    DiffuseRGB    ),
                (self.specular_rgb,   SpecularRGB   ),
                (self.specular_power, SpecularPower ),
                (self.unknown_11,     KeyframeType11),
                (self.opacity,        Opacity       ),
                (self.tex0_uv,        Tex0UV        ),
                (self.emissive_rgb,   EmissiveRGB   ),
                (self.unknown_15,     KeyframeType15),
                (self.tex1_uv,        Tex1UV        ),
                (self.tex0_uv_snap,   Tex0UVSnap    ), # This should be merged with tex0_uv
                (self.opacity_snap,   OpacitySnap   ), # This should be merged with opacity
                (self.unknown_29,     KeyframeType29),
                (self.unknown_30,     KeyframeType30),
                (self.tex1_uv_snap,   Tex1UVSnap    )  # This should be merged with tex1_uv
            ]:
            if len(dataset):
                kf_type = keyframe_type
                
                #frames,\
                #kf_values = construct_frames((dataset, lerp ))
                frames    = list(dataset.keys())
                kf_values = list(dataset.values())

                track_binary = AnimationTrackBinary()
                    
                track_binary.frames = frames
                track_binary.keyframe_type = kf_type.VARIANT_TYPE
                track_binary.keyframe_count = len(track_binary.frames)
                track_binary.values = [kf_type(args) for args in kf_values]
                
                tracks.append(track_binary)
        
        controller_binary = AnimationControllerBinary()
        controller_binary.type = 2
        controller_binary.target_id = self.id # [b.name for b in gfs.materials].index(self.name)
        controller_binary.target_name = controller_binary.target_name.from_name(self.name)
        controller_binary.tracks.data = tracks
        controller_binary.tracks.count = len(tracks)
        
        return controller_binary
        
class CameraAnimation:
    def __init__(self, id, name):
        self.name = name
        self.id   = id
        self.fov  = {}
        self.roll = {}

    def to_controller(self):
        tracks = []
        for dataset, keyframe_type in [
                (self.fov,   CameraFOV),
                (self.roll,  CameraRoll)
            ]:
            if len(dataset):
                kf_type = keyframe_type
                
                #frames,\
                #kf_values = construct_frames((dataset, lerp ))
                frames    = list(dataset.keys())
                kf_values = list(dataset.values())
                
                track_binary = AnimationTrackBinary()
                    
                track_binary.frames = frames
                track_binary.keyframe_type = kf_type.VARIANT_TYPE
                track_binary.keyframe_count = len(track_binary.frames)
                track_binary.values = [kf_type(args) for args in kf_values]
                
                tracks.append(track_binary)
                
        controller_binary = AnimationControllerBinary()
        controller_binary.type = 3
        controller_binary.target_id = self.id # [b.name for b in gfs.cameras].index(self.name)
        controller_binary.target_name = controller_binary.target_name.from_name(self.name)
        controller_binary.tracks.data = tracks
        controller_binary.tracks.count = len(tracks)
        
        return controller_binary

class MorphAnimation:
    def __init__(self, id, name):
        self.name = name
        self.id   = id
        self.unknown = {}

    def to_controller(self):
        tracks = []
        for dataset, keyframe_type in [
                (self.unknown, KeyframeType3)
            ]:
            if len(dataset):
                kf_type = keyframe_type
                
                #frames,\
                #kf_values = construct_frames((dataset, lerp ))
                frames    = list(dataset.keys())
                kf_values = list(dataset.values())
                
                track_binary = AnimationTrackBinary()
                    
                track_binary.frames = frames
                track_binary.keyframe_type = kf_type.VARIANT_TYPE
                track_binary.keyframe_count = len(track_binary.frames)
                track_binary.values = [kf_type(args) for args in kf_values]
                
                tracks.append(track_binary)
                
        controller_binary = AnimationControllerBinary()
        controller_binary.type = 4
        controller_binary.target_id = self.id #[b.name for b in gfs.morphs].index(self.name)
        controller_binary.target_name = controller_binary.target_name.from_name(self.name)
        controller_binary.tracks.data = tracks
        controller_binary.tracks.count = len(tracks)
        
        return controller_binary
    
class UnknownAnimation:
    def __init__(self, id, name):
        self.name = name
        self.id   = id
        self.unknown = {}

    def to_controller(self):
        tracks = []
        for dataset, keyframe_type in [
                (self.unknown, KeyframeType5)
            ]:
            if len(dataset):
                kf_type = keyframe_type
                
                #frames,\
                #kf_values = construct_frames((dataset, lerp ))
                frames    = list(dataset.keys())
                kf_values = list(dataset.values())
                
                track_binary = AnimationTrackBinary()
                    
                track_binary.frames = frames
                track_binary.keyframe_type = kf_type.VARIANT_TYPE
                track_binary.keyframe_count = len(track_binary.frames)
                track_binary.values = [kf_type(args) for args in kf_values]
                
                tracks.append(track_binary)
                
        controller_binary = AnimationControllerBinary()
        controller_binary.type = 5
        controller_binary.target_id = self.id #[b.name for b in gfs.morphs].index(self.name)
        controller_binary.target_name = controller_binary.target_name.from_name(self.name)
        controller_binary.tracks.data = tracks
        controller_binary.tracks.count = len(tracks)
        
        return controller_binary
    

class BoundingBoxOverride:
    def __init__(self):
        self.enabled = False
        self.min_dims = [0, 0, 0]
        self.max_dims = [0, 0, 0]


class AnimationOverrides:
    def __init__(self):
        self._bounding_box = BoundingBoxOverride()
    
    @property
    def bounding_box(self):
        return self._bounding_box
