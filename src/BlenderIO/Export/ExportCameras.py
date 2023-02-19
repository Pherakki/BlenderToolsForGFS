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
        
        node_idx = [b.name for b in gfs.bones].index(bpy_camera_object.parent_bone)
        props = bpy_camera_object.data.GFSTOOLS_CameraProperties
        
        if bpy_camera_object.data.lens_unit != "FOV":
            errorlog.log_error(ReportableError(f"Camera '{bpy_camera_object.name}' has a focal length not defined in FOV units. Cameras must currently be exported with FOV units."))
        
        cam_bone = armature.data.bones[bpy_camera_object.parent_bone]
        view_pos, view_rot, view_scl = ((armature.matrix_world @ cam_bone.matrix_local).inverted() @ bpy_camera_object.matrix_world).decompose()
        view_matrix = Matrix.Translation(view_pos) @ view_rot.to_matrix().to_4x4()
        
        
        parent_transform = Matrix.Translation([0., -cam_bone.length, 0.])
        parent_transform @= Quaternion([.5**.5, 0., 0., .5**.5]).to_matrix().to_4x4()
        view_matrix @= parent_transform.inverted()
        
        gfs.add_camera(node_idx, 
                       [elem for row in view_matrix for elem in row],
                       bpy_camera_object.data.clip_start,
                       bpy_camera_object.data.clip_end,
                       bpy_camera_object.data.lens,
                       props.aspect_ratio,
                       props.unknown_0x50)
        
