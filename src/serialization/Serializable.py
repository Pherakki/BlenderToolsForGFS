from .parsers import GFSReader, GFSWriter, GFSValidator
from ...external.exbip.serializables.traits import ReadableTrait
from ...external.exbip.serializables.traits import WriteableTrait
from ...external.exbip.serializables.traits import ValidatableTrait

class GFSSerializable(ReadableTrait(GFSReader),
                      WriteableTrait(GFSWriter),
                      ValidatableTrait(GFSValidator)):
    pass
