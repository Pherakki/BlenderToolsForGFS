from ....API.Version import bpy_at_least
from .Utils import empty_attr


# Public
def get_color_maps(bpy_mesh):
    if bpy_at_least(3, 2, 0):
        return bpy_mesh.color_attributes
    else:
        return bpy_mesh.vertex_colors


def get_colors(bpy_mesh_obj, use_colors, map_name, data_format, errorlog=None, transform=None, error_context=''):
    if len(error_context):
        error_context = f"{error_context}: "
    
    bpy_mesh = bpy_mesh_obj.data
    
    loops  = bpy_mesh.loops
    nloops = len(loops)
    if data_format not in ("BYTE", "FLOAT"):
        raise NotImplementedError("Invalid data format provided to 'get_colors'. Options are 'BYTE' or 'FLOAT'.")
    if use_colors:
        ################
        # EXTRACT DATA #
        ################
        color_maps = get_color_maps(bpy_mesh)
        
        # Blender 3.2+ 
        # vertex_colors is equivalent to color_attributes.new(name=name, type="BYTE_COLOR", domain="CORNER").
        if bpy_at_least(3, 2, 0):
            if map_name not in color_maps:
                data = warn_and_return_blank_color(bpy_mesh, map_name, nloops, errorlog, error_context)
            else:
                ca = color_maps[map_name]
                
                if ca.domain == "CORNER":
                    data = (c.color for c in ca.data)
                elif ca.domain == "POINT":
                    # Copy vertex data to loop data
                    data = (ca.data[loop.vertex_index].color for loop in bpy_mesh.loops)
                else:
                    if errorlog is not None:
                        errorlog.log_warning_message(f"{error_context}Unable to extract data from unknown color map domain '{ca.domain}' on '{map_name}'; exporting a fallback (1.0, 1.0, 1.0, 1.0) map.")
                    data = make_blank_color(nloops)
        # Blender 2.81-3.2
        else:
            if map_name not in color_maps:
                data = warn_and_return_blank_color(bpy_mesh, map_name, nloops, errorlog, error_context)
            else:
                vc = color_maps[map_name]
                data = (l.color for l in vc.data)
                
        #############################################
        # Convert to the requested output data type #
        #############################################
        # the .color member will always return a float value
        if data_format == "FLOAT":
            if transform is None: return [tuple(d) for d in data]
            else:                 return [tuple(transform(d, l)) for d, l in zip(data, loops)]
        elif data_format == "BYTE":
            if transform is None: return [          tuple([int(min(255, max(0, round(e*255)))) for e in d])     for d    in data            ]
            else:                 return [tuple(transform([int(min(255, max(0, round(e*255)))) for e in d], l)) for d, l in zip(data, loops)]
        else:
            raise NotImplementedError("Unhandled output data type '{data_format}'")
        
    else:
        return empty_attr(nloops)


# Utils
def make_blank_color(count):
    elem = tuple([1.0, 1.0, 1.0, 1.0])
    return [elem for _ in range(count)]


def warn_and_return_blank_color(bpy_mesh_obj, map_name, nloops, errorlog=None, error_context=''):
    if errorlog is not None:
        errorlog.log_warning_message(f"{error_context}Unable to locate color map '{map_name}' on mesh '{bpy_mesh_obj.name}'; exporting a fallback (1.0, 1.0, 1.0, 1.0) map")
    return make_blank_color(nloops) 
