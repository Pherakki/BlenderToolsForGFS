from ..framework.parsers.WriterBase import WriterBase
from ..descriptors import STANDARD_DESCRIPTORS
from ..descriptors import STANDARD_ENDIAN_DESCRIPTORS


class Writer(WriterBase.extended_with(STANDARD_DESCRIPTORS, STANDARD_ENDIAN_DESCRIPTORS)):
    pass
