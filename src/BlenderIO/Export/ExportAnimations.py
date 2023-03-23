import io

import bpy
from mathutils import Matrix, Quaternion, Vector
import numpy as np

from ...serialization.BinaryTargets import Reader
from ...FileFormats.GFS.SubComponents.Animations import AnimationInterface, AnimationBinary
from ...FileFormats.GFS.SubComponents.Animations.Binary.AnimationBinary import EPLEntry
from ..Utils.Maths import convert_rotation_to_quaternion, convert_XDirBone_to_YDirBone, convert_Zup_to_Yup
from ..Utils.Interpolation import lerp


def export_animations(gfs, armature, keep_unused_anims):
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
            if   action.GFSTOOLS_AnimationProperties.category == "NORMAL": export_animation(gfs, armature, gfs.add_animation(),       action, is_blend=False, keep_unused_anims=keep_unused_anims)
            elif action.GFSTOOLS_AnimationProperties.category == "BLEND":  export_animation(gfs, armature, gfs.add_blend_animation(), action, is_blend=True,  keep_unused_anims=keep_unused_anims)
        export_lookat_animations(armature, ap_props, gfs, keep_unused_anims)

def export_lookat_animations(armature, props, gfs_obj, keep_unused_anims):
        if props.has_lookat_anims:
            la_up, la_down, la_left, la_right = gfs_obj.add_lookat_animations(
                props.lookat_up_factor, 
                props.lookat_down_factor, 
                props.lookat_left_factor, 
                props.lookat_right_factor
            )
            
            export_animation(gfs_obj, armature, la_up,    props.lookat_up,    is_blend=True, keep_unused_anims=keep_unused_anims)
            export_animation(gfs_obj, armature, la_down,  props.lookat_down,  is_blend=True, keep_unused_anims=keep_unused_anims)
            export_animation(gfs_obj, armature, la_left,  props.lookat_left,  is_blend=True, keep_unused_anims=keep_unused_anims)
            export_animation(gfs_obj, armature, la_right, props.lookat_right, is_blend=True, keep_unused_anims=keep_unused_anims)


