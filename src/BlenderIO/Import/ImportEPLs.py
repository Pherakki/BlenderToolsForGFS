import io

import bpy
from mathutils import Quaternion, Matrix

from ...FileFormats.GFS import GFSInterface, GFSBinary
from ...serialization.BinaryTargets import Writer
from ..Globals import GFS_MODEL_TRANSFORMS
from ..modelUtilsTest.Context.ActiveObject import safe_active_object_switch
from ..modelUtilsTest.Context.ActiveObject import set_active_obj
from ..modelUtilsTest.Context.ActiveObject import get_active_obj
from ..modelUtilsTest.Context.ActiveObject import set_mode
from . import ImportGFS
from .Utils.BoneConstruction import construct_bone, resize_bone_length


def import_epls(gfs, armature, gfs_to_bpy_bone_map, errorlog, import_policies):
    for epl in gfs.epls:
        import_child_epl(gfs, epl, armature, gfs_to_bpy_bone_map, errorlog, import_policies)

def import_child_epl(gfs, epl, armature, gfs_to_bpy_bone_map, errorlog, import_policies):
    if epl.node == 0:
        props = armature.data.GFSTOOLS_NodeProperties
    else:
        # Get bone
        bpy_bone_idx = gfs_to_bpy_bone_map[epl.node]
        bpy_bone     = armature.data.bones[bpy_bone_idx]
        props        = bpy_bone.GFSTOOLS_NodeProperties
        
    # Write the EPL to a blob
    stream = io.BytesIO()
    wtr = Writer(None)
    wtr.bytestream = stream
    wtr.rw_obj(epl.to_binary(), 0x01105100)
    stream.seek(0)
    
    # Add blob
    item = props.epls.add()
    item.blob = ''.join(f"{elem:0>2X}" for elem in stream.read())
    
    
    if import_policies.epl_tests:
        armature_name = gfs.bones[epl.node].name
        main_armature = import_epl(armature_name, epl, errorlog, import_policies)
        
        if epl.node == 0:
            main_armature.parent = armature
        else:
            constraint = main_armature.constraints.new("CHILD_OF")
            constraint.target    = armature
            bpy_bone_idx = gfs_to_bpy_bone_map[epl.node]
            bpy_bone     = armature.data.bones[bpy_bone_idx]
            constraint.subtarget = bpy_bone.name
            constraint.inverse_matrix = Matrix.Identity(4)


def import_epl(name, epl, errorlog, import_policies):
    main_armature = bpy.data.objects.new(name, bpy.data.armatures.new(name))
    bpy.context.collection.objects.link(main_armature)
    bpy.context.view_layer.objects.active = main_armature
    bpy_nodes, bone_transforms, epl_to_bpy_bone_map = build_armature(epl, main_armature)

    for leaf in epl.leaves:
        lb = leaf.binary
        if lb.type == 7: # Model
            payload = lb.payload
            if payload.has_embedded_file:
                file = payload.embedded_file
                
                model_name = file.name.string
                model_data = file.payload
                
                gb = GFSBinary()
                gb.unpack(model_data)
                gi = GFSInterface.from_binary(gb, duplicate_data=False)
                
                subobject = ImportGFS.import_gfs_object(gi, lb.name.string, errorlog, import_policies)

            
                if leaf.node == 0:
                    subobject.parent = main_armature
                else:
                    constraint = subobject.constraints.new("CHILD_OF")
                    constraint.target    = main_armature
                    bpy_bone_idx         = epl_to_bpy_bone_map[leaf.node]
                    bpy_bone             = main_armature.data.bones[bpy_bone_idx]
                    constraint.subtarget = bpy_bone.name
                    constraint.inverse_matrix = Matrix.Identity(4)
    return main_armature

def build_armature(epl, main_armature):
    matrix_w = GFS_MODEL_TRANSFORMS.world_axis_rotation.matrix4x4
    matrix_b = GFS_MODEL_TRANSFORMS.bone_axis_permutation.matrix4x4
    
    bones_to_ignore = {0}
    gfs_to_bpy_bone_map = {}
    bpy_bone_counter = 0
    
    bpy_nodes       = [None]*len(epl.nodes)
    true_transforms = [None]*len(epl.nodes)
    bone_transforms = [None]*len(epl.nodes)
    
    set_active_obj(main_armature)
    set_mode("EDIT")
    
    for i, node in enumerate(epl.nodes):
        t = node.position
        r = node.rotation
        
        local_bind_matrix = Matrix.Translation(t) @ Quaternion([r[3], r[0], r[1], r[2]]).to_matrix().to_4x4()
        if node.parent_idx > -1:
            bind_matrix = true_transforms[node.parent_idx] @ local_bind_matrix
        else:
            bind_matrix = local_bind_matrix
            
        true_transforms[i] = bind_matrix

        if i not in bones_to_ignore:      
            bpy_bone = construct_bone(node.name, main_armature, 
                                     matrix_w @ bind_matrix @ matrix_b,
                                     10)
            if node.parent_idx > -1:
                bpy_bone.parent = bpy_nodes[node.parent_idx] 
            bpy_nodes[i]           = bpy_bone
            gfs_to_bpy_bone_map[i] = bpy_bone_counter
            bpy_bone_counter      += 1

        bone_transforms[i] = matrix_w @ bind_matrix
    
    for bpy_bone in bpy_nodes[1:]:
        resize_bone_length(bpy_bone, [10, 10, 10], 0.01)
        
    set_mode("OBJECT")
    
    return bpy_nodes, bone_transforms, gfs_to_bpy_bone_map
