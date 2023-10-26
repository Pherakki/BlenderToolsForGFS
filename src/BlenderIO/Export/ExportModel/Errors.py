import bpy 
from ...modelUtilsTest.Misc.Errorlog.Warnings import ReportableError
from ...modelUtilsTest.Misc.Errorlog.Warnings import DisplayableVerticesError
from ...modelUtilsTest.Misc.Errorlog.Warnings import DisplayablePolygonsError
from ...modelUtilsTest.Misc.Errorlog.Warnings import DisplayableMeshesError

VERTEX_LIMIT = 6192


class NonTriangularFacesError(DisplayablePolygonsError):
    def __init__(self, bpy_mesh_object, poly_indices):
        msg = f"Mesh '{bpy_mesh_object.name}' has {len(poly_indices)} non-triangular faces. Ensure that all faces are triangular before exporting."
        super().__init__(msg, bpy_mesh_object, poly_indices)


class MissingVertexGroupsError(DisplayableVerticesError):
    def __init__(self, bpy_mesh_object, vertex_indices, bone_names):
        newline = '\n'
        msg = f"Mesh '{bpy_mesh_object.name}' has {len(vertex_indices)} vertices weighted to bones that do not exist. These vertices have been selected for you. If you wish to ignore this error, check the 'Strip Missing Vertex Groups' option when exporting. The missing bones are:{newline}{newline.join(bone_names)}"
        super().__init__(msg, bpy_mesh_object, vertex_indices)


class MissingUVMapsError(ReportableError):
    __slots__ = ("bpy_mesh_object", "mapname")
    
    def __init__(self, bpy_mesh_object, mapname):
        msg = f"Mesh '{bpy_mesh_object.name}' uses a material that requires UV map '{mapname}', but the mesh does not contain this map."
        super().__init__(msg)
        self.bpy_mesh_object = bpy_mesh_object
        self.mapname = mapname
        
    def showErrorData(self):
        bpy.ops.object.select_all(action='DESELECT')
        self.bpy_mesh_object.select_set(True)
        
    def hideErrorData(self):
        self.bpy_mesh_object.select_set(False)


class MissingMaterialError(DisplayableMeshesError):
    def __init__(self, bpy_mesh_objects):
        msg = f"{len(bpy_mesh_objects)} meshes have no material. A mesh must have a single material for successful export. The affected meshes have been selected for you."
        super().__init__(msg, bpy_mesh_objects)


class MultipleMaterialsError(DisplayableMeshesError):
    def __init__(self, bpy_mesh_objects):
        msg = f"{len(bpy_mesh_objects)} meshes have more than one material. A mesh must have a single material for successful export. You can split meshes by material by selecting all vertices in Edit Mode, pressing P, and clicking 'Split by Material' on the pop-up menu. You can ignore this error or auto-split meshes on export from the Export menu and in the Addon Preferences. The affected meshes have been selected for you."
        super().__init__(msg, bpy_mesh_objects)


class PartiallyUnriggedMeshError(DisplayableVerticesError):
    def __init__(self, bpy_mesh_object, vertex_indices):
        msg = f"Mesh '{bpy_mesh_object.name}' has {len(vertex_indices)}/{len(bpy_mesh_object.data.vertices)} vertices that are unrigged. These vertices have been selected for you."
        super().__init__(msg, bpy_mesh_object, vertex_indices)


class TooManyIndicesError(DisplayableVerticesError):
    def __init__(self, bpy_mesh_object, vertex_indices):
        msg = f"Mesh '{bpy_mesh_object.name}' has {len(vertex_indices)} vertices that belong to more than 4 vertex groups. Ensure that all vertices belong to, at most, 4 groups before exporting. Alternatively, switch the export setting to 'Warn' to automatically strip the least influential groups."
        super().__init__(msg, bpy_mesh_object, vertex_indices)


class TooManyVerticesError(DisplayableMeshesError):
    vtx_limit = VERTEX_LIMIT
    
    def __init__(self, bpy_mesh_objects):
        msg = f"{len(bpy_mesh_objects)} meshes need to be split into more than {self.vtx_limit} vertices. These have been selected for you."
        super().__init__(msg, bpy_mesh_objects)
