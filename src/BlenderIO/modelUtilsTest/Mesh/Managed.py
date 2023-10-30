import bpy


def define_managed_mesh(make_name, update_mesh, get_props=None, operator_id=None, calculate=None, calculate_id=None, get_parent=None):
    has_operator  = get_props is not None and operator_id is not None
    has_calculate = calculate is not None and calculate_id is not None
    
    if has_operator:
        class ShowHideOperator(bpy.types.Operator):
            bl_idname = operator_id
            bl_label = "Show"
            bl_options = {'REGISTER', 'UNDO'}
            
            def execute(self, context):
                props = get_props(context)
                if props.is_alive(): props.remove()
                else:                props.generate(context)
                return {'FINISHED'}

    if has_calculate:
        class CalculateOperator(bpy.types.Operator):
            bl_idname = calculate_id
            bl_label = "Calculate"
            bl_options = {'REGISTER', 'UNDO'}
            
            def execute(self, context):
                calculate(context)
                return {'FINISHED'}
        
    
    class ManagedMesh(bpy.types.PropertyGroup):
        ref: bpy.props.PointerProperty(type=bpy.types.Object)
    
        def draw_operator(self, layout):
            is_alive = self.is_alive()
            if has_operator:  layout.operator(ShowHideOperator.bl_idname, text="Hide" if is_alive else "Show")
            if has_calculate: layout.operator(CalculateOperator.bl_idname)
    
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
            if get_parent is None:
                active_obj = context.active_object
            else:
                active_obj = get_parent(context)
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
            if has_operator:  bpy.utils.register_class(ShowHideOperator)
            if has_calculate: bpy.utils.register_class(CalculateOperator)
            
        @classmethod
        def unregister(cls):
            if has_operator:  bpy.utils.unregister_class(ShowHideOperator)
            if has_calculate: bpy.utils.unregister_class(CalculateOperator)
    
    return ManagedMesh
