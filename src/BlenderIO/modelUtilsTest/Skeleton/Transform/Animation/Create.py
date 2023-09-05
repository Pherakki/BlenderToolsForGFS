def create_nla_track(action, armature, blend_type):
    armature.animation_data.action = action
    track = armature.animation_data.nla_tracks.new()
    track.name = action.name
    track.mute = True
    strip = track.strips.new(action.name, 1, action)
    strip.blend_type = blend_type
    armature.animation_data.action = None