def export_animation(gfs_obj, armature, gfs_anim, action, is_blend, keep_unused_anims):
    # EXPORT NODE ANIMS
    animated_nodes = set()
    node_transforms, root_transform = get_action_data(action, armature, is_blend)
    
    if is_blend:
        # First export the translations and rotations
        node_anims = {}
        for (bidx, bname, t, r, _) in sorted(node_transforms, key=lambda x: x[0]):
            anim = gfs_anim.add_node_animation(bidx, bname)
            anim.positions = t
            anim.rotations = r
            animated_nodes.add(bname)
            node_anims[bname] = anim
        
        if root_transform is not None:
            bidx, bname, t, r, s = root_transform
            root_anim = gfs_anim.add_node_animation(bidx, bname)
            root_anim.positions = t
            root_anim.rotations = r
            animated_nodes.add(bname)
        
        # Now get the scale track
        # The scale track needs to be separated since it's additive, not
        # multiplicative
        if action.GFSTOOLS_AnimationProperties.has_scale_action:
            scale_action = action.GFSTOOLS_AnimationProperties.blend_scale_action
            if scale_action is not None:
                scale_transforms, root_scale = get_action_data(scale_action, armature, is_blend)
                
                for (bidx, bname, _, _, s) in sorted(scale_transforms, key=lambda x: x[0]):
                    node_anim = node_anims.get(bname)
                    if node_anim is None:
                        node_anim = gfs_anim.add_node_animation(bidx, bname)
                    node_anim.scales = s
                    
                if root_transform is not None:
                    root_anim.scales = root_scale[-1]
    else:
        for (bidx, bname, t, r, s) in sorted(node_transforms, key=lambda x: x[0]):
            anim = gfs_anim.add_node_animation(bidx, bname)
            anim.positions = t
            anim.rotations = r
            anim.scales    = s
            animated_nodes.add(bname)
        
        if root_transform is not None:
            bidx, bname, t, r, s = root_transform
            anim = gfs_anim.add_node_animation(bidx, bname)
            anim.positions = t
            anim.rotations = r
            anim.scales    = s
            animated_nodes.add(bname)
    
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
        export_lookat_animations(armature, props, gfs_anim, keep_unused_anims)
        gfs_anim.extra_track_data = unimported_tracks.extra_track_data
        
    # Export unused bone animations
    bone_names = [b.name for b in gfs_obj.bones]
    for track in unimported_tracks.node_animations:
        if track.name not in animated_nodes:
            if remap_track_id(track, bone_names, keep_unused_anims, offset=1):
                gfs_anim.node_animations.append(track)
    
    # Export unused material animations
    material_names = [m.name for m in gfs_obj.materials]
    for track in unimported_tracks.material_animations:
        if remap_track_id(track, material_names, keep_unused_anims):
            gfs_anim.material_animations.append(track)
            
    # Export unused camera animations
    camera_names = [bone_names[cam.node] for cam in gfs_obj.cameras]
    for track in unimported_tracks.camera_animations:
        if remap_track_id(track, camera_names, keep_unused_anims):
            gfs_anim.camera_animations.append(track)
            
    # Export unused morph animations
    morph_names = [bone_names[mesh.node] for mesh in gfs_obj.meshes if len(mesh.morphs)]
    for track in unimported_tracks.morph_animations:
        if remap_track_id(track, morph_names, keep_unused_anims):
            gfs_anim.morph_animations.append(track)
            
    # Absolutely no idea what these are. Better not do anything important...
    gfs_anim.unknown_animations  = unimported_tracks.unknown_animations
    
    # Bake the speed into the frame times, no sensible way to separate speed and
    # frame times in Blender sadly
    gfs_anim.speed = None
    
    # Export the custom properties
    for prop in props.properties:
        gfs_anim.add_property(*prop.extract_data(prop))
    
    # Export bone epls
    for epl_prop in props.epls:
        stream = io.BytesIO()
        stream.write(bytes.fromhex(epl_prop.blob))
        stream.seek(0)
        rdr = Reader(None)
        rdr.bytestream = stream
        epl_entry = EPLEntry(endianness=">")
        rdr.rw_obj(epl_entry, 0x01105100)
        
        gfs_anim.epls.append(epl_entry)


def remap_track_id(track, names, keep_unused_anims, offset=0):
    elem_idx = next((i for i, nm in enumerate(names) if track.name == nm), None)
    if elem_idx is None:
        if keep_unused_anims:
            track.id = 0
        else:
            return False
    else:
        track.id = elem_idx + offset
    
    return True

