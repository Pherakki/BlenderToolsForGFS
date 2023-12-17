import bpy

from ..modelUtilsTest.UI.Layout import indent


def define_bounding_box(bbox_type):
    class BoundingBox(bpy.types.PropertyGroup):
        export_policy: bpy.props.EnumProperty(items=[("NONE",   "None",   "Do not export a bounding box"),
                                                     ("MANUAL", "Manual", "Manually create bounding box"),
                                                     ("AUTO",   "Auto",   "Auto-calculate a bounding box on export")],
                                                     name="Bounding Box", default="AUTO")
        mesh: bpy.props.PointerProperty(type=bbox_type)
        min_dims:  bpy.props.FloatVectorProperty(name="Bounding Box Min", 
                                                 size=3,
                                                 default=(0, 0, 0),
                                                 update=lambda self, ctx: bbox_type.update(self, ctx, self.mesh))
        max_dims:  bpy.props.FloatVectorProperty(name="Bounding Box Max",
                                                 size=3, 
                                                 default=(0, 0, 0),
                                                 update=lambda self, ctx: bbox_type.update(self, ctx, self.mesh))
    
        def draw(self, layout):
            # Bounding box
            layout.prop(self, "export_policy")
            if self.export_policy == "MANUAL":
                col = indent(layout)
                
                row = col.row()
                row.prop(self, "min_dims")
                row = col.row()
                row.prop(self, "max_dims")
                self.mesh.draw_operator(col)

    return BoundingBox


def define_bounding_sphere(bsph_type):
    class BoundingSphere(bpy.types.PropertyGroup):
        export_policy: bpy.props.EnumProperty(items=[("NONE",   "None",   "Do not export a bounding sphere"),
                                                     ("MANUAL", "Manual", "Manually create bounding sphere"),
                                                     ("AUTO",   "Auto",   "Auto-calculate a bounding sphere on export")],
                                                     name="Bounding Sphere", default="AUTO")
        mesh:   bpy.props.PointerProperty(type=bsph_type)
        center: bpy.props.FloatVectorProperty(name="Bounding Sphere Center", 
                                              size=3,
                                              default=(0, 0, 0),
                                              update=lambda self, ctx: bsph_type.update(self, ctx, self.mesh))
        radius: bpy.props.FloatProperty(name="Bounding Sphere Radius",
                                        default=0,
                                        update=lambda self, ctx: bsph_type.update(self, ctx, self.mesh))
    
        def draw(self, layout):        
            layout.prop(self, "export_policy")
            if self.export_policy == "MANUAL":
                col = indent(layout)
                
                row = col.row()
                row.prop(self, "center")
                row = col.row()
                row.prop(self, "radius")
                self.mesh.draw_operator(col)
        
    return BoundingSphere
