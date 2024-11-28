import array
import os

import bpy
from bpy_extras.io_utils import ExportHelper

from ...FileFormats.GFS import GFSInterface
from ..Data import version_override_options
from ..Data import too_many_vertices_policy_options
from ..Data import too_many_vertex_groups_policy_options
from ..Data import missing_uv_maps_policy_options
from ..Data import multiple_materials_policy_options
from ..Data import triangulate_mesh_policy_options
from ..Preferences import get_preferences
from ..Properties.MixIns.Version import GFSVersionedProperty
from ..modelUtilsTest.API.Operator import get_op_idname
from ..Globals import ErrorLogger
from .ExportNodes import export_node_tree
from .ExportModel.Mesh import export_mesh_data
from .ExportMaterials import export_materials_and_textures
from .ExportLights import export_lights
from .ExportCameras import export_cameras
from .ExportPhysics import export_physics
from .Export0x000100F8 import export_0x000100F8
from .ExportAnimations import export_gap_props
from .ExportEPLs import export_epls


class ExportPolicies(GFSVersionedProperty, bpy.types.PropertyGroup):
    combine_new_mesh_nodes: bpy.props.BoolProperty(
        name="Combine New Mesh Nodes",
        default=False
    )
    
    do_strip_epls: bpy.props.BoolProperty(
        name="Strip EPLs",
        description="Do not export EPL data from the hidden GFS properties of the models. If you don't know what that means, keep this option as false",
        default=False
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
    
    throw_missing_weight_errors: bpy.props.BoolProperty(
        name="Raise Error for Unrigged Vertices",
        description="If attempting to export a rigged mesh, throw an error if any vertices do not have vertex weights instead of throwing a warning",
        default=False
    )
    
    too_many_vertices_policy: bpy.props.EnumProperty(
        items=too_many_vertices_policy_options(),
        name=">6192 Vertices per Mesh",
        description="Decide the export behavior in the event of a mesh being split into more than 6192 vertices for export",
        default="WARN"
    )
    
    too_many_vertex_groups_policy: bpy.props.EnumProperty(
        items=too_many_vertex_groups_policy_options(),
        name="Vertex Group Limits",
        description="Decide the export behavior in the event of a mesh having vertices belonging to more than 4 vertex groups",
        default="ERROR"
    )
    
    multiple_materials_policy: bpy.props.EnumProperty(
        items=multiple_materials_policy_options(),
        name="Multiple Materials per Mesh",
        description="Decide the export behavior in the event of a mesh containing more than a single material",
        default="WARN"
    )
    
    missing_uv_maps_policy: bpy.props.EnumProperty(
        items=missing_uv_maps_policy_options(),
        name="Missing UV Maps",
        description="Decide the export behavior in the event of a mesh not having a UV map required by the material",
        default="WARN"
    )
    
    triangulate_mesh_policy: bpy.props.EnumProperty(
        items=triangulate_mesh_policy_options(),
        name="Triangulate Meshes",
        description="Decide the export behavior in the event of a mesh having any non-triangular faces",
        default="ERROR"
    )
    
    version_override: bpy.props.EnumProperty(
        items=version_override_options(),
        name="Export Version",
        description="Method used to determine the version number of the exported data",
        default="DEFAULT"
    )
    
    def get_version(self, default_version):
        if self.version_override == "DEFAULT":
            return default_version
        elif self.version_override == "P5R":
            return 0x01105100
        elif self.version_override == "CUSTOM":
            return self.int_version
        else:
            raise NotImplementedError(f"CRITICAL INTERNAL ERROR: Unknown VERSION_OVERRIDE policy '{self.version_override}'")


class ExportGFS(bpy.types.Operator, ExportHelper):
    bl_idname = 'export_file.export_gfs'
    bl_label = 'Persona 5 Royal - PC (.GMD, .GFS)'
    bl_options = {'REGISTER', 'UNDO'}
    internal_idname = ''
    
    debug_mode: bpy.props.BoolProperty(
        default=False,
        options={'HIDDEN'},
    )
    
    filename_ext: bpy.props.EnumProperty(
        items=[
            ('.GMD', '.GMD', ''),
            ('.GFS', '.GFS', '')
        ],
        options={'HIDDEN'}
    )

    filter_glob: bpy.props.StringProperty(
        default="*.GMD;*.GFS",
        options={'HIDDEN'},
    )
    
    
    policies: bpy.props.PointerProperty(type=ExportPolicies)
    
    def invoke(self, context, event):
        prefs = get_preferences()
        
        # Get from preferences
        self.policies.combine_new_mesh_nodes        = prefs.combine_new_mesh_nodes
        self.policies.strip_missing_vertex_groups   = prefs.strip_missing_vertex_groups
        self.policies.recalculate_tangents          = prefs.recalculate_tangents
        self.policies.throw_missing_weight_errors   = prefs.throw_missing_weight_errors
        self.policies.too_many_vertices_policy      = prefs.too_many_vertices_policy
        self.policies.too_many_vertex_groups_policy = prefs.too_many_vertex_groups_policy
        self.policies.multiple_materials_policy     = prefs.multiple_materials_policy
        self.policies.missing_uv_maps_policy        = prefs.missing_uv_maps_policy
        self.policies.triangulate_mesh_policy       = prefs.triangulate_mesh_policy
        
        return super().invoke(context, event)


    @ErrorLogger.display_exceptions("The .blend file you are trying to export from, with all images packed into the file.")
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
        mprops = selected_model.data.GFSTOOLS_ModelProperties
        gfs = GFSInterface()
        gfs.version = self.policies.get_version(selected_model.data.GFSTOOLS_ModelProperties.int_version)
        
        bpy_to_gfs_nodes, full_rest_pose_matrices = export_node_tree(gfs, selected_model, errorlog)
        bpy_material_names = export_mesh_data(gfs, selected_model, bpy_to_gfs_nodes, full_rest_pose_matrices, errorlog, self.policies)
        texbin = export_materials_and_textures(gfs, bpy_material_names, mprops.texture_mode, mprops.unused_textures, errorlog)
        export_lights(gfs, selected_model)
        export_cameras(gfs, selected_model, errorlog)
        export_physics(gfs, selected_model, errorlog)
        export_0x000100F8(gfs, selected_model)
        export_epls(gfs, selected_model, errorlog, self.policies)
        
        internal_pack = mprops.get_internal_gap()
        if internal_pack is not None:
            export_gap_props(gfs, selected_model, internal_pack, keep_unused_anims=False, errorlog=errorlog)
        
        
        # Check if any errors occurred that prevented export.
        bpy.ops.object.mode_set(mode=original_mode)
        bpy.context.view_layer.objects.active = original_obj
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'CANCELLED'}
        
        gfs.has_end_container = True # Put this somewhere else
        gb = gfs.to_binary()
        model_bin = gb.get_model_block()
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'CANCELLED'}
        
        gb.write(filepath, endianness="<" if gfs.version > 0x02000000 else ">")
        if texbin is not None:
            tex_fp = os.path.splitext(filepath)[0] + os.path.extsep + "TEX"
            texbin.write(tex_fp)
        
        # Tell the user if there are any warnings they should be aware of.
        if len(errorlog.warnings):
            errorlog.digest_warnings(self.debug_mode)
            self.report({"INFO"}, "Export successful, with warnings.")
        elif not self.debug_mode:
            self.report({"INFO"}, "Export successful.")
        return {'FINISHED'}
    
    def execute(self, context):
        return self.export_file(context, self.filepath)
    
    def draw(self, context):
        pass

    @classmethod
    def register(cls):
        cls.internal_idname = get_op_idname(cls)
        
        bpy.utils.register_class(CUSTOM_PT_GFSModelExportSettings)
        bpy.utils.register_class(CUSTOM_PT_GFSMeshExportSettings)
        
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(CUSTOM_PT_GFSModelExportSettings)
        bpy.utils.unregister_class(CUSTOM_PT_GFSMeshExportSettings)


