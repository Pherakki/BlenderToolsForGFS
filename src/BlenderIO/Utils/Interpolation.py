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
