from mathutils import Matrix
from .Maths import convert_rotation_to_quaternion


def get_rest_pose(bpy_armature_object):
    rest_pose_action = None
    if bpy_armature_object.animation_data is not None:
        rest_pose_nla = bpy_armature_object.animation_data.nla_tracks.get("Rest Pose", None)
        if rest_pose_nla is not None:
            if len(rest_pose_nla.strips):
                rest_pose_action = rest_pose_nla.strips[0].action
    if rest_pose_action is None:
        rest_pose_matrices = rest_pose_from_armature_bind_pose(bpy_armature_object.data.bones)
        armature_rest_pose = Matrix.Identity(4)
    else:
        rest_pose_matrices, armature_rest_pose = extract_first_frame(rest_pose_action, bpy_armature_object, bpy_armature_object.pose.bones)
        if armature_rest_pose is None:
            armature_rest_pose = Matrix.Identity(4)
    return rest_pose_matrices, armature_rest_pose


def get_bone_name_from_fcurve(fcurve):
    return fcurve.data_path.split('[')[1].split(']')[0][1:-1]


def get_fcurve_type(fcurve):
    return fcurve.data_path.split('.')[-1]

def create_anim_init_data():
    return {'rotation_quaternion': [1., 0., 0., 0.],
            'location':            [0., 0., 0.],
            'scale':               [1., 1., 1.],
            'rotation_euler':      [0., 0., 0.]}

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
        # Get value of first keyframe point
        edit_transforms[curve_type][array_index] = fcurve.keyframe_points[0].co[1]
        
    return res, obj_transforms


def local_bind_pose(bpy_bone):
    if bpy_bone.parent is None:
        parent_matrix = Matrix.Identity(4)
    else:
        parent_matrix = bpy_bone.parent.matrix_local
    return parent_matrix.inverted() @ bpy_bone.matrix_local


def rest_pose_from_armature_bind_pose(armature):
    out = {}
    for bpy_bone in armature.data.bones:
        out[bpy_bone.name] = Matrix.Identity(4) # local_bind_pose(bpy_bone)
    return out


def create_pose_matrix(pose_curves, pose_object):
    rotation = convert_rotation_to_quaternion(pose_curves["rotation_quaternion"],
                                              pose_curves["rotation_euler"],
                                              pose_object.rotation_mode)
    
    t_matrix = Matrix.Translation(pose_curves['location'])
    r_matrix = rotation.normalized().to_matrix().to_4x4()
    s_matrix = Matrix.Diagonal([*pose_curves['scale'], 1.])
    
    return  t_matrix @ r_matrix @ s_matrix


def extract_first_frame(action, armature_object, pose_bones):
    out = {}
    extracted_fcurve_data, extracted_root_fcurve_data = group_fcurves_by_bone_and_type(action)
    for pose_bone in pose_bones:
        pose_curves = extracted_fcurve_data.get(pose_bone.name)
        if pose_curves is None:
            out[pose_bone.name] = Matrix.Identity(4)
            continue

        out[pose_bone.name] = create_pose_matrix(pose_curves, pose_bone)
        
    root_pose = None if extracted_root_fcurve_data is None else create_pose_matrix(extracted_root_fcurve_data, armature_object)
        
    return out, root_pose