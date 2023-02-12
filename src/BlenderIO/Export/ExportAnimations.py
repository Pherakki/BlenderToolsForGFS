import io

import bpy
from mathutils import Matrix, Quaternion
import numpy as np

from ...serialization.BinaryTargets import Reader
from ...FileFormats.GFS.SubComponents.Animations import AnimationInterface, AnimationBinary
from ..Utils.Maths import convert_rotation_to_quaternion, transform_node_animations
from ..Utils.Interpolation import interpolate_keyframe_dict, lerp, slerp


def export_animations(gfs, armature):
    if armature.animation_data is not None:
        ap_props = armature.data.GFSTOOLS_AnimationPackProperties
        
        gfs.anim_flag_0  = ap_props.flag_0
        gfs.anim_flag_1  = ap_props.flag_1
        gfs.anim_flag_3  = ap_props.flag_3
        gfs.anim_flag_4  = ap_props.flag_4
        gfs.anim_flag_5  = ap_props.flag_5
        gfs.anim_flag_6  = ap_props.flag_6
        gfs.anim_flag_7  = ap_props.flag_7
        gfs.anim_flag_8  = ap_props.flag_8
        gfs.anim_flag_9  = ap_props.flag_9
        gfs.anim_flag_10 = ap_props.flag_10
        gfs.anim_flag_11 = ap_props.flag_11
        gfs.anim_flag_12 = ap_props.flag_12
        gfs.anim_flag_13 = ap_props.flag_13
        gfs.anim_flag_14 = ap_props.flag_14
        gfs.anim_flag_15 = ap_props.flag_15
        gfs.anim_flag_16 = ap_props.flag_16
        gfs.anim_flag_17 = ap_props.flag_17
        gfs.anim_flag_18 = ap_props.flag_18
        gfs.anim_flag_19 = ap_props.flag_19
        gfs.anim_flag_20 = ap_props.flag_20
        gfs.anim_flag_21 = ap_props.flag_21
        gfs.anim_flag_22 = ap_props.flag_22
        gfs.anim_flag_23 = ap_props.flag_23
        gfs.anim_flag_24 = ap_props.flag_24
        gfs.anim_flag_25 = ap_props.flag_25
        gfs.anim_flag_26 = ap_props.flag_26
        gfs.anim_flag_27 = ap_props.flag_27
        gfs.anim_flag_28 = ap_props.flag_28
        gfs.anim_flag_29 = ap_props.flag_29
        gfs.anim_flag_30 = ap_props.flag_30
        gfs.anim_flag_31 = ap_props.flag_31

        for track in armature.animation_data.nla_tracks:
            if track.name == "Rest Pose":
                continue
            if not len(track.strips):
                continue
            action = track.strips[0].action
            if   action.GFSTOOLS_AnimationProperties.category == "NORMAL": export_animation(armature, gfs.add_animation(),       track)
            elif action.GFSTOOLS_AnimationProperties.category == "BLEND":  export_animation(armature, gfs.add_blend_animation(), track)
        export_lookat_animations(armature, ap_props, gfs)

def export_lookat_animations(armature, props, gfs_obj):
        if props.has_lookat_anims:
            la_up, la_down, la_left, la_right = gfs_obj.add_lookat_animations(
                props.lookat_up_factor, 
                props.lookat_down_factor, 
                props.lookat_left_factor, 
                props.lookat_right_factor
            )
            
            export_animation(armature, la_up,    armature.animation_data.nla_tracks[props.lookat_up])
            export_animation(armature, la_down,  armature.animation_data.nla_tracks[props.lookat_down])
            export_animation(armature, la_left,  armature.animation_data.nla_tracks[props.lookat_left])
            export_animation(armature, la_right, armature.animation_data.nla_tracks[props.lookat_right])
        

