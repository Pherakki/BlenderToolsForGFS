from .Binary import AnimationBinary
from .Binary.AnimController import AnimationControllerBinary
from .Binary.AnimTrack import AnimationTrackBinary
from .Binary.AnimTrack import KeyframeType1
from .Binary.AnimTrack import KeyframeType2
from .Binary.AnimTrack import KeyframeType3
from .Binary.AnimTrack import KeyframeType4
from .Binary.AnimTrack import KeyframeType5
from .Binary.AnimTrack import KeyframeType6
from .Binary.AnimTrack import KeyframeType7
from .Binary.AnimTrack import KeyframeType8
from .Binary.AnimTrack import KeyframeType9
from .Binary.AnimTrack import KeyframeType10
from .Binary.AnimTrack import KeyframeType11
from .Binary.AnimTrack import KeyframeType12
from .Binary.AnimTrack import KeyframeType13
from .Binary.AnimTrack import KeyframeType14
from .Binary.AnimTrack import KeyframeType15
from .Binary.AnimTrack import KeyframeType16
from .Binary.AnimTrack import KeyframeType17
from .Binary.AnimTrack import KeyframeType18
from .Binary.AnimTrack import KeyframeType19
from .Binary.AnimTrack import KeyframeType20
from .Binary.AnimTrack import KeyframeType21
from .Binary.AnimTrack import KeyframeType22
from .Binary.AnimTrack import KeyframeType23
from .Binary.AnimTrack import KeyframeType24
from .Binary.AnimTrack import KeyframeType25
from .Binary.AnimTrack import KeyframeType26
from .Binary.AnimTrack import KeyframeType27
from .Binary.AnimTrack import KeyframeType28
from .Binary.AnimTrack import KeyframeType29
from .Binary.AnimTrack import KeyframeType30
from .Binary.AnimTrack import KeyframeType31
from .Binary.AnimTrack import KeyframeType32
from .Binary.AnimTrack import KeyframeType33
from .Binary.AnimTrack import KeyframeType34
from .Binary.AnimTrack import KeyframeType35
from .Binary.AnimTrack import KeyframeType36

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

class LookAtAnims:
    def __init__(self):
        self.right = None
        self.right_factor = 0.
        self.left = None
        self.left_factor = 0.
        self.up = None
        self.up_factor = 0.
        self.down = None
        self.down_factor = 0.

