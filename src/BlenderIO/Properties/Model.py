import numpy as np

import bpy
from mathutils import Vector

from ..Globals import GFS_MODEL_TRANSFORMS
from ..modelUtilsTest.Mesh.Managed import define_managed_mesh
from ..Utils.BoundingVolumes import update_box
from ..Utils.BoundingVolumes import update_sphere
from ..Utils.RestPose import get_rest_pose
from .BoundingVolumes import define_bounding_box
from .BoundingVolumes import define_bounding_sphere
from .Meshes import calculate_mesh_box
from .Nodes import make_node_props_class
from .Physics import GFSToolsPhysicsProperties
from .AnimationPack import GFSToolsAnimationPackProperties
from .MixIns.Version import GFSVersionedProperty
from ..Preferences import get_preferences


def get_box_props(context):
    return context.active_object.data.GFSTOOLS_ModelProperties.bounding_box.mesh


def build_pose_matrix(bone, bones, local_matrices):
    m = local_matrices[bone.name]
    if bone.parent is None:
        return m
    else:
        return build_pose_matrix(bone.parent, bones, local_matrices) @ m


def get_mesh_box_verts(bpy_armature_object):
    meshes = bpy_armature_object.GFSTOOLS_ObjectProperties.get_model_meshes()
    
    # Bounding boxes
    bbox_verts = []
    for m in meshes:
        mprops = m.data.GFSTOOLS_MeshProperties
        bbox = mprops.bounding_box
        if bbox.export_policy == "AUTO":
            bmin, bmax = calculate_mesh_box(m.data)
        elif bbox.export_policy == "MANUAL":
            bmin = bbox.min_dims
            bmax = bbox.max_dims
        elif bbox.export_policy == "NONE":
            continue
        else:
            raise NotImplementedError(f"CRITICAL INTERNAL ERROR: Unknown mesh bounding box calculation policy '{bbox.export_policy}'")
        
        bbox_verts.append((m.matrix_local @ Vector([*bmin, 1.]))[:3])
        bbox_verts.append((m.matrix_local @ Vector([*bmax, 1.]))[:3])
    return bbox_verts


def calculate_model_box(bpy_armature_object):
    rest_pose_matrices, armature_pose = get_rest_pose(bpy_armature_object)

    # Bounding boxes
    bbox_verts = get_mesh_box_verts(bpy_armature_object)

    # Deal with armature
    bone_matrices = {}
    for bone_name, dpm in rest_pose_matrices.items():
        bone = bpy_armature_object.data.bones[bone_name]
        bone_parent = bone.parent
        bind_matrix = bone.matrix_local
        if bone_parent is None:
            local_bind_matrix = bind_matrix
        else:
            local_bind_matrix = bone_parent.matrix_local.inverted() @ bind_matrix
        
        lrpm = local_bind_matrix @ dpm
        bone_matrices[bone.name] = lrpm
    
    bone_positions = []
    for bone_name in bone_matrices:
        bone = bpy_armature_object.data.bones[bone_name]
        rpm = build_pose_matrix(bone, bpy_armature_object.data.bones, bone_matrices)
        bone_positions.append([rpm[0][3], rpm[1][3], rpm[2][3]])
    
    # Calculate dimensions
    all_pos = [*bbox_verts, *bone_positions]
    
    return np.min(all_pos, axis=0), np.max(all_pos, axis=0)


def calculate_box(context):
    bpy_armature_object = context.active_object
    bpy_armature = bpy_armature_object.data
    bbox = bpy_armature.GFSTOOLS_ModelProperties.bounding_box
    bbox.min_dims, bbox.max_dims = calculate_model_box(bpy_armature_object)


def get_sphere_props(context):
    return context.active_object.data.GFSTOOLS_ModelProperties.bounding_sphere.mesh


def calculate_sphere(context):
    bpy_armature_object = context.active_object
    bbox_verts = get_mesh_box_verts(bpy_armature_object)
    sphere_centre = np.mean(bbox_verts, axis=0)
    
    props = bpy_armature_object.data.GFSTOOLS_ModelProperties
    boxprops = props.bounding_box
    if boxprops.export_policy == "MANUAL":
        bmin = np.array(boxprops.min_dims)
        bmax = np.array(boxprops.max_dims)
    else:
        bmin, bmax = calculate_model_box(bpy_armature_object)
        
    # Choose vertices in GFS-space, not Blender-space
    inv_xform = np.array(GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix3x3_inv.copy())
    tmpmin = inv_xform @ bmin
    tmpmax = inv_xform @ bmax
    bmin = np.min([tmpmin, tmpmax], axis=0)
    bmax = np.max([tmpmin, tmpmax], axis=0)
    tmp_centre = inv_xform @ sphere_centre
    radius = max([np.linalg.norm(np.array(v) - tmp_centre) for v in [bmin, bmax]])
    
    sphprops = props.bounding_sphere
    sphprops.center = sphere_centre
    sphprops.radius = radius


