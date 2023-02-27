from ..CommonStructures.CustomProperty import PropertyInterface
from .Binary import AnimationBinary, LookAtAnimationsBinary
from .Binary.AnimController import AnimationControllerBinary
from .Binary.AnimTrack import AnimationTrackBinary
from .Binary.AnimTrack import NodeTR
from .Binary.AnimTrack import NodeTRS
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
from .Binary.AnimTrack import KeyframeType16
from .Binary.AnimTrack import KeyframeType17
from .Binary.AnimTrack import KeyframeType18
from .Binary.AnimTrack import KeyframeType19
from .Binary.AnimTrack import Tex1UV
from .Binary.AnimTrack import Tex0UVSnap
from .Binary.AnimTrack import KeyframeType22
from .Binary.AnimTrack import KeyframeType23
from .Binary.AnimTrack import KeyframeType24
from .Binary.AnimTrack import OpacitySnap
from .Binary.AnimTrack import KeyframeType26
from .Binary.AnimTrack import NodeTRSHalf
from .Binary.AnimTrack import KeyframeType28
from .Binary.AnimTrack import KeyframeType29
from .Binary.AnimTrack import KeyframeType30
from .Binary.AnimTrack import NodeTHalf
from .Binary.AnimTrack import NodeRHalf
from .Binary.AnimTrack import NodeSHalf
from .Binary.AnimTrack import NodeTSHalf
from .Binary.AnimTrack import NodeRSHalf
from .Binary.AnimTrack import Tex1UVSnap

import numpy as np


def lerp(x, y, t):
    return (1-t)*x + t*y


def slerp(x, y, t):
    omega = np.arccos(np.dot(x, y))
    if omega == 0 or np.isnan(omega):
        return x
    term_1 = x * np.sin((1-t)*omega)
    term_2 = y * np.sin(t*omega)
    return (term_1 + term_2) / np.sin(omega)


