import math

import bpy
from mathutils import Matrix, Quaternion

from ..Utils.Maths import convert_rotation_to_quaternion
from ..WarningSystem.Warning import ReportableError


def export_cameras(gfs, armature, errorlog):
    bpy_cams = [obj for obj in armature.children if obj.type == "CAMERA"]
    
    for bpy_camera_object in bpy_cams:
        if bpy_camera_object.parent_type != "BONE":
            continue
        
        node_idx = armature.data.bones.index(bpy_camera_object.parent_bone.name)
        props = bpy_camera_object.data.GFSTOOLS_CameraProperties
        
        if bpy_camera_object.lens_unit != "FOV":
            errorlog.log_error(ReportableError(f"Camera '{bpy_camera_object.name}' has a focal length not defined in FOV units. Cameras must currently be exported with FOV units."))
        
        view_pos, view_rot, view_scl = bpy_camera_object.matrix_basis.decompose()
        view_matrix = Matrix.Translation(view_pos) @ view_rot.to_matrix().to_4x4()
        gfs.add_camera(node_idx, 
                       [elem for row in view_matrix for elem in row],
                       bpy_camera_object.clip_start,
                       bpy_camera_object.clip_end,
                       bpy_camera_object.lens,
                       props.aspect_ratio,
                       props.unknown_0x50)
        
