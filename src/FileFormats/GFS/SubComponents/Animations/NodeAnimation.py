from .Binary.AnimTrack import AnimationTrackBinary
from .Binary.AnimController import AnimationControllerBinary
from .Binary.AnimTrack import NodeTR
from .Binary.AnimTrack import NodeTRS
from .Binary.AnimTrack import KeyframeType16
from .Binary.AnimTrack import KeyframeType17
from .Binary.AnimTrack import KeyframeType18
from .Binary.AnimTrack import KeyframeType19
from .Binary.AnimTrack import KeyframeType22
from .Binary.AnimTrack import KeyframeType26
from .Binary.AnimTrack import NodeTRSHalf
from .Binary.AnimTrack import KeyframeType28
from .Binary.AnimTrack import NodeTHalf
from .Binary.AnimTrack import NodeRHalf
from .Binary.AnimTrack import NodeSHalf
from .Binary.AnimTrack import NodeTSHalf
from .Binary.AnimTrack import NodeRSHalf
from .Binary.AnimTrack import NodeTR31

import numpy as np


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
    
    @classmethod
    def from_controller(cls, controller_binary):
        anim = cls(controller_binary.target_id, controller_binary.target_name.string)
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
                # WRONG but will do for now
                anim.scales    = {f: base_scale             for f     in track_binary.frames}
                anim.track_groups.append([0, 1, 2])
            elif track_binary.keyframe_type == 31:
                if isinstance(track_binary, NodeTHalf):
                    anim.compress = True
                    anim.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                    # WRONG but will do for now
                    anim.scales    = {f: base_scale             for f     in track_binary.frames}
                    anim.track_groups.append([0, 2])
                else:
                    anim.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    anim.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                    # WRONG but will do for now
                    anim.scales    = {f: base_scale             for f     in track_binary.frames}
                    anim.track_groups.append([0, 1, 2])
            elif track_binary.keyframe_type == 32:
                anim.compress = True
                anim.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                # WRONG but will do for now
                anim.scales    = {f: base_scale             for f     in track_binary.frames}
                anim.track_groups.append([1, 2])
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
    
    def to_controller(self, old_node_id_to_new_node_id_map, version):        
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
                        if version > 0x02000000:
                            raise NotImplementedError("No compressed translation keyframe after version 2")
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
                        if version > 0x02000000:
                            kf_type = NodeTR31
                        else:
                            kf_type = NodeTR
                        
                        frames,\
                        kf_values = construct_frames((self.positions, lerp),
                                                     (self.rotations, slerp))
                    elif has_floats:
                        kf_type = KeyframeType16
                        
                        frames,\
                        kf_values = construct_frames((self.unknown_floats, lerp))
                    else:
                        kf_type = NodeTRS
                        
                        if has_trans: p = self.positions
                        else:         p = {0: [0, 0, 0]}
                        if has_rot:   r = self.rotations
                        else:         r = {0: [0, 0, 0, 1]}
                        if has_scale: s = self.scales
                        else:         s = {0: [1, 1, 1]}
                        
                        frames,\
                        kf_values = construct_frames((p, lerp),
                                                     (r, slerp),
                                                     (s, lerp))
         
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


def apply_scale_to_keyframes(keyframes, scale):
    out = {}
    for key, value in keyframes.items():
        out[key] = [k/s if s != 0 else 0 for k, s in zip(value, scale)]
    return out


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