def interpolate_keyframe_dict(frames, idx, interpolation_function, debug_output=False):
    frame_idxs = list(frames.keys())
    smaller_elements = [fidx for fidx in frame_idxs if idx >= fidx]
    next_smallest_frame = max(smaller_elements) if len(smaller_elements) else frame_idxs[0]
    larger_elements = [fidx for fidx in frame_idxs if idx <= fidx]
    next_largest_frame = min(larger_elements) if len(larger_elements) else frame_idxs[-1]

    if next_largest_frame == next_smallest_frame:
        t = 0  # Totally arbitrary, since the interpolation will be between two identical values
    else:
        t = (idx - next_smallest_frame) / (next_largest_frame - next_smallest_frame)

    min_value = frames[next_smallest_frame]
    max_value = frames[next_largest_frame]

    return interpolation_function(np.array(min_value), np.array(max_value), t)

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
        
    def to_binary(self, old_node_id_to_new_node_id_map):
        binary = LookAtAnimationsBinary()
        binary.right = self.right.to_binary(old_node_id_to_new_node_id_map)
        binary.left  = self.left.to_binary(old_node_id_to_new_node_id_map)
        binary.up    = self.up.to_binary(old_node_id_to_new_node_id_map)
        binary.down  = self.down.to_binary(old_node_id_to_new_node_id_map)
        
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
        
        self.particle_data         = None
        self.lookat_animations     = None
        self.extra_track_data      = None
        self.bounding_box_max_dims = None
        self.bounding_box_min_dims = None
        self.speed = None
        self.properties = []
        
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
                instance.node_animations.append    (cls._import_node_animation_binary    (controller_binary))
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
        if binary.flags.has_particles:
            instance.particle_data = binary.particle_data
        instance.extra_track_data      = binary.extra_track_data
        instance.bounding_box_max_dims = binary.bounding_box_max_dims
        instance.bounding_box_min_dims = binary.bounding_box_min_dims
        instance.speed                 = binary.speed
        instance.properties = [PropertyInterface.from_binary(prop) for prop in binary.properties.data]

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
    def _import_node_animation_binary(controller_binary):
        anim = NodeAnimation(controller_binary.target_id, controller_binary.target_name.string)
        anim.track_groups = []
            
        for track_binary in controller_binary.tracks:
            base_position = track_binary.base_position
            base_scale = track_binary.base_scale
            def scale_pos(pos):
                return [p*bp for p, bp in zip(pos, base_position)]
            def scale_scl(scl):
                return [s*bs for s, bs in zip(scl, base_scale)]
            
            if track_binary.keyframe_type == 1:
                anim.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([0, 1])
            elif track_binary.keyframe_type == 2:
                anim.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.scales    = {f: kf.scale    for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([0, 1, 2])
            elif track_binary.keyframe_type == 16:
                anim.unknown_floats = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([4])
            elif track_binary.keyframe_type == 26:
                # How does this differ from 28?
                anim.compress = True
                anim.is_kf26  = True
                anim.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([0, 1])
            elif track_binary.keyframe_type == 27:
                anim.compress = True
                anim.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([0, 1, 2])
            elif track_binary.keyframe_type == 28:
                anim.compress = True
                anim.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([0, 1])
            elif track_binary.keyframe_type == 31:
                anim.compress = True
                anim.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([0])
            elif track_binary.keyframe_type == 32:
                anim.compress = True
                anim.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([1])
            elif track_binary.keyframe_type == 33:
                anim.compress = True
                anim.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([2])
            elif track_binary.keyframe_type == 34:
                anim.compress = True
                anim.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([0, 2])
            elif track_binary.keyframe_type == 35:
                anim.compress = True
                anim.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.track_groups.append([1, 2])
            # Unknown EPL stuff
            elif track_binary.keyframe_type == 17:
                anim.track_17_data = {f: [kf.position, kf.rotation, kf.scale, kf.unknown] for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 18:
                anim.track_18_data = {f: [kf.unknown_0x00, kf.unknown_0x04, kf.unknown_0x08, kf.unknown_0x0C] for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 19:
                anim.track_19_data = {f: [kf.unknown_1, kf.unknown_2] for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 22:
                anim.track_22_data = {f: [
                    kf.unknown_0x00,
                    kf.unknown_0x04,
                    kf.unknown_0x08,
                    kf.unknown_0x0A,
                    kf.unknown_0x0E,
                    kf.unknown_0x12,
                    kf.unknown_0x16,
                    kf.unknown_0x1A,
                    kf.unknown_0x1C,
                    kf.unknown_0x20,
                    kf.unknown_0x24,
                    kf.unknown_0x28
                    ]
                    for f, kf in zip(track_binary.frames, track_binary.values)}
            else:
                raise NotImplementedError(f"No instruction to convert keyframe type '{track_binary.keyframe_type}' to a Node Animation exists")
        
        return anim
        
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
                anim.unknown_24 = {f: kf.unknown_float for f, kf in zip(track_binary.frames, track_binary.values)}
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
    
    def to_binary(self, old_node_id_to_new_node_id_map):
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
        binary.flags.has_particles      = self.particle_data         is not None
        binary.flags.has_lookat_anims   = self.lookat_animations     is not None
        binary.flags.has_bounding_box   = self.bounding_box_max_dims is not None
        binary.flags.has_extra_data     = self.extra_track_data      is not None

        if binary.flags.has_particles:
            binary.particle_data     = self.particle_data
        if binary.flags.has_lookat_anims:
            binary.lookat_animations = self.lookat_animations.to_binary()
        binary.extra_track_data      = self.extra_track_data
        binary.bounding_box_max_dims = self.bounding_box_max_dims
        binary.bounding_box_min_dims = self.bounding_box_min_dims
        binary.speed                 = self.speed
        binary.properties.data       = [prop.to_binary() for prop in self.properties]
        binary.properties.count      = len(self.properties)
        
        binary.controllers.data.extend([a.to_controller(old_node_id_to_new_node_id_map) for a in self.node_animations]) # Nodes are first
        binary.controllers.data.extend([a.to_controller() for a in self.camera_animations  ]) # Then cameras - SOMETIMES MIXED WITH NODES?!
        binary.controllers.data.extend([a.to_controller() for a in self.material_animations]) # Then materials
        binary.controllers.data.extend([a.to_controller() for a in self.morph_animations   ]) # Then... ??
        binary.controllers.data.extend([a.to_controller() for a in self.unknown_animations ])
        binary.controllers.count     = len(binary.controllers.data)
        track_frames = [track.frames[-1] for ctlr in binary.controllers for track in ctlr.tracks]
        if len(track_frames):
            binary.duration = max(track_frames) - min(track_frames) # Might this be calculated from a subset of anims?
        else:
            binary.duration = 0
        
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
        prop = PropertyInterface()
        prop.name = name
        prop.type = dtype
        prop.data = data
        self.properties.append(prop)
        return prop


def construct_frames(*keyframe_sets):
    all_frames = set()
    for keyframes, _ in keyframe_sets:
        all_frames.update(keyframes.keys())
    all_frames = sorted(all_frames)
    
    out = []
    for (keyframes, interpolation_function) in keyframe_sets:
        out_kf = [None]*len(all_frames)
        for i, frame in enumerate(all_frames):
            if frame in keyframes:
                out_kf[i] = keyframes[frame]
            else:
                out_kf[i] = interpolate_keyframe_dict(keyframes, frame, interpolation_function)
        out.append(out_kf)
    return all_frames, out


def apply_scale_to_keyframes(keyframes, scale):
    out = {}
    for key, value in keyframes.items():
        out[key] = [k/s if s != 0 else 0 for k, s in zip(value, scale)]
    return out


def extract_scale(keyframes, size):
    # The original files seem to not care if the values are smaller than 1 already
    maxima = [1., 1., 1.]
    for e in keyframes.values():    
        for i in range(size):
            if abs(e[i]) > abs(maxima[i]):
                maxima[i] = e[i]
            elif (abs(e[i]) == abs(maxima[i])) and (e[i] > maxima[i]):
                maxima[i] = e[i]
    # for i, m in enumerate(maxima):
    #     if m == 0:
    #         maxima[i] = 1.
    return maxima


class NodeAnimation:
    def __init__(self, id, name):
        self.name = name
        self.id   = id
        self.compress = False
        self.is_kf26  = False
        self.positions = {}
        self.rotations = {}
        self.scales    = {}
        self.byte_data = {}
        self.unknown_floats = {}
        self.track_17_data = {}
        self.track_18_data = {}
        self.track_19_data = {}
        self.track_22_data = {}
        self.track_groups = None
        
    def to_controller(self, old_node_id_to_new_node_id_map):        
        track_binary = AnimationTrackBinary()
        has_trans    = len(self.positions)
        has_rot      = len(self.rotations)
        has_scale    = len(self.scales)
        has_byte     = len(self.byte_data)
        has_floats   = len(self.unknown_floats)
        
                
        # Create controller
        controller_binary = AnimationControllerBinary()
        controller_binary.type = 1
        controller_binary.target_id = self.id #[b.name for b in gfs.nodes].index(self.name)
        controller_binary.target_name = controller_binary.target_name.from_name(self.name)
        controller_binary.tracks.data = []
        
        if old_node_id_to_new_node_id_map is not None:
            controller_binary.target_id = old_node_id_to_new_node_id_map[controller_binary.target_id]
        
        
        # Pos, Rot, Scale
        if (has_trans or has_rot or has_scale or has_byte or has_floats):
            
            if len(self.byte_data):
                raise NotImplementedError("Cannot export Node Byte data yet")
            
            # Bundle the data depending on the keyframes
            position_idx = 0
            rotation_idx = 1
            scale_idx    = 2
            byte_idx     = 3
            float_idx    = 4
            if self.track_groups is None:
                anim_tracks = [self.positions, self.rotations, self.scales, self.byte_data, self.unknown_floats]
                anim_track_groups = [[]]
                for at_idx, at in enumerate(anim_tracks):
                    if not len(at):
                        continue
                    anim_track_groups[0].append(at_idx)
            else:
                anim_track_groups = self.track_groups
    
            # Create tracks
            for atg in anim_track_groups:
                
                has_trans    = position_idx in atg
                has_rot      = rotation_idx in atg
                has_scale    = scale_idx    in atg
                has_byte     = byte_idx     in atg
                has_floats   = float_idx    in atg
                
                position_scale = [0., 0., 0.]
                scale_scale    = [0., 0., 0.]
                # This is obviously incomplete
                if self.compress:
                    if has_trans and has_rot and has_scale:
                        kf_type = NodeTRSHalf
                        
                        position_scale = extract_scale(self.positions, 3)
                        scale_scale    = extract_scale(self.scales,    3)
        
                        frames,\
                        kf_values = construct_frames((apply_scale_to_keyframes(self.positions, position_scale), lerp ),
                                                     (self.rotations, slerp),
                                                     (apply_scale_to_keyframes(self.scales,    scale_scale   ), lerp ))
                    elif has_trans and has_rot:
                        if self.is_kf26:
                            kf_type = KeyframeType26
                        else:
                            kf_type = KeyframeType28
                        
                        position_scale = extract_scale(self.positions, 3)
                        scale_scale    = [1., 1., 1.]
                        
                        frames,\
                        kf_values = construct_frames((apply_scale_to_keyframes(self.positions, position_scale), lerp ),
                                                     (self.rotations, slerp))
                        
                        #print("SCALE:", position_scale, "FIRST:", kf_values[0][0])
                        
                    elif has_trans and has_scale:
                        kf_type = NodeTSHalf
                        
                        position_scale = extract_scale(self.positions, 3)
                        scale_scale    = extract_scale(self.scales,    3)
                        
                        frames,\
                        kf_values = construct_frames((apply_scale_to_keyframes(self.positions, position_scale), lerp ),
                                                     (apply_scale_to_keyframes(self.scales,    scale_scale   ), lerp ))
                    elif has_rot and has_scale:
                        kf_type = NodeRSHalf
                        
                        position_scale = [1., 1., 1.]
                        scale_scale    = extract_scale(self.scales,    3)
                        
                        frames,\
                        kf_values = construct_frames((self.rotations, slerp),
                                                     (apply_scale_to_keyframes(self.scales,    scale_scale   ), lerp ))
                    elif has_trans:
                        kf_type = NodeTHalf
                        
                        position_scale = extract_scale(self.positions, 3)
                        scale_scale    = [1., 1., 1.,]
                        
                        frames,\
                        kf_values = construct_frames((apply_scale_to_keyframes(self.positions, position_scale), lerp ))
                    elif has_rot:
                        kf_type = NodeRHalf
                        
                        frames,\
                        kf_values = construct_frames((self.rotations, slerp))
                    elif has_scale:
                        kf_type = NodeSHalf
                        
                        position_scale = [1., 1., 1.]
                        scale_scale    = extract_scale(self.scales,    3)
                        
                        frames,\
                        kf_values = construct_frames((apply_scale_to_keyframes(self.scales,    scale_scale   ), lerp ))
                    else:
                        raise NotImplementedError
                else:
                    if has_trans and has_rot and has_scale:
                        kf_type = NodeTRS
                        
                        frames,\
                        kf_values = construct_frames((self.positions, lerp ),
                                                     (self.rotations, slerp),
                                                     (self.scales,    lerp ))
                    elif has_trans and has_rot:
                        kf_type = NodeTR
                        
                        frames,\
                        kf_values = construct_frames((self.positions, lerp),
                                                     (self.rotations, slerp))
                    elif has_floats:
                        kf_type = KeyframeType16
                        
                        frames,\
                        kf_values = construct_frames((self.unknown_floats, lerp))
                    else:
                        raise NotImplementedError
         
                track_binary = AnimationTrackBinary()
                track_binary.frames = frames
                track_binary.keyframe_type = kf_type.VARIANT_TYPE
                track_binary.keyframe_count = len(track_binary.frames)
                track_binary.values = [kf_type(*args) for args in zip(*kf_values)]
                track_binary.base_position = position_scale
                track_binary.base_scale    = scale_scale
                
                controller_binary.tracks.data.append(track_binary)
        
        elif len(self.track_17_data):
            kf_type = KeyframeType17
            
            track_binary = AnimationTrackBinary()
            track_binary.frames = self.track_17_data.keys()
            track_binary.keyframe_type = kf_type.VARIANT_TYPE
            track_binary.keyframe_count = len(track_binary.frames)
            track_binary.values = [kf_type(*args) for args in zip(*list(self.track_17_data.values()))]
            track_binary.base_position = [0., 0., 0.]
            track_binary.base_scale    = [0., 0., 0.]
            
            controller_binary.tracks.data.append(track_binary)
        
        elif len(self.track_18_data):
            kf_type = KeyframeType18
            
            track_binary = AnimationTrackBinary()
            track_binary.frames = self.track_18_data.keys()
            track_binary.keyframe_type = kf_type.VARIANT_TYPE
            track_binary.keyframe_count = len(track_binary.frames)
            track_binary.values = [kf_type(*args) for args in zip(*list(self.track_18_data.values()))]
            track_binary.base_position = [0., 0., 0.]
            track_binary.base_scale    = [0., 0., 0.]
            
            controller_binary.tracks.data.append(track_binary)
        
        elif len(self.track_19_data):
            kf_type = KeyframeType19
            
            track_binary = AnimationTrackBinary()
            track_binary.frames = self.track_19_data.keys()
            track_binary.keyframe_type = kf_type.VARIANT_TYPE
            track_binary.keyframe_count = len(track_binary.frames)
            track_binary.values = [kf_type(*args) for args in zip(*list(self.track_19_data.values()))]
            track_binary.base_position = [0., 0., 0.]
            track_binary.base_scale    = [0., 0., 0.]
            
            controller_binary.tracks.data.append(track_binary)
        
        elif len(self.track_22_data):
            kf_type = KeyframeType22
            
            track_binary = AnimationTrackBinary()
            track_binary.frames = self.track_22_data.keys()
            track_binary.keyframe_type = kf_type.VARIANT_TYPE
            track_binary.keyframe_count = len(track_binary.frames)
            track_binary.values = [kf_type(*args) for args in zip(*list(self.track_22_data.values()))]
            track_binary.base_position = [0., 0., 0.]
            track_binary.base_scale    = [0., 0., 0.]
            
            controller_binary.tracks.data.append(track_binary)
         
        controller_binary.tracks.count = len(controller_binary.tracks.data)
        
        return controller_binary

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
        self.fov        = {}
        self.unknown_24 = {}

    def to_controller(self):
        tracks = []
        for dataset, keyframe_type in [
                (self.fov,         KeyframeType23),
                (self.unknown_24,  KeyframeType24)
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
    