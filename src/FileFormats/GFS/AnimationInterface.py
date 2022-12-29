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
                if track_binary.keyframe_type == 1:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 2:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.scales    = {f: kf.scale    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 17:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.scales    = {f: kf.scale    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 26:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 27:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.scales    = {f: kf.scale    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 28:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 31:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 32:
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 33:
                    track.scales    = {f: kf.scale    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 34:
                    track.positions = {f: kf.position for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.scales    = {f: kf.scale    for f, kf in zip(track_binary.frames, track_binary.values)}
                elif track_binary.keyframe_type == 35:
                    track.rotations = {f: kf.rotation for f, kf in zip(track_binary.frames, track_binary.values)}
                    track.scales    = {f: kf.scale    for f, kf in zip(track_binary.frames, track_binary.values)}
                
                track.base_position = track_binary.base_position
                track.base_scale    = track_binary.base_scale
                
                instance.tracks.append(track)
        return instance
                    
class AnimationTrack:
    def __init__(self):
        self.name = None
        self.positions = {}
        self.rotations = {}
        self.scales    = {}
        self.base_position = [1., 1., 1.]
        self.base_scale    = [1., 1., 1.]
        