#############################
# STUFF THAT SHOULD BE USED #
#############################
def get_action_data(action, armature, is_blend):
    curve_defaults = {'location': [0., 0., 0.],
                      'rotation_quaternion': [1., 0., 0., 0.],
                      'scale': [1., 1., 1.],
                      'rotation_euler': [0, 0, 0]}
    
    bone_names = [b.name for b in armature.data.bones]
    out = []
    animation_data = {}
    fcurve_groups, obj_transforms = group_fcurves_by_bone_and_type(action)
    for bone_name, group in fcurve_groups.items():
        if bone_name not in armature.pose.bones:
            continue
        animation_data[bone_name] = {'rotation_quaternion': {},
                                     'location': {},
                                     'scale': {},
                                     'rotation_euler': {}}
        extract_clean_animation_data(group, curve_defaults, animation_data[bone_name], armature.pose.bones[bone_name])
        
        if is_blend:
            # Extract animation data
            positions = animation_data[bone_name].get("location", {})
            rotations = animation_data[bone_name].get("rotation_quaternion", {})
            scales    = animation_data[bone_name].get("scale", {})
            
            # Get the matrices required to convert animations from Blender -> GFS
            axis_conversion = convert_XDirBone_to_YDirBone(Matrix.Identity(4))
            bpy_bone = armature.data.bones[bone_name]
            if bpy_bone.parent is not None:
                local_bind_matrix = axis_conversion @ bpy_bone.parent.matrix_local.inverted() @ bpy_bone.matrix_local
            else:
                local_bind_matrix = convert_Zup_to_Yup(bpy_bone.matrix_local)
                
            # This can DEFINITELY be made more efficient if it's a bottleneck
            bind_pose_translation, bind_pose_quaternion, _ = local_bind_matrix.decompose()
            bind_pose_rotation     = bind_pose_quaternion.to_matrix().to_4x4()
            inv_bind_pose_rotation = bind_pose_rotation.inverted()
            inv_axis_conversion    = axis_conversion.inverted()
            
            g_positions = {k: bind_pose_rotation @ Matrix.Translation(v)                                      @ inv_bind_pose_rotation for k, v in positions.items()}
            g_rotations = {k: axis_conversion    @ Quaternion([v[3], v[0], v[1], v[2]]).to_matrix().to_4x4()  @ inv_axis_conversion    for k, v in rotations.items()}
            g_scales    = {k: axis_conversion    @ Matrix.Diagonal([*v, 1.])                                  @ inv_axis_conversion    for k, v in scales.items()   }
            
            g_positions = {k: v.decompose()[0]     for k, v in g_positions.items()}
            g_rotations = {k: q.decompose()[1]     for k, q in g_rotations.items()}
            g_rotations = {k: [q.x, q.y, q.z, q.w] for k, q in g_rotations.items()}
            g_scales    = {k: v.decompose()[2]     for k, v in g_scales.items()}
        else:
            # Extract animation data
            positions = animation_data[bone_name].get("location", {})
            rotations = animation_data[bone_name].get("rotation_quaternion", {})
            scales    = animation_data[bone_name].get("scale", {})
            
            # Get the matrices required to convert animations from Blender -> GFS
            axis_conversion = convert_XDirBone_to_YDirBone(Matrix.Identity(4))
            bpy_bone = armature.data.bones[bone_name]
            if bpy_bone.parent is not None:
                local_bind_matrix = axis_conversion @ bpy_bone.parent.matrix_local.inverted() @ bpy_bone.matrix_local
            else:
                local_bind_matrix = convert_Zup_to_Yup(bpy_bone.matrix_local)
                
            # This can DEFINITELY be made more efficient if it's a bottleneck
            bind_pose_translation, bind_pose_quaternion, _ = local_bind_matrix.decompose()
            bind_pose_rotation     = bind_pose_quaternion.to_matrix().to_4x4()
            inv_bind_pose_rotation = bind_pose_rotation.inverted()
            inv_axis_conversion    = axis_conversion.inverted()
            bptm = Matrix.Translation(bind_pose_translation)
            
            g_positions = {k: (bind_pose_rotation @ Matrix.Translation(Vector(v))                              @ inv_bind_pose_rotation) + bptm for k, v in positions.items()}
            g_rotations = {k: bind_pose_rotation  @ Quaternion([v[3], v[0], v[1], v[2]]).to_matrix().to_4x4()  @ inv_axis_conversion            for k, v in rotations.items()}
            g_scales    = {k: axis_conversion     @ Matrix.Diagonal([*v, 1.])                                  @ inv_axis_conversion            for k, v in scales.items()   }
            
            g_positions = {k: v.decompose()[0]     for k, v in g_positions.items()}
            g_rotations = {k: q.decompose()[1]     for k, q in g_rotations.items()}
            g_rotations = {k: [q.x, q.y, q.z, q.w] for k, q in g_rotations.items()}
            g_scales    = {k: v.decompose()[2]     for k, v in g_scales.items()}
        
        fps = 30
        out.append([bone_names.index(bone_name) + 1, bone_name, 
                    {(k-1)/fps : v for k, v in g_positions.items()}, 
                    {(k-1)/fps : v for k, v in g_rotations.items()}, 
                    {(k-1)/fps : v for k, v in g_scales.items()}])
        
        if bone_name == "frost_dam":
            print(g_rotations())

    root_animation = None
    if obj_transforms is not None:
        root_animation_buffer = {'rotation_quaternion': {},
                                 'location':            {},
                                 'scale':               {},
                                 'rotation_euler':      {}}
        extract_clean_animation_data(obj_transforms, curve_defaults, root_animation_buffer, armature)
    
        # Extract animation data
        positions = root_animation_buffer.get("location", {})
        rotations = root_animation_buffer.get("rotation_quaternion", {})
        rotations = {k: [q.x, q.y, q.z, q.w] for k, q in rotations.items()}
        scales    = root_animation_buffer.get("scale", {})
    
        fps = 30
        root_animation = ([0, armature.data.GFSTOOLS_ModelProperties.root_node_name, 
                          {(k-1)/fps : v for k, v in positions.items()}, 
                          {(k-1)/fps : v for k, v in rotations.items()}, 
                          {(k-1)/fps : v for k, v in scales.items()}])
        
    return out, root_animation


