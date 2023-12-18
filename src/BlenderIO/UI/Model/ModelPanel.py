import bpy

from .AnimationsSubPanel import OBJECT_PT_GFSToolsAnimationDataPanel
from .PhysicsSubPanel import OBJECT_PT_GFSToolsPhysicsDataPanel
from ..Node import makeNodePropertiesPanel
from ...Globals import NAMESPACE


def _draw_on_node(context, layout):
    armature = context.armature
    layout = layout

    layout.prop(armature.GFSTOOLS_ModelProperties, "root_node_name")


class AutonameMeshUVs(bpy.types.Operator):
    bl_label = "Auto-Rename Mesh UVs"
    bl_idname = f"{NAMESPACE}.autonamemeshuvs"

    @classmethod
    def poll(cls, context):
        if context.active_object is None:
            return False
        return context.active_object.GFSTOOLS_ObjectProperties.is_model()

    def execute(self, context):
        context.active_object.GFSTOOLS_ObjectProperties.autoname_mesh_uvs()
        return {'FINISHED'}


class OBJECT_PT_GFSToolsModelDataPanel(bpy.types.Panel):
    bl_label = "GFS Model"
    bl_idname = "OBJECT_PT_GFSToolsModelDataPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.armature is not None

    def draw(self, context):
        armature = context.armature
        layout = self.layout
        aprops = armature.GFSTOOLS_ModelProperties

        ctr = layout.column()

        ctr.prop(aprops, 'version')
        ctr.prop(aprops, "has_external_emt")
        ctr.prop(aprops, "flag_3")

        ctr.operator(AutonameMeshUVs.bl_idname)

        aprops.bounding_box.draw(ctr)
        aprops.bounding_sphere.draw(ctr)

    @classmethod
    def register(cls):
        bpy.utils.register_class(AutonameMeshUVs)
        bpy.utils.register_class(cls.NodePropertiesPanel)
        bpy.utils.register_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        bpy.utils.register_class(OBJECT_PT_GFSToolsAnimationDataPanel)

    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(AutonameMeshUVs)
        bpy.utils.unregister_class(cls.NodePropertiesPanel)
        bpy.utils.unregister_class(OBJECT_PT_GFSToolsPhysicsDataPanel)
        bpy.utils.unregister_class(OBJECT_PT_GFSToolsAnimationDataPanel)

    NodePropertiesPanel = makeNodePropertiesPanel(
        "ArmatureNode",
        "PROPERTIES",
        "WINDOW",
        "data",
        lambda context: context.armature.GFSTOOLS_NodeProperties,
        lambda cls, context: context.armature is not None,
        parent_id="OBJECT_PT_GFSToolsModelDataPanel",
        predraw=_draw_on_node
    )
