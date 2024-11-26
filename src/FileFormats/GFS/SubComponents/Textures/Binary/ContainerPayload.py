from ...CommonStructures import SizedObjArray
from .TextureBinary import TextureBinary


class TexturePayload(SizedObjArray):
    TYPECODE = 0x000100FC

    def __init__(self):
        super().__init__(TextureBinary)