#####################
# UTILITY FUNCTIONS #
#####################

def get_bone_name_from_fcurve(fcurve):
    return fcurve.data_path.split('[')[1].split(']')[0][1:-1]


def get_fcurve_type(fcurve):
    return fcurve.data_path.split('.')[-1]


def create_anim_init_data():
    return {'rotation_quaternion': [None, None, None, None],
            'location':            [None, None, None],
            'scale':               [None, None, None],
            'rotation_euler':      [None, None, None]}


def group_fcurves_by_bone_and_type(action):
    res = {}
    possible_transforms = set(create_anim_init_data().keys())
    obj_transforms = None
    
    for fcurve in action.fcurves:
        # Bone transform
        if fcurve.data_path[:10] == 'pose.bones':
            bone_name = get_bone_name_from_fcurve(fcurve)
            if bone_name not in res: res[bone_name] = create_anim_init_data()
            curve_type = get_fcurve_type(fcurve)
            edit_transforms = res[bone_name]
        # Object transforms
        elif fcurve.data_path in possible_transforms:
            if obj_transforms is None: obj_transforms = create_anim_init_data()
            curve_type = fcurve.data_path
            edit_transforms = obj_transforms
        else:
            continue
        
        array_index = fcurve.array_index
        edit_transforms[curve_type][array_index] = fcurve
            
    return res, obj_transforms


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
                 'rotation_euler':      [{}, {}, {}]}
    for curve_type in group:
        for curve_idx, f_curve in enumerate(group[curve_type]):
            if f_curve is None:
                continue
            elements_used[curve_type] = True
            bone_data[curve_type][curve_idx] = {k: v for k, v in [kfp.co for kfp in f_curve.keyframe_points]}

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


def extract_clean_animation_data(group, curve_defaults, out_buffer, pose_object):
    # Get whether any of the locations, rotations, and scales are animated; plus the f-curves for those
    # that are
    elements_used, bone_data = get_used_animation_elements_in_group(group)
    # For each set that is animated, interpolate missing keyframes for each component of the relevant vector
    # on each keyframe where at least one element is used
    for curve_type, isUsed in elements_used.items():
        if isUsed:
            curve_data = interpolate_missing_frame_elements(bone_data[curve_type], curve_defaults[curve_type], lerp)
            zipped_data = zip_vector_elements(curve_data)
            out_buffer[curve_type] = zipped_data
       
    rotation_mode = pose_object.rotation_mode
    if rotation_mode != "QUATERNION":
        out_buffer["rotation_quaternion"] = {
            k: convert_rotation_to_quaternion(None, v, rotation_mode) 
            for k, v in out_buffer["rotation_euler"].items()
        }
    
    elif "rotation_quaternion" in out_buffer:
        out_buffer["rotation_quaternion"] = {
            k: [v[1], v[2], v[3], v[0]] 
            for k, v in out_buffer["rotation_quaternion"].items()
        }