class CUSTOM_PT_GFSModelExportSettings(bpy.types.Panel):
    """
    Adapted from https://blender.stackexchange.com/a/217796
    """
    
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Model Settings"
    bl_options = set()

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == ExportGFS.internal_idname

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator
        policies = operator.policies

        layout.prop(policies, 'version_override')
        if policies.version_override == "CUSTOM":
            layout.prop(policies, "version")
        layout.prop(policies, 'combine_new_mesh_nodes')
        layout.prop(policies, 'do_strip_epls')

class CUSTOM_PT_GFSMeshExportSettings(bpy.types.Panel):
    """
    Adapted from https://blender.stackexchange.com/a/217796
    """
    
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Mesh Settings"
    bl_options = set()

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == ExportGFS.internal_idname

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator
        policies = operator.policies

        layout.prop(policies, 'strip_missing_vertex_groups')
        layout.prop(policies, 'recalculate_tangents')
        layout.prop(policies, 'throw_missing_weight_errors')
        layout.prop(policies, 'too_many_vertices_policy')
        layout.prop(policies, 'too_many_vertex_groups_policy')
        layout.prop(policies, 'multiple_materials_policy')
        layout.prop(policies, 'missing_uv_maps_policy')
        layout.prop(policies, 'triangulate_mesh_policy')


