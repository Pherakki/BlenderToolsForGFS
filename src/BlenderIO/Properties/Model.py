import bpy
from .Nodes import make_node_props_class
from .Physics import GFSToolsPhysicsProperties
from ..modelUtilsTest.Mesh.Managed import define_managed_mesh
from ..Utils.BoundingVolumes import update_box
from ..Utils.BoundingVolumes import update_sphere
from .BoundingVolumes import define_bounding_box
from .BoundingVolumes import define_bounding_sphere
    

def get_box_props(context):
    return context.active_object.data.GFSTOOLS_ModelProperties.bounding_box.mesh


def get_sphere_props(context):
    return context.active_object.data.GFSTOOLS_ModelProperties.bounding_sphere.mesh


ModelBoundingBox    = define_managed_mesh(lambda arm: f".GFSTOOLS_{arm.name}Box",    lambda arm, ctx, obj: update_box   (arm.GFSTOOLS_ModelProperties.bounding_box,    ctx, obj), get_box_props,    "gfstools.showmodelboundingbox"   )
ModelBoundingSphere = define_managed_mesh(lambda arm: f".GFSTOOLS_{arm.name}Sphere", lambda arm, ctx, obj: update_sphere(arm.GFSTOOLS_ModelProperties.bounding_sphere, ctx, obj), get_sphere_props, "gfstools.showmodelboundingsphere")
ModelBoundingBoxProps    = define_bounding_box   (ModelBoundingBox)
ModelBoundingSphereProps = define_bounding_sphere(ModelBoundingSphere)

GFSToolsModelNodeProperties = make_node_props_class("GFSToolsModelNodeProperties")


class GFSToolsModelProperties(bpy.types.PropertyGroup):
    bounding_box:    bpy.props.PointerProperty(type=ModelBoundingBoxProps)
    bounding_sphere: bpy.props.PointerProperty(type=ModelBoundingSphereProps)

    # Remaining stuff
    flag_3:           bpy.props.BoolProperty(name="Unknown Flag 3", default=False) 
    root_node_name:   bpy.props.StringProperty(name="Root Node Name", default="RootNode")
    has_external_emt: bpy.props.BoolProperty(name="External EMT", default=False)    
    physics:          bpy.props.PointerProperty(name="Physics", type=GFSToolsPhysicsProperties)
    physics_blob:     bpy.props.StringProperty(name="SECRET PHYSICS BLOB - DO NOT TOUCH", default='', options={'HIDDEN'})
