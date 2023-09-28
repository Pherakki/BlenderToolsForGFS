import bpy 
# TODO: WOAH THIS IS ANCIENT, NEED TO CHANGE THIS!!!
from ...WarningSystem.Warning import ReportableError


VERTEX_LIMIT = 6192

class DisplayableVerticesError(ReportableError):
    __slots__ = ("mesh", "vertex_indices", "prev_obj")
    
    HAS_DISPLAYABLE_ERROR = True
    
    def __init__(self, msg, mesh, vertex_indices):
        super().__init__(msg)
        self.mesh = mesh
        self.vertex_indices = vertex_indices
        self.prev_obj = None
        
    def showErrorData(self):
        self.prev_obj = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = self.mesh
        bpy.ops.object.mode_set(mode="OBJECT")
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        
        for vidx in self.vertex_indices:
            self.mesh.data.vertices[vidx].select = True
        
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type="VERT")
        
    def hideErrorData(self):
        bpy.context.view_layer.objects.active = self.mesh
        bpy.ops.object.mode_set(mode="OBJECT")
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        if self.prev_obj is not None:
            bpy.context.view_layer.objects.active = self.prev_obj


class NonTriangularFacesError(ReportableError):
    __slots__ = ("mesh", "poly_indices", "prev_obj")
    
    HAS_DISPLAYABLE_ERROR = True
    
    def __init__(self, mesh, poly_indices):
        msg = f"Mesh '{mesh.name}' has {len(poly_indices)} non-triangular faces. Ensure that all faces are triangular before exporting."
        super().__init__(msg)
        self.mesh = mesh
        self.poly_indices = poly_indices
        self.prev_obj = None
        
    def showErrorData(self):
        self.prev_obj = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = self.mesh
        bpy.ops.object.mode_set(mode="OBJECT")
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        
        for pidx in self.poly_indices:
            self.mesh.data.polygons[pidx].select = True
        
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type="FACE")
        
    def hideErrorData(self):
        bpy.context.view_layer.objects.active = self.mesh
        bpy.ops.object.mode_set(mode="OBJECT")
        
        self.mesh.data.polygons.foreach_set("select", (False,) * len(self.mesh.data.polygons))
        self.mesh.data.edges   .foreach_set("select", (False,) * len(self.mesh.data.edges))
        self.mesh.data.vertices.foreach_set("select", (False,) * len(self.mesh.data.vertices))
        if self.prev_obj is not None:
            bpy.context.view_layer.objects.active = self.prev_obj
        

class DisplayableMeshesError(ReportableError):
    __slots__ = ("meshes",)
    
    HAS_DISPLAYABLE_ERROR = True
    
    def __init__(self, msg, meshes):
        super().__init__(msg)
        self.meshes = meshes
        
    def showErrorData(self):
        bpy.ops.object.select_all(action='DESELECT')
        for mesh in self.meshes:
            mesh.select_set(True)
        
    def hideErrorData(self):
        pass
        

class MissingVertexGroupsError(DisplayableVerticesError):
    def __init__(self, mesh, vertex_indices, bone_names):
        newline = '\n'
        msg = f"Mesh '{mesh.name}' has {len(vertex_indices)} vertices weighted to bones that do not exist. These vertices have been selected for you. If you wish to ignore this error, check the 'Strip Missing Vertex Groups' option when exporting. The missing bones are:{newline}{newline.join(bone_names)}"
        super().__init__(msg, mesh, vertex_indices)


class MissingUVMapsError(ReportableError):
    __slots__ = ("mesh", "mapname")
    
    def __init__(self, mesh, mapname):
        msg = f"Mesh '{mesh.name}' uses a material that requires UV map '{mapname}', but the mesh does not contain this map"
        super().__init__(msg)
        self.mesh = mesh
        self.mapname = mapname
        
    def showErrorData(self):
        bpy.ops.object.select_all(action='DESELECT')
        self.mesh.select_set(True)
        
    def hideErrorData(self):
        self.mesh.select_set(False)


class MultipleMaterialsError(DisplayableMeshesError):
    def __init__(self, meshes):
        msg = f"{len(meshes)} meshes have more than one material. A mesh must have a single material for successful export. You can split meshes by material by selecting all vertices in Edit Mode, pressing P, and clicking 'Split by Material' on the pop-up menu. You can ignore this error or auto-split meshes on export from the Export menu and in the Addon Preferences. The affected meshes have been selected for you"
        super().__init__(msg, meshes)



class PartiallyUnriggedMeshError(DisplayableVerticesError):
    def __init__(self, mesh, vertex_indices):
        msg = f"Mesh '{mesh.name}' has {len(vertex_indices)}/{len(mesh.data.vertices)} vertices that are unrigged. These vertices have been selected for you."
        super().__init__(msg, mesh, vertex_indices)


class TooManyIndicesError(DisplayableVerticesError):
    def __init__(self, mesh, vertex_indices):
        msg = f"Mesh '{mesh.name}' has {len(vertex_indices)} vertices that belong to more than 4 vertex groups. Ensure that all vertices belong to, at most, 4 groups before exporting. Alternatively, switch the export setting to 'Warn' to automatically strip the least influential groups."
        super().__init__(msg, mesh, vertex_indices)


class TooManyVerticesError(DisplayableMeshesError):
    vtx_limit = VERTEX_LIMIT
    
    def __init__(self, meshes):
        msg = f"{len(meshes)} meshes need to be split into more than {self.vtx_limit} vertices. These have been selected for you"
        super().__init__(msg, meshes)



