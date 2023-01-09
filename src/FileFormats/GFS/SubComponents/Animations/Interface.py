class AnimationInterface:
    def __init__(self):
        self.tracks = []
    
    @classmethod
    def from_binary(cls, binary):
        instance = cls()
        
        for controller_binary in binary.controllers:
            track = AnimationTrack()
            track.name = controller_binary.target_name.string
            for track_binary in controller_binary.tracks:
                base_position = track_binary.base_position
                base_scale = track_binary.base_scale
                def scale_pos(pos):
                    return [p*bp for p, bp in zip(pos, base_position)]
                def scale_scl(scl):
                    return [s*bs for s, bs in zip(scl, base_scale)]
                
                if track_binary.keyframe_type == 1:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 2:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.scales    = {f: kf.scale    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 3:
                    track.unknown_data_3 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 4:
                    track.rotation = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 5:
                    track.unknown_data_5 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 6:
                    track.unknown_data_6 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 7:
                    track.unknown_data_7 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 8:
                    track.unknown_data_8 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 9:
                    track.unknown_data_9 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 10:
                    track.rotation = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 11:
                    track.unknown_data_11 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 12:
                    track.unknown_data_12 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 13:
                    track.unknown_data_13 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 14:
                    track.unknown_data_14 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 15:
                    track.unknown_data_15 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 16:
                    track.unknown_data_16 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 17:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.scales    = {f: kf.scale    for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.byte_data = {f: kf.unknown    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 18:
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.byte_data = {f: kf.unknown    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 19:
                    track.unknown_data_19 = {f: kf.unknown_1 for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.byte_data = {f: kf.unknown_2    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 20:
                    track.unknown_data_20 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 21:
                    track.unknown_data_21 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 22:
                    track.unknown_data_22 = {f: [kf.unknown_0x00, 
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
                                                 kf.unknown_0x28] for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 23:
                    track.camera_fov = {f: kf.camera_fov for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 24:
                    track.unknown_data_24 = {f: kf.unknown_float for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 25:
                    track.unknown_data_25 = {f: kf.unknown_float for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 26:
                    track.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 27:
                    track.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 28:
                    track.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 29:
                    track.unknown_data_29 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 30:
                    track.unknown_data_30 = {f: kf.unknown_float for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 31:
                    track.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 32:
                    track.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 33:
                    track.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 34:
                    track.positions = {f: scale_pos(kf.position) for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 35:
                    track.rotations = {f: kf.rotation            for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.scales    = {f: scale_scl(kf.scale)    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 36:
                    track.unknown_data_36 = {f: kf.unknown for f, kf in zip(track_binary.frames, track_binary.values)}
                
                
                instance.tracks.append(track)
        return instance
    
    
class AnimationTrack:
    def __init__(self):
        self.name = None
        self.compress_transforms = False
        self.positions = {}
        self.rotations = {}
        self.scales    = {}
        self.byte_data = {}
        self.camera_fov = {}
        self.unknown_data_3 = {}
        self.unknown_data_5 = {}
        self.unknown_data_6 = {}
        self.unknown_data_7 = {}
        self.unknown_data_8 = {}
        self.unknown_data_9 = {}
        self.unknown_data_11 = {}
        self.unknown_data_12 = {}
        self.unknown_data_13 = {}
        self.unknown_data_14 = {}
        self.unknown_data_15 = {}
        self.unknown_data_16 = {}
        self.unknown_data_19 = {}
        self.unknown_data_20 = {}
        self.unknown_data_21 = {}
        self.unknown_data_22 = {}
        self.unknown_data_24 = {}
        self.unknown_data_25 = {}
        self.unknown_data_36 = {}
        