def export_animation(armature, gfs_anim, nla_track):
    strip = nla_track.strips[0]
    action = strip.action
    
    # EXPORT NODE ANIMS
    node_transforms = get_action_data(action, armature)
    for (bidx, bname, t, r, s) in sorted(node_transforms, key=lambda x: x[0]):
        anim = gfs_anim.add_node_animation(bidx, bname)
        anim.positions = t
        anim.rotations = r
        anim.scales    = s
    
    # Export extra data
    props = action.GFSTOOLS_AnimationProperties
    gfs_anim.flag_0  = props.flag_0
    gfs_anim.flag_1  = props.flag_1
    gfs_anim.flag_2  = props.flag_2
    gfs_anim.flag_3  = props.flag_3
    gfs_anim.flag_4  = props.flag_4
    gfs_anim.flag_5  = props.flag_5
    gfs_anim.flag_6  = props.flag_6
    gfs_anim.flag_7  = props.flag_7
    gfs_anim.flag_8  = props.flag_8
    gfs_anim.flag_9  = props.flag_9
    gfs_anim.flag_10 = props.flag_10
    gfs_anim.flag_11 = props.flag_11
    gfs_anim.flag_12 = props.flag_12
    gfs_anim.flag_13 = props.flag_13
    gfs_anim.flag_14 = props.flag_14
    gfs_anim.flag_15 = props.flag_15
    gfs_anim.flag_16 = props.flag_16
    gfs_anim.flag_17 = props.flag_17
    gfs_anim.flag_18 = props.flag_18
    gfs_anim.flag_19 = props.flag_19
    gfs_anim.flag_20 = props.flag_20
    gfs_anim.flag_21 = props.flag_21
    gfs_anim.flag_22 = props.flag_22
    gfs_anim.flag_24 = props.flag_24
    gfs_anim.flag_26 = props.flag_26
    gfs_anim.flag_27 = props.flag_27
    
    
    # Export extra track + other data
    unimported_tracks = AnimationInterface()
    if len(props.unimported_tracks):
        stream = io.BytesIO()
        stream.write(bytes.fromhex(props.unimported_tracks))
        stream.seek(0)
        rdr = Reader(None)
        rdr.bytestream = stream
        ab = AnimationBinary()
        rdr.rw_obj(ab, 0x01105100)
        unimported_tracks = AnimationInterface.from_binary(ab)
    
    if props.category == "NORMAL":
        export_lookat_animations(armature, props, gfs_anim)
        gfs_anim.extra_track_data = unimported_tracks.extra_track_data
        
    gfs_anim.material_animations = unimported_tracks.material_animations
    gfs_anim.camera_animations   = unimported_tracks.camera_animations
    gfs_anim.morph_animations    = unimported_tracks.morph_animations
    gfs_anim.unknown_animations  = unimported_tracks.unknown_animations
    
    # If scale is outside the range 0.995 - 1.005...
    if abs(strip.scale - 1) > 0.005:
        gfs_anim.speed = 1 / strip.scale
    
    # Export the custom properties
    for prop in props.properties:
        gfs_anim.add_property(*prop.extract_data(prop))
    
    # # Only for Blend and LookAt animations
    # has_scale_action:   bpy.props.BoolProperty("Has Scale Channel")
    # blend_scale_action: bpy.props.EnumProperty(name="Scale Channel", items=find_blendscales)