ModelBoundingBox    = define_managed_mesh(lambda arm: f".GFSTOOLS_{arm.name}Box",    lambda arm, ctx, obj: update_box   (arm.GFSTOOLS_ModelProperties.bounding_box,    ctx, obj), get_box_props,    "gfstools.showmodelboundingbox"   , calculate_box,    "gfstools.calcmodelboundingbox")
ModelBoundingSphere = define_managed_mesh(lambda arm: f".GFSTOOLS_{arm.name}Sphere", lambda arm, ctx, obj: update_sphere(arm.GFSTOOLS_ModelProperties.bounding_sphere, ctx, obj), get_sphere_props, "gfstools.showmodelboundingsphere", calculate_sphere, "gfstools.calcmodelboundingsphere")
ModelBoundingBoxProps    = define_bounding_box   (ModelBoundingBox)
ModelBoundingSphereProps = define_bounding_sphere(ModelBoundingSphere)

GFSToolsModelNodeProperties = make_node_props_class("GFSToolsModelNodeProperties")


class GFSToolsModelProperties(GFSVersionedProperty, bpy.types.PropertyGroup):
    bounding_box:    bpy.props.PointerProperty(type=ModelBoundingBoxProps)
    bounding_sphere: bpy.props.PointerProperty(type=ModelBoundingSphereProps)

    # Remaining stuff
    flag_3:           bpy.props.BoolProperty(name="Unknown Flag 3", default=False) 
    root_node_name:   bpy.props.StringProperty(name="Root Node Name", default="RootNode")
    has_external_emt: bpy.props.BoolProperty(name="External EMT", default=False)    
    physics:          bpy.props.PointerProperty(name="Physics", type=GFSToolsPhysicsProperties)
    physics_blob:     bpy.props.StringProperty(name="SECRET PHYSICS BLOB - DO NOT TOUCH", default='', options={'HIDDEN'})

    active_animation_pack_idx:   bpy.props.IntProperty(default=-1, options={'HIDDEN'})
    internal_animation_pack_idx: bpy.props.IntProperty(default=-1, options={'HIDDEN'})
    animation_pack_idx:          bpy.props.IntProperty(default= 0, options={'HIDDEN'})
    animation_packs:             bpy.props.CollectionProperty(type=GFSToolsAnimationPackProperties)
    
    ERROR_TEMPLATE = "CRITICAL INTERNAL ERROR: INVALID {msg} ANIMATION PACK INDEX '{idx}'"
    
    def get_gap(self, idx, msg="list index out of range"):
        if not len(self.animation_packs):
            return None
        elif idx == -1:
            return None
        elif idx < len(self.animation_packs):
            return self.animation_packs[idx]
        else:
            raise IndexError(msg)
    
    def _internal_get_gap(self, idx, msg):
        err_msg = self.ERROR_TEMPLATE.format(msg=msg, idx=idx)
        return self.get_gap(idx, err_msg)
    
    def get_active_gap(self):
        return self._internal_get_gap(self.active_animation_pack_idx, "ACTIVE")
    
    def get_internal_gap(self):
        return self._internal_get_gap(self.internal_animation_pack_idx, "INTERNAL")
    
    def get_selected_gap(self):
        return self._internal_get_gap(self.animation_pack_idx, "SELECTED")

    def is_selected_gap_active(self):
        if get_preferences().wip_animation_import and get_preferences().developer_mode:
            return self.get_selected_gap().is_active
        else:
            return self.animation_pack_idx == self.active_animation_pack_idx

    def is_internal_gap_active(self):
        return self.active_animation_pack_idx == self.internal_animation_pack_idx

    def is_internal_gap_selected(self):
        return self.animation_pack_idx == self.internal_animation_pack_idx

    def has_internal_gap(self):
        return self.internal_animation_pack_idx > -1

    def gaps_as_dict(self):
        out = {}
        for i, gap in enumerate(self.animation_packs):
            out[gap.name] = i
