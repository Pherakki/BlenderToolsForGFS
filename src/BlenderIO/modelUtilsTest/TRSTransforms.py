from .TranslationTransforms import TranslationTransforms
from .RotationTransforms import RotationTransforms


class TRSTransforms:
    __slots__ = ("translation", "rotation")
    
    def __init__(self, translation_vector=None, translation_matrix4x4=None,
                 rotation_quat=None, rotation_matrix4x4=None):
        self.translation = TranslationTransforms(translation_vector, translation_matrix4x4)
        self.rotation    = RotationTransforms(rotation_matrix4x4, rotation_quat)
