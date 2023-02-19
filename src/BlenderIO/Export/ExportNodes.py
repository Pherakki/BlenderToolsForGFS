import math

import bpy
from mathutils import Matrix, Quaternion

from ..Utils.Maths import convert_rotation_to_quaternion, convert_YDirBone_to_XDirBone, convert_Zup_to_Yup, BlenderBoneToMayaBone


def export_node_tree(gfs, armature, errorlog):
    gfs.keep_bounding_box    = armature.data.GFSTOOLS_ModelProperties.export_bounding_box
    gfs.keep_bounding_sphere = armature.data.GFSTOOLS_ModelProperties.export_bounding_sphere
    gfs.flag_3               = armature.data.GFSTOOLS_ModelProperties.flag_3
    
    # Get the rest pose if it exists
    rest_pose_action = None
    if armature.animation_data is not None:
        rest_pose_nla = armature.animation_data.nla_tracks.get("Rest Pose", None)
        if rest_pose_nla is not None:
            if len(rest_pose_nla.strips):
                rest_pose_action = rest_pose_nla.strips[0].action
    rest_pose_matrices = extract_first_frame(rest_pose_action, armature.pose.bones)
    
    # Add root node
    rn_props = armature.data.GFSTOOLS_NodeProperties
    root_node = gfs.add_node(-1, armature.data.GFSTOOLS_ModelProperties.root_node_name,
                              [0., 0., 0.], [0., 0., 0., 1.],  [1., 1., 1.], 
                              rn_props.unknown_float,
                              [1., 0., 0., 0.,
                               0., 1., 0., 0.,
                               0., 0., 1., 0.])
    for prop in rn_props.properties:
        root_node.add_property(*prop.extract_data(prop))
    
    bone_list = {bone.name: i for i, bone in enumerate([root_node, *armature.data.bones])}
    # Export each bone as a node
    for bone in armature.data.bones:
        # Reconstruct the rest pose transform
        bone_parent = bone.parent
        bind_matrix = bone.matrix_local
        if bone_parent is None:
            parent_id = 0
            local_bind_matrix = convert_Zup_to_Yup(bind_matrix)
        else:
            parent_id = bone_list[bone_parent.name]
            local_bind_matrix = (convert_YDirBone_to_XDirBone(bone_parent.matrix_local)).inverted() @ bind_matrix
        
        bind_relative_pose = rest_pose_matrices[bone.name]
        parent_relative_pose = local_bind_matrix @ convert_YDirBone_to_XDirBone(bind_relative_pose)
        p, r, s = parent_relative_pose.decompose()
        position = [p.x, p.y, p.z]
        rotation = [r.x, r.y, r.z, r.w]
        scale    = [s.x, s.y, s.z]
        
        bm = BlenderBoneToMayaBone(bind_matrix)
        export_bm = [
            bm[0][0], bm[0][1], bm[0][2], bm[0][3],
            bm[1][0], bm[1][1], bm[1][2], bm[1][3],
            bm[2][0], bm[2][1], bm[2][2], bm[2][3],
        ]
        
        # Export the node object
        unknown_float = bone.GFSTOOLS_NodeProperties.unknown_float
        node = gfs.add_node(parent_id, bone.name, position, rotation, scale, unknown_float, export_bm)
        
        # Export the custom properties
        for prop in bone.GFSTOOLS_NodeProperties.properties:
            node.add_property(*prop.extract_data(prop))


#####################
# PRIVATE FUNCTIONS #
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
                res[bone_name] = {'rotation_quaternion': [1., 0., 0., 0.],
                                  'location':            [0., 0., 0.],
                                  'scale':               [1., 1., 1.],
                                  'rotation_euler':      [0., 0., 0.]}
            curve_type = get_fcurve_type(fcurve)
            array_index = fcurve.array_index

            # Get value of first keyframe point
            res[bone_name][curve_type][array_index] = fcurve.keyframe_points[0].co[1]
    return res


def extract_first_frame(action, pose_bones):
    out = {}
    extracted_fcurve_data = group_fcurves_by_bone_and_type(action)
    for pose_bone in pose_bones:
        pose_curves = extracted_fcurve_data.get(pose_bone.name)
        if pose_curves is None:
            out[pose_bone.name] = Matrix.Identity(4)
            continue

        rotation = convert_rotation_to_quaternion(pose_curves["rotation_quaternion"],
                                                  pose_curves["rotation_euler"],
                                                  pose_bone.rotation_mode)
        
        t_matrix = Matrix.Translation(pose_curves['location'])
        r_matrix = rotation.to_matrix().to_4x4()
        s_matrix = Matrix.Diagonal([*pose_curves['scale'], 1.])
        
        out[pose_bone.name] = t_matrix @ r_matrix @ s_matrix
    return out