class AnimationInterface:
    def __init__(self):
        self.node_animations     = []
        self.material_animations = []
        self.camera_animations   = []
        self.morph_animations    = []
        self.unknown_animations  = []
        
        self.lookat_anims = LookAtAnims()
        self.extra_track_data   = None
        self.bounding_box_max_dims = None
        self.bounding_box_min_dims = None
        self.speed = None
        self.properties = []
        
        # These are all always false
        self.flag_4  = False
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
                
        if binary.flags.has_unknown_chunk:
            instance.lookat_anims.right = cls.from_binary(binary.unknown_anim_chunk.anim_1)
            instance.lookat_anims.left  = cls.from_binary(binary.unknown_anim_chunk.anim_2)
            instance.lookat_anims.up    = cls.from_binary(binary.unknown_anim_chunk.anim_3)
            instance.lookat_anims.down  = cls.from_binary(binary.unknown_anim_chunk.anim_4)
        
            instance.lookat_anims.right_factor = cls.from_binary(binary.unknown_anim_chunk.unknown_1)
            instance.lookat_anims.left_factor  = cls.from_binary(binary.unknown_anim_chunk.unknown_2)
            instance.lookat_anims.up_factor    = cls.from_binary(binary.unknown_anim_chunk.unknown_3)
            instance.lookat_anims.down_factor  = cls.from_binary(binary.unknown_anim_chunk.unknown_4)
            
        instance.extra_track_data      = binary.extra_track_data
        instance.bounding_box_max_dims = binary.bounding_box_max_dims
        instance.bounding_box_min_dims = binary.bounding_box_min_dims
        instance.speed                 = binary.speed
        instance.properties            = binary.properties.data

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
        anim = NodeAnimation()
        
        anim.name = controller_binary.target_name.string
        anim.id   = controller_binary.target_id
            
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
            elif track_binary.keyframe_type == 2:
                anim.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.scales    = {f: kf.scale    for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 16:
                anim.unknown_floats = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 27:
                anim.compress = True
                anim.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 28:
                anim.compress = True
                anim.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 31:
                anim.compress = True
                anim.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 32:
                anim.compress = True
                anim.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 33:
                anim.compress = True
                anim.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 34:
                anim.compress = True
                anim.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 35:
                anim.compress = True
                anim.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                anim.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
            else:
                raise NotImplementedError("No instruction to convert keyframe type '{track_binary.keyframe_type}' to a Node Animation exists")
        
        return anim
        
    @staticmethod
    def _import_material_animation_binary(controller_binary):
        anim = MaterialAnimation()
        
        anim.name = controller_binary.target_name.string
        anim.id   = controller_binary.target_id
            
        for track_binary in controller_binary.tracks:
            if track_binary.keyframe_type == 6:
                anim.unknown_6 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 7:
                anim.unknown_7 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 8:
                anim.unknown_8 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 9:
                anim.unknown_9 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 11:
                anim.unknown_11 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 12:
                anim.unknown_12 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 13:
                anim.unknown_13 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 14:
                anim.unknown_14 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 15:
                anim.unknown_15 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 20:
                anim.unknown_20 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 21:
                anim.unknown_21 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 25:
                anim.unknown_25 = {f: kf.unknown_float for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 29:
                anim.unknown_29 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 30:
                anim.unknown_30 = {f: kf.unknown_float for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 36:
                anim.unknown_36 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            else:
                raise NotImplementedError("No instruction to convert keyframe type '{track_binary.keyframe_type}' to a Material Animation exists")
        
        return anim

    @staticmethod
    def _import_camera_animation_binary(controller_binary):
        anim = CameraAnimation()
        
        anim.name = controller_binary.target_name.string
        anim.id   = controller_binary.target_id
            
        for track_binary in controller_binary.tracks:
            if track_binary.keyframe_type == 23:
                anim.fov = {f: kf.camera_fov for f, kf in zip(track_binary.frames, track_binary.values)}
            elif track_binary.keyframe_type == 24:
                anim.unknown_24 = {f: kf.unknown_float for f, kf in zip(track_binary.frames, track_binary.values)}
            else:
                raise NotImplementedError("No instruction to convert keyframe type '{track_binary.keyframe_type}' to a Camera Animation exists")

        return anim

    @staticmethod
    def _import_morph_animation_binary(controller_binary):
        anim = MorphAnimation()
        
        anim.name = controller_binary.target_name.string
        anim.id   = controller_binary.target_id
            
        for track_binary in controller_binary.tracks:
            if track_binary.keyframe_type == 3:
                anim.unknown = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            else:
                raise NotImplementedError("No instruction to convert keyframe type '{track_binary.keyframe_type}' to a Morph Animation exists")
    
        return anim

    @staticmethod
    def _import_unknown_animation_binary(controller_binary):
        anim = UnknownAnimation()
        
        anim.name = controller_binary.target_name.string
        anim.id   = controller_binary.target_id
            
        for track_binary in controller_binary.tracks:
            if track_binary.keyframe_type == 5:
                anim.unknown = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
            else:
                raise NotImplementedError("No instruction to convert keyframe type '{track_binary.keyframe_type}' to a Morph Animation exists")
    
        return anim
    
    def to_binary(self, gfs):
        binary = AnimationBinary()
        
        binary.flags.has_node_anims     = len(self.node_animations)
        binary.flags.has_material_anims = len(self.material_animations)
        binary.flags.has_camera_anims   = len(self.camera_animations)
        binary.flags.has_morph_anims    = len(self.morph_animations)
        binary.flags.has_type_5_aninms  = len(self.unknown_animations)
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
        binary.flags.has_particles      = False
        binary.flags.has_unknown_chunk  = self.unknown_anim_chunk is not None
        binary.flags.has_bounding_box   = self.bounding_box_max_dims is not None
        binary.flags.has_extra_data     = self.extra_track_data is not None

        binary.unknown_anim_chunk    = self.unknown_anim_chunk
        binary.extra_track_data      = self.extra_track_data
        binary.bounding_box_max_dims = self.bounding_box_max_dims
        binary.bounding_box_min_dims = self.bounding_box_min_dims
        binary.speed                 = self.speed
        binary.properties.data       = self.properties
        binary.properties.count      = len(self.properties)
        binary.controllers.data.extend([a.to_controller(gfs) for a in self.node_animations    ])
        binary.controllers.data.extend([a.to_controller(gfs) for a in self.material_animations])
        binary.controllers.data.extend([a.to_controller(gfs) for a in self.camera_animations  ])
        binary.controllers.data.extend([a.to_controller(gfs) for a in self.morph_animations   ])
        binary.controllers.data.extend([a.to_controller(gfs) for a in self.unknown_animations ])
        binary.controllers.count     = len(binary.controllers.data)
        binary.duration = max([track.frames[-1] for ctlr in binary.controllers for track in ctlr.tracks])
        
        return binary


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


class NodeAnimation:
    def __init__(self):
        self.name = None
        self.id   = None
        self.compress = False
        self.positions = {}
        self.rotations = {}
        self.scales    = {}
        self.byte_data = {}
        self.unknown_floats = {}
        
    def to_controller(self, gfs):
        if not len(self.positions) and not len(self.rotations) and not len(self.scales) and not len(self.byte_data) and not len(self.unknown_floats):
            return []
        
        track_binary = AnimationTrackBinary()
        if self.compress:
            if len(self.positions) and len(self.rotations) and len(self.scales) and not len(self.byte_data) and not len(self.unknown_floats):
                kf_type = KeyframeType27
                
                position_scale = [max([e[i] for e in self.positions] for i in range(3))]
                scale_scale    = [max([e[i] for e in self.scale    ] for i in range(3))]
                
                frames,\
                kf_values = construct_frames(([[p/ps for p, ps in zip(pos, position_scale)] for pos in self.positions], lerp ),
                                             (self.rotations, slerp),
                                             ([[s/ss for s, ss in zip(scl, scale_scale   )] for scl in self.scale    ], lerp ))
            elif len(self.positions) and len(self.rotations) and not len(self.scales) and not len(self.byte_data) and not len(self.unknown_floats):
                kf_type = KeyframeType28
                
                position_scale = [max([e[i] for e in self.positions] for i in range(3))]
                
                frames,\
                kf_values = construct_frames(([[p/ps for p, ps in zip(pos, position_scale)] for pos in self.positions], lerp ),
                                             (self.rotations, slerp))
            else:
                raise NotImplementedError
        else:
            if len(self.positions) and len(self.rotations) and len(self.scales) and not len(self.byte_data) and not len(self.unknown_floats):
                kf_type = KeyframeType2
                
                frames,\
                kf_values = construct_frames((self.positions, lerp ),
                                             (self.rotations, slerp),
                                             (self.scale,     lerp ))
            elif len(self.positions) and len(self.rotations) and not len(self.scales) and not len(self.byte_data) and not len(self.unknown_floats):
                kf_type = KeyframeType1
                
                frames,\
                kf_values = construct_frames((self.positions, lerp),
                                             (self.rotations, slerp))
            elif len(self.unknown_floats):
                kf_type = KeyframeType16
                
                frames,\
                kf_values = construct_frames((self.unknown_floats, lerp))
            else:
                raise NotImplementedError
 
        track_binary.frames = frames
        track_binary.keyframe_type = kf_type.VARIANT_TYPE
        track_binary.keyframe_count = len(track_binary.frames)
        track_binary.values = [kf_type(*args) for args in zip(kf_values)]
        
        controller_binary = AnimationControllerBinary()
        controller_binary.type = 1
        controller_binary.target_id = self.id #[b.name for b in gfs.nodes].index(self.name)
        controller_binary.target_name = controller_binary.target_name.from_name(self.name)
        controller_binary.tracks.data = [track_binary]
        controller_binary.tracks.count = 1
        
        return controller_binary

class MaterialAnimation:
    def __init__(self):
        self.name = None
        self.id   = None
        
        self.unknown_6  = {}
        self.unknown_7  = {}
        self.unknown_8  = {}
        self.unknown_9  = {}
        self.unknown_11 = {}
        self.unknown_12 = {}
        self.unknown_13 = {}
        self.unknown_14 = {}
        self.unknown_15 = {}
        self.unknown_20 = {}
        self.unknown_21 = {}
        self.unknown_25 = {}
        self.unknown_29 = {}
        self.unknown_30 = {}
        self.unknown_36 = {}

    def to_controller(self, gfs):
        tracks = []
        for dataset, keyframe_type in [
                (self.unknown_6,  KeyframeType6 ),
                (self.unknown_7,  KeyframeType7 ),
                (self.unknown_8,  KeyframeType8 ),
                (self.unknown_9,  KeyframeType9 ),
                (self.unknown_11, KeyframeType11),
                (self.unknown_12, KeyframeType12),
                (self.unknown_13, KeyframeType13),
                (self.unknown_14, KeyframeType14),
                (self.unknown_15, KeyframeType15),
                (self.unknown_20, KeyframeType20),
                (self.unknown_21, KeyframeType21),
                (self.unknown_25, KeyframeType25),
                (self.unknown_29, KeyframeType29),
                (self.unknown_30, KeyframeType30),
                (self.unknown_36, KeyframeType36)
            ]:
            if len(dataset):
                kf_type = keyframe_type
                
                frames,\
                kf_values = construct_frames((dataset, lerp ))
                
                track_binary = AnimationTrackBinary()
                    
                track_binary.frames = frames
                track_binary.keyframe_type = kf_type.VARIANT_TYPE
                track_binary.keyframe_count = len(track_binary.frames)
                track_binary.values = [kf_type(*args) for args in zip(kf_values)]
                
                tracks.append(track_binary)
        
        controller_binary = AnimationControllerBinary()
        controller_binary.type = 2
        controller_binary.target_id = self.id # [b.name for b in gfs.materials].index(self.name)
        controller_binary.target_name = controller_binary.target_name.from_name(self.name)
        controller_binary.tracks.data = tracks
        controller_binary.tracks.count = len(tracks)
        
        return controller_binary
        
class CameraAnimation:
    def __init__(self):
        self.name = None
        self.id   = None
        self.fov        = {}
        self.unknown_24 = {}

    def to_controller(self, gfs):
        tracks = []
        for dataset, keyframe_type in [
                (self.fov,         KeyframeType23),
                (self.unknown_24,  KeyframeType24)
            ]:
            if len(dataset):
                kf_type = keyframe_type
                
                frames,\
                kf_values = construct_frames((dataset, lerp ))
                
                track_binary = AnimationTrackBinary()
                    
                track_binary.frames = frames
                track_binary.keyframe_type = kf_type.VARIANT_TYPE
                track_binary.keyframe_count = len(track_binary.frames)
                track_binary.values = [kf_type(*args) for args in zip(kf_values)]
                
                tracks.append(track_binary)
                
        controller_binary = AnimationControllerBinary()
        controller_binary.type = 3
        controller_binary.target_id = self.id # [b.name for b in gfs.cameras].index(self.name)
        controller_binary.target_name = controller_binary.target_name.from_name(self.name)
        controller_binary.tracks.data = tracks
        controller_binary.tracks.count = len(tracks)
        
        return controller_binary

class MorphAnimation:
    def __init__(self):
        self.name = None
        self.id
        self.unknown = {}

    def to_controller(self, gfs):
        raise NotImplementedError
    
        tracks = []
        for dataset, keyframe_type in [
                (self.unknown, KeyframeType3)
            ]:
            if len(dataset):
                kf_type = keyframe_type
                
                frames,\
                kf_values = construct_frames((dataset, lerp ))
                
                track_binary = AnimationTrackBinary()
                    
                track_binary.frames = frames
                track_binary.keyframe_type = kf_type.VARIANT_TYPE
                track_binary.keyframe_count = len(track_binary.frames)
                track_binary.values = [kf_type(*args) for args in zip(kf_values)]
                
                tracks.append(track_binary)
                
        controller_binary = AnimationControllerBinary()
        controller_binary.type = 4
        controller_binary.target_id = self.id #[b.name for b in gfs.morphs].index(self.name)
        controller_binary.target_name = controller_binary.target_name.from_name(self.name)
        controller_binary.tracks.data = tracks
        controller_binary.tracks.count = len(tracks)
        
        return controller_binary
    
class UnknownAnimation:
    def __init__(self):
        self.name = None
        self.id = None
        self.unknown = {}

    def to_controller(self, gfs):
        raise NotImplementedError
    
        tracks = []
        for dataset, keyframe_type in [
                (self.unknown, KeyframeType5)
            ]:
            if len(dataset):
                kf_type = keyframe_type
                
                frames,\
                kf_values = construct_frames((dataset, lerp ))
                
                track_binary = AnimationTrackBinary()
                    
                track_binary.frames = frames
                track_binary.keyframe_type = kf_type.VARIANT_TYPE
                track_binary.keyframe_count = len(track_binary.frames)
                track_binary.values = [kf_type(*args) for args in zip(kf_values)]
                
                tracks.append(track_binary)
                
        controller_binary = AnimationControllerBinary()
        controller_binary.type = 5
        controller_binary.target_id = self.id #[b.name for b in gfs.morphs].index(self.name)
        controller_binary.target_name = controller_binary.target_name.from_name(self.name)
        controller_binary.tracks.data = tracks
        controller_binary.tracks.count = len(tracks)
        
        return controller_binary
    