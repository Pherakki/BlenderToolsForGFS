import array

from mathutils import Vector

from ...API.Version import bpy_at_least


if bpy_at_least(4, 1, 0):
    def create_loop_normals(bpy_mesh, normals):
        bpy_mesh.polygons.foreach_set("use_smooth", [True] * len(bpy_mesh.polygons))
        bpy_mesh.normals_split_custom_set([Vector(n) for n in normals])

        bpy_mesh.validate(clean_customdata=False)
        bpy_mesh.update()
else:
    def create_loop_normals(bpy_mesh, normals):
        """
        Loads per-loop normal vectors into a mesh.
        
        Works thanks to this stackexchange answer https://blender.stackexchange.com/a/75957,
        which a few of these comments below are also taken from.
        """
        bpy_mesh.create_normals_split()
        for face in bpy_mesh.polygons:
            face.use_smooth = True  # loop normals have effect only if smooth shading ?
    
        # Set loop normals
        loop_normals = [Vector([normal[0], normal[1], normal[2]]) for normal in normals]
        bpy_mesh.loops.foreach_set("normal", [subitem for item in loop_normals for subitem in item])
    
        bpy_mesh.validate(clean_customdata=False)  # important to not remove loop normals here!
        bpy_mesh.update()
    
        clnors = array.array('f', [0.0] * (len(bpy_mesh.loops) * 3))
        bpy_mesh.loops.foreach_get("normal", clnors)
    
        bpy_mesh.polygons.foreach_set("use_smooth", [True] * len(bpy_mesh.polygons))
        # This line is pretty smart (came from the stackoverflow answer)
        # 1. Creates three copies of the same iterator over clnors
        # 2. Splats those three copies into a zip
        # 3. Each iteration of the zip now calls the iterator three times, meaning that three consecutive elements
        #    are popped off
        # 4. Turn that triplet into a tuple
        # In this way, a flat list is iterated over in triplets without wasting memory by copying the whole list
        bpy_mesh.normals_split_custom_set(tuple(zip(*(iter(clnors),) * 3)))
    
        bpy_mesh.use_auto_smooth = True


def create_uv_map(bpy_mesh, name, uvs):
    uv_layer = bpy_mesh.uv_layers.new(name=name, do_init=True)
    for loop_idx, (loop, (u, v)) in enumerate(zip(bpy_mesh.loops, uvs)):
        uv_layer.data[loop_idx].uv = (u, v)



if bpy_at_least(3, 2, 0):
    def create_color_map(bpy_mesh, name, color_data, datatype):
        if datatype == "FLOAT":
            ca = bpy_mesh.color_attributes.new(name=name, type="FLOAT_COLOR", domain="CORNER")
            for loop_idx, loop in enumerate(bpy_mesh.loops):
                ca.data[loop_idx].color = color_data[loop_idx]
        elif datatype == "BYTE":
            ca = bpy_mesh.color_attributes.new(name=name, type="BYTE_COLOR", domain="CORNER")
            for loop_idx, loop in enumerate(bpy_mesh.loops):
                ca.data[loop_idx].color = [c/255 for c in color_data[loop_idx]]
        else:
            raise ValueError(f"Invalid datatype '{datatype}': allowed values are 'FLOAT' and 'BYTE'")
else:
    def create_color_map(bpy_mesh, name, color_data, datatype):
        vc = bpy_mesh.vertex_colors.new(name=name)
        if datatype == "FLOAT":
            for loop_idx, loop in enumerate(bpy_mesh.loops):
                vc.data[loop_idx].color = color_data[loop_idx]
        elif datatype == "BYTE":
            for loop_idx, loop in enumerate(bpy_mesh.loops):
                vc.data[loop_idx].color = [c/255 for c in color_data[loop_idx]]
        else:
            raise ValueError(f"Invalid datatype '{datatype}': allowed values are 'FLOAT' and 'BYTE'")
            
