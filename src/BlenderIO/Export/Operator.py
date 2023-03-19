import array

import bpy
from bpy_extras.io_utils import ExportHelper
import numpy as np

from ...FileFormats.GFS import GFSInterface
from ..Data import available_versions_property
from ..Preferences import get_preferences
from .ExportNodes import export_node_tree
from .ExportMeshData import export_mesh_data
from .ExportMaterials import export_materials_and_textures
from .ExportLights import export_lights
from .ExportCameras import export_cameras
from .ExportPhysics import export_physics
from .Export0x000100F8 import export_0x000100F8
from .ExportAnimations import export_animations
from .ExportEPLs import export_epls

from ..WarningSystem import ErrorLogger, handle_warning_system


class ExportGFS(bpy.types.Operator, ExportHelper):
    bl_idname = 'export_file.export_gfs'
    bl_label = 'Persona 5 Royal - PC (.GMD, .GFS)'
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext: bpy.props.EnumProperty(
        items=[
            ('.GMD', '.GMD', ''),
            ('.GFS', '.GFS', '')
        ],
        options={'HIDDEN'}
    )

    pack_animations: bpy.props.BoolProperty(
        name="Pack Animations into Model",
        default=False
    )

    filter_glob: bpy.props.StringProperty(
        default="*.GMD;*.GFS",
        options={'HIDDEN'},
    )
    
    debug_mode: bpy.props.BoolProperty(
        default=False,
        options={'HIDDEN'},
    )
    
    strip_missing_vertex_groups: bpy.props.BoolProperty(
        name="Strip Missing Vertex Groups",
        description="If a mesh has vertex groups with no corresponding bone, ignore those groups and renormalize the vertex weights with those groups removed",
        default=False
    )
    
    recalculate_tangents: bpy.props.BoolProperty(
        name="Recalculate Tangents",
        description="Recalculate tangents on export if they are required",
        default=True
    )
    
    version: available_versions_property()
    
    def invoke(self, context, event):
        prefs = get_preferences()
        self.strip_missing_vertex_groups = prefs.strip_missing_vertex_groups
        self.recalculate_tangents  = prefs.recalculate_tangents
        self.version = prefs.version
        return super().invoke(context, event)


    @handle_warning_system("The .blend file you are trying to export from, with all images packed into the file.")
    def export_file(self, context, filepath):
        # Init a logger
        errorlog = ErrorLogger()
        
        # Locate which model to expose based on what object the user has
        # selected.
        selected_model = find_selected_model(errorlog)
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'CANCELLED'}
        
        original_obj  = bpy.context.view_layer.objects.active
        original_mode = selected_model.mode
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.context.view_layer.objects.active = selected_model
        bpy.ops.object.mode_set(mode="OBJECT")
        
        # If there are any exceptions that get thrown in here, this is
        # probably not good.
        # Any exceptions that interrupt model export in this block should be
        # reported as bugs, and this should be communicated to the user.
        gfs = GFSInterface()
        export_node_tree(gfs, selected_model, errorlog)
        bpy_material_names, bpy_node_meshes = export_mesh_data(gfs, selected_model, errorlog, log_missing_weights=not self.strip_missing_vertex_groups, recalculate_tangents=self.recalculate_tangents)
        export_materials_and_textures(gfs, bpy_material_names, errorlog)
        export_lights(gfs, selected_model)
        export_cameras(gfs, selected_model, errorlog)
        export_physics(gfs, selected_model)
        export_0x000100F8(gfs, selected_model)
        export_epls(gfs, selected_model, bpy_node_meshes, errorlog)
        if self.pack_animations:
            export_animations(gfs, selected_model, keep_unused_anims=False)
        
        
        # Check if any errors occurred that prevented export.
        bpy.ops.object.mode_set(mode=original_mode)
        bpy.context.view_layer.objects.active = original_obj
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'CANCELLED'}
        
        gfs.has_end_container = True # Put this somewhere else
        gb = gfs.to_binary(int(self.version, 0x10))
        model_bin = gb.get_model_block()
        if model_bin is not None:
            if model_bin.data.skinning_data.bone_count is not None:
                if model_bin.data.skinning_data.bone_count > 256:
                    errorlog.log_error_message("More than 256 vertex groups are used across the model. A maximum of 256 are supported. Reduce the number of vertex groups to enable export.")
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'CANCELLED'}
        
        gb.write(filepath)
        
        # Tell the user if there are any warnings they should be aware of.
        if len(errorlog.warnings):
            errorlog.digest_warnings(self.debug_mode)
        elif not self.debug_mode:
            self.report({"INFO"}, "Export successful.")
        return {'FINISHED'}
    
    def execute(self, context):
        return self.export_file(context, self.filepath)


class ExportGAP(bpy.types.Operator, ExportHelper):
    bl_idname = 'export_file.export_gap'
    bl_label = 'Persona 5 Royal - PC (.GAP)'
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: bpy.props.StringProperty(
                                              default="*.GAP",
                                              options={'HIDDEN'},
                                          )
    
    debug_mode: bpy.props.BoolProperty(
                                           default=False,
                                           options={'HIDDEN'},
                                      )
    
    filename_ext = ".GAP"
    
    version: available_versions_property()
    
    def invoke(self, context, event):
        prefs = get_preferences()
        self.version = prefs.version
        return super().invoke(context, event)


    @handle_warning_system("The .blend file you are trying to export from, with all images packed into the file.")
    def export_file(self, context, filepath):
        # Init a logger
        errorlog = ErrorLogger()
        
        # Locate which model to expose based on what object the user has
        # selected.
        selected_model = find_selected_model(errorlog)
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'CANCELLED'}
        
        original_obj  = bpy.context.view_layer.objects.active
        original_mode = selected_model.mode
        bpy.context.view_layer.objects.active = selected_model
        bpy.ops.object.mode_set(mode="OBJECT")
        
        # If there are any exceptions that get thrown in here, this is
        # probably not good.
        # Any exceptions that interrupt model export in this block should be
        # reported as bugs, and this should be communicated to the user.
        gfs = GFSInterface()
        export_animations(gfs, selected_model, keep_unused_anims=True)
        
        # Check if any errors occurred that prevented export.
        bpy.ops.object.mode_set(mode=original_mode)
        bpy.context.view_layer.objects.active = original_obj
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'CANCELLED'}
        
        gfs.has_end_container = False # Put this somewhere else
        gb = gfs.to_binary(int(self.version, 0x10))
        gb.write(filepath)
        
        # Tell the user if there are any warnings they should be aware of.
        if len(errorlog.warnings):
            errorlog.digest_warnings(self.debug_mode)
            self.report({"INFO"}, "Export successful, with warnings.")
        elif not self.debug_mode:
            self.report({"INFO"}, "Export successful.")
        return {'FINISHED'}
    
    def execute(self, context):
        return self.export_file(context, self.filepath)
    

def find_selected_model(errorlog):
    try:
        parent_obj = bpy.context.selected_objects[0]
    except IndexError:
        errorlog.log_error_message("You must select some part of the model you wish to export in Object Mode before attempting to export it. No model is currently selected.")
        return

    sel_obj = None
    while parent_obj is not None:
        sel_obj = parent_obj
        parent_obj = sel_obj.parent
    parent_obj = sel_obj
    if parent_obj.type != "ARMATURE":
        errorlog.log_error_message(f"An object is selected, but the top-level object \'{parent_obj.name}\' is not an Armature object - has type {parent_obj.type}.")
    return parent_obj