#############################
# STUFF THAT SHOULD BE USED #
#############################
def get_action_data(action, armature):
    curve_defaults = {'location': [0., 0., 0.],
                      'rotation_quaternion': [1., 0., 0., 0.],
                      'scale': [1., 1., 1.],
                      'rotation_euler': [0, 0, 0]}
    
    bone_names = [b.name for b in armature.data.bones]
    out = []
    animation_data = {}
    fcurve_groups = group_fcurves_by_bone_and_type(action)
    for bone_name, group in fcurve_groups.items():
        if bone_name not in armature.pose.bones:
            continue
        animation_data[bone_name] = {'rotation_quaternion': {},
                                     'location': {},
                                     'scale': {},
                                     'rotation_euler': {}}
        # Get whether any of the locations, rotations, and scales are animated; plus the f-curves for those
        # that are
        elements_used, bone_data = get_used_animation_elements_in_group(group)
        # For each set that is animated, interpolate missing keyframes for each component of the relevant vector
        # on each keyframe where at least one element is used
        for curve_type, isUsed in elements_used.items():
            if isUsed:
                curve_data = interpolate_missing_frame_elements(bone_data[curve_type], curve_defaults[curve_type], lerp)
                zipped_data = zip_vector_elements(curve_data)
                animation_data[bone_name][curve_type] = zipped_data
           
        rotation_mode = armature.pose.bones[bone_name].rotation_mode
        if rotation_mode != "QUATERNION":
            animation_data[bone_name]["rotation_quaternion"] = {
                k: convert_rotation_to_quaternion(None, v, rotation_mode) 
                for k, v in animation_data[bone_name]["rotation_euler"]
            }
        
        if "rotation_quaternion" in animation_data[bone_name]:
            animation_data[bone_name]["rotation_quaternion"] = {
                k: [v[1], v[2], v[3], v[0]] 
                for k, v in animation_data[bone_name]["rotation_quaternion"].items()
                }
            
        bpy_bone = armature.data.bones[bone_name]
        if bpy_bone.parent is not None:
            base_matrix = bpy_bone.parent.matrix_local.inverted() @ bpy_bone.matrix_local
        else:
            base_matrix = bpy_bone.matrix_local

        t, r, s = transform_node_animations(animation_data[bone_name].get("location", {}),
                                            animation_data[bone_name].get("rotation_quaternion", {}),
                                            animation_data[bone_name].get("scale", {}),
                                            base_matrix)
        
        
        fps = 30
        out.append([bone_names.index(bone_name), bone_name, 
                    {(k-1)/fps : v for k, v in t.items()}, 
                    {(k-1)/fps : v for k, v in r.items()}, 
                    {(k-1)/fps : v for k, v in s.items()}])
        
    print(out[[a[1] for a in out].index("Bip01 R Forearm")])
    return out


#####################
# UTILITY FUNCTIONS #
#####################

def get_bone_name_from_fcurve(fcurve):
    return fcurve.data_path.split('[')[1].split(']')[0][1:-1]


def get_fcurve_type(fcurve):
    return fcurve.data_path.split('.')[-1]


def group_fcurves_by_bone_and_type(action):
    res = {}
    for fcurve in action.fcurves:
        if fcurve.data_path[:10] == 'pose.bones':
            bone_name = get_bone_name_from_fcurve(fcurve)
            if bone_name not in res:
                res[bone_name] = {'rotation_quaternion': [None, None, None, None],
                                  'location':            [None, None, None],
                                  'scale':               [None, None, None],
                                  'rotation_euler':      [None, None, None]}
            curve_type = get_fcurve_type(fcurve)
            array_index = fcurve.array_index

            # Get value of first keyframe point
            res[bone_name][curve_type][array_index] = fcurve
    return res


def get_used_animation_elements_in_group(group):
    """
    Summary
    -------
    Takes a list of f-curves and assigns the keyframe point co-ordinates in each f-curve to the appropriate transform
    and array index of a returned dictionary.

    The animation export module should probably be refactored so that the groups that get passed into this function
    are either locations, rotations, or scales, so that all three are not handled simultaneously, but rather by three
    separate function calls.

    Parameters
    ----------
    :parameters:
    group -- A list of Blender f-curve objects.

    Returns
    -------
    :returns:
    A two-element tuple:
    - The first element is a dictionary in the shape {'location': bool, 'rotation_quaternion': bool, 'scale': bool} that
      states whether any of the input f-curves are of any of those types
    - The second element is a dictionary in the shape
                {'location': {0: {}, 1: {}, 2: {}},
                 'rotation_quaternion': {0: {}, 1: {}, 2: {}, 3: {}},
                 'scale': {0: {}, 1: {}, 2: {}}},
      where the integers are the array indices of the appropriate f-curves. Each array index is also given a dictionary
      as above, which contains the frame index and the f-curve value as key-value pairs.
    """
    elements_used = {'location': False,
                     'rotation_quaternion': False,
                     'scale': False,
                     'rotation_euler': False}

    bone_data = {'rotation_quaternion': [{}, {}, {}, {}],
                 'location':            [{}, {}, {}],
                 'scale':               [{}, {}, {}],
                 'rotation_euler': [{}, {}, {}]}
    for curve_type in group:
        for curve_idx, f_curve in enumerate(group[curve_type]):
            if f_curve is None:
                continue
            elements_used[curve_type] = True
            bone_data[curve_type][curve_idx] = {k-1: v for k, v in [kfp.co for kfp in f_curve.keyframe_points]}

    return elements_used, bone_data


