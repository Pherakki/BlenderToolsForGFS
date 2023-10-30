import bpy


class GFSToolsClipboard(bpy.types.PropertyGroup):
    bounding_box_min_dims:  bpy.props.FloatVectorProperty(name="Bounding Box Min Dims", size=3, default=(0., 0., 0.))
    bounding_box_max_dims:  bpy.props.FloatVectorProperty(name="Bounding Box Max Dims", size=3, default=(0., 0., 0.))
    bounding_sphere_center: bpy.props.FloatVectorProperty(name="Bounding Sphere Center", size=3, default=(0., 0., 0.))
    bounding_sphere_radius: bpy.props.FloatProperty(name="Bounding Sphere Radius", default=0.)
    