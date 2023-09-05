from mathutils import Matrix, Vector


def freeze(transforms):
    transforms.vector.freeze()
    transforms.matrix4x4.freeze()
    transforms.matrix4x4_inv.freeze()
    
class TranslationTransforms:
    """
    A class containing multiple pre-computed representations of a translation.
    
    This class can currently only be initialised from a data structure 
    interpretable as a 4x4 matrix.
    """
    
    __slots__ = ("vector",
                 "matrix4x4", "matrix4x4_inv")
    
    def __init__(self, vector=None, matrix4x4=None):
        if vector is not None:
            self.set_from_vector(vector)
        elif matrix4x4 is not None:
            self.set_from_matrix4x4(matrix4x4)
        else:
            self.set_from_vector(Vector((0., 0., 0.)))
    
    def set_from_vector(self, vector):
        self.vector        = Vector(vector[:3])
        self.matrix4x4     = Matrix.Translation(self.vector)
        self.matrix4x4_inv = self.matrix4x4.inverted()
        freeze(self)
        
    
    def set_from_matrix4x4(self, matrix4x4):
        self.vector        = Matrix(matrix4x4).to_translation()
        self.matrix4x4     = Matrix.Translation(self.vector)
        self.matrix4x4_inv = self.matrix4x4.inverted()
        freeze(self)
        
