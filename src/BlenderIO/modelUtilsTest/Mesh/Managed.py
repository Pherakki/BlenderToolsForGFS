import bpy


def define_managed_mesh(make_name, update_mesh, get_props, operator_id):
    class ShowHideOperator(bpy.types.Operator):
        bl_idname = operator_id
        bl_label = "Show"
        bl_options = {'REGISTER', 'UNDO'}
        
        def execute(self, context):
            props = get_props(context)
            if props.is_alive(): props.remove()
            else:                props.generate(context)
            return {'FINISHED'}
    
    
    class ManagedMesh(bpy.types.PropertyGroup):
        ref: bpy.props.PointerProperty(type=bpy.types.Object)
    
        def draw_operator(self, layout):
            is_alive = self.is_alive()
            layout.operator(ShowHideOperator.bl_idname, text="Hide" if is_alive else "Show")
    
        def is_alive(self):
            if self.ref is None:
                return False
            else:
                try:
                    links = self.ref.users_collection
                    if not len(links):
                        return False
                except ReferenceError:
                    return False
                
                return True
        
        def generate(self, context):
            self.remove()
            
            # Generate object
            active_obj = context.active_object
            bpy_mesh = bpy.data.meshes.new(make_name(self.id_data))
            bpy_mesh_object = bpy.data.objects.new(bpy_mesh.name, bpy_mesh)
            active_obj.users_collection[0].objects.link(bpy_mesh_object)
            bpy_mesh_object.parent = active_obj
            self.ref = bpy_mesh_object
            
            # Generate geometry
            update_mesh(self.id_data, context, bpy_mesh_object)
            
            # Lock transforms            
            bpy_mesh_object.lock_location[0] = True
            bpy_mesh_object.lock_location[1] = True
            bpy_mesh_object.lock_location[2] = True
            
            bpy_mesh_object.lock_rotation[0] = True
            bpy_mesh_object.lock_rotation[1] = True
            bpy_mesh_object.lock_rotation[2] = True
            bpy_mesh_object.lock_rotation_w  = True
            
            bpy_mesh_object.lock_scale[0]    = True
            bpy_mesh_object.lock_scale[1]    = True
            bpy_mesh_object.lock_scale[2]    = True
        
        def remove(self):
            if self.ref is None:
                return
            else:
                try:
                    bpy.data.objects.remove(self.ref, do_unlink=True)
                except ReferenceError:
                    pass
                
                self.ref = None
                
        @staticmethod
        def update(props, context, self):
            bpy_mesh_object = self.ref
            if bpy_mesh_object is None:
                return
            
            try:
                bpy_mesh_object.lock_location[0] = False
                bpy_mesh_object.lock_location[1] = False
                bpy_mesh_object.lock_location[2] = False
                
                bpy_mesh_object.lock_rotation[0] = False
                bpy_mesh_object.lock_rotation[1] = False
                bpy_mesh_object.lock_rotation[2] = False
                bpy_mesh_object.lock_rotation_w  = False
                
                bpy_mesh_object.lock_scale[0]    = False
                bpy_mesh_object.lock_scale[1]    = False
                bpy_mesh_object.lock_scale[2]    = False
                
                bpy_mesh_object.data.clear_geometry()
                update_mesh(self.id_data, context, bpy_mesh_object)
                bpy_mesh_object.active_material = get_col_material()
            finally:
                bpy_mesh_object.lock_location[0] = True
                bpy_mesh_object.lock_location[1] = True
                bpy_mesh_object.lock_location[2] = True
                
                bpy_mesh_object.lock_rotation[0] = True
                bpy_mesh_object.lock_rotation[1] = True
                bpy_mesh_object.lock_rotation[2] = True
                bpy_mesh_object.lock_rotation_w  = True
                
                bpy_mesh_object.lock_scale[0]    = True
                bpy_mesh_object.lock_scale[1]    = True
                bpy_mesh_object.lock_scale[2]    = True
        
        @classmethod
        def register(cls):
            bpy.utils.register_class(ShowHideOperator)
            
        @classmethod
        def unregister(cls):
            bpy.utils.unregister_class(ShowHideOperator)
    
    
    return ManagedMesh
