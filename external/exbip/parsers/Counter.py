from ..framework.parsers.CounterBase import CounterBase
from ..descriptors import STANDARD_DESCRIPTORS
from ..descriptors import STANDARD_ENDIAN_DESCRIPTORS


class Counter(CounterBase.extended_with(STANDARD_DESCRIPTORS, STANDARD_ENDIAN_DESCRIPTORS)):
    pass