def get_exportable_gaps(self, context):
    errorlog = ErrorLogger()
    selected_model = find_selected_model(errorlog)
    if len(errorlog.errors):
        errorlog.digest_errors(self.debug_mode)
        return {'CANCELLED'}

    mprops = selected_model.data.GFSTOOLS_ModelProperties
    return [(str(i), gap.name, "") for i, gap in enumerate(mprops.animation_packs)]


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
    
    policies: bpy.props.PointerProperty(type=ExportPolicies)
    available_gaps: bpy.props.EnumProperty(items=get_exportable_gaps, name="GAP")

    def invoke(self, context, event):
        prefs = get_preferences()
        return super().invoke(context, event)

    @ErrorLogger.display_exceptions("The .blend file you are trying to export from, with all images packed into the file.")
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

        prefs = get_preferences()
        mprops = selected_model.data.GFSTOOLS_ModelProperties
        active_pack = mprops.animation_packs[int(self.available_gaps)]
        export_gap_props(gfs, selected_model, active_pack, keep_unused_anims=True, errorlog=errorlog)

        # Check if any errors occurred that prevented export.
        bpy.ops.object.mode_set(mode=original_mode)
        bpy.context.view_layer.objects.active = original_obj
        if len(errorlog.errors):
            errorlog.digest_errors(self.debug_mode)
            return {'CANCELLED'}
        
        # Need to serialise the mesh data in order to calculate the anim
        # bounding boxes
        gfs_bbox = GFSInterface()
        export_node_tree(gfs_bbox, selected_model, None)
        
        gfs.version           = self.policies.get_version(active_pack.int_version)
        gfs.has_end_container = False # Put this somewhere else
        gb = gfs.to_binary(anim_model_binary=gfs_bbox.to_binary(active_pack.int_version).get_model_block().data)
        gb.write(filepath, endianness="<" if gfs.version > 0x02000000 else ">")
        
        # Tell the user if there are any warnings they should be aware of.
        if len(errorlog.warnings):
            errorlog.digest_warnings(self.debug_mode)
            self.report({"INFO"}, "Export successful, with warnings.")
        elif not self.debug_mode:
            self.report({"INFO"}, "Export successful.")
        return {'FINISHED'}
    
    def execute(self, context):
        return self.export_file(context, self.filepath)
    
    def draw(self, context):
        pass
    
    @classmethod
    def register(cls):
        cls.internal_idname = get_op_idname(cls)
        bpy.utils.register_class(CUSTOM_PT_GFSAnimExportSettings)
        
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(CUSTOM_PT_GFSAnimExportSettings)
    

class CUSTOM_PT_GFSAnimExportSettings(bpy.types.Panel):
    """
    Adapted from https://blender.stackexchange.com/a/217796
    """
    
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Anim Settings"
    bl_options = set()

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == ExportGAP.internal_idname

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator
        policies = operator.policies

        layout.prop(policies, 'version_override')
        if policies.version_override == "CUSTOM":
            layout.prop(policies, "version")

        layout.prop(operator, "available_gaps")


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