def get_all_required_frames(curve_data):
    """
    Returns all keys in a list of dictionaries as a sorted list of rounded integers plus the rounded-up final key,
    assuming all keys are floating-point values.
    """
    res = set()
    for dct in curve_data:
        iter_keys = tuple(dct.keys())
        for key in iter_keys:
            res.add(key)
    return sorted(list(res))


def interpolate_missing_frame_elements(curve_data, default_values, interpolation_function):
    """
    GFS requires animations to be stored as whole quaternions, locations, and scales.
    This function ensures that every passed f-curve has a value at every frame referenced by all f-curves - e.g. if
    a location has values at frame 30 on its X f-curve but not on its Y and Z f-curves, the Y and Z values at frame 30
    will be interpolated from the nearest frames on the Y and Z f-curves respectively and stored in the result.
    """
    # First get every frame required by the vector and which will be passed on to GFS
    all_frame_idxs = get_all_required_frames(curve_data)
    for (component_idx, framedata), default_value in zip(enumerate(curve_data), default_values):
        # Get all the frames at which the curve has data
        component_frame_idxs = list(framedata.keys())
        # Produce a function that will return the value for the frame, based on how many frames are available
        interp_method = produce_interpolation_method(component_frame_idxs, framedata, default_value, interpolation_function)
        new_framedata = {}
        # Generate the GFS-compatible data
        for frame_idx in all_frame_idxs:
            if frame_idx not in component_frame_idxs:
                new_framedata[frame_idx] = interp_method(frame_idx)
            else:
                new_framedata[frame_idx] = framedata[frame_idx]

        curve_data[component_idx] = new_framedata

    return curve_data


def zip_vector_elements(curve_data):
    """
    Takes n dictionaries in a list, with each dictionary containing the frame indices (as keys) and values (as values)
    of a single component of a vector. All dictionaries must have exactly the same keys (frame indices).
    Returns a single dictionary with the frame indices as keys, and the vector components for that frame stored in a
    list as the value for that key.
    """
    new_curve_data = {}
    for frame_idxs in zip(*[list(e.keys()) for e in curve_data]):
        for frame_idx in frame_idxs:
            assert frame_idx == frame_idxs[0]
        frame_idx = frame_idxs[0]
        new_curve_data[frame_idx] = [e[frame_idx] for e in curve_data]
    return new_curve_data


def interpolate_keyframe(frame_idxs, frame_values, idx, interpolation_function):
    smaller_elements = [fidx for fidx in frame_idxs if idx >= fidx]
    next_smallest_frame = max(smaller_elements) if len(smaller_elements) else frame_idxs[0]
    larger_elements = [fidx for fidx in frame_idxs if idx <= fidx]
    next_largest_frame = min(larger_elements) if len(larger_elements) else frame_idxs[-1]

    if next_largest_frame == next_smallest_frame:
        t = 0  # Totally arbitrary, since the interpolation will be between two identical values
    else:
        t = (idx - next_smallest_frame) / (next_largest_frame - next_smallest_frame)

    # Should change lerp to the proper interpolation method
    min_value = frame_values[next_smallest_frame]
    max_value = frame_values[next_largest_frame]

    return interpolation_function(np.array(min_value), np.array(max_value), t)


def produce_interpolation_method(frame_idxs, frame_values, default_value, interpolation_function):
    """
    Returns an interpolation function dependant on the number of passed frames.
    """
    if len(frame_idxs) == 0:
        def interp_method(input_frame_idx):
            return default_value
    elif len(frame_idxs) == 1:
        value = frame_values[frame_idxs[0]]

        def interp_method(input_frame_idx):
            return value
    else:
        def interp_method(input_frame_idx):
            return interpolate_keyframe(frame_idxs, frame_values, input_frame_idx, interpolation_function)

    return interp_method
