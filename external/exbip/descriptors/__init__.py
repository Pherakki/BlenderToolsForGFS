from .Array           import PRIMITIVE_ARRAY_DESCRIPTORS
from .Array           import PRIMITIVE_ENDIAN_ARRAY_DESCRIPTORS
from .Descriptor      import DescriptorDescriptor
from .Object          import ObjectDescriptor
from .Object          import DynamicObjectDescriptor
from .Object          import DynamicObjectsDescriptor
from .Primitive       import PRIMITIVE_DESCRIPTORS
from .Primitive       import PRIMITIVE_ENDIAN_DESCRIPTORS
from .Section         import SectionExistsDescriptor
from .StreamAlignment import AlignmentDescriptor
from .StreamEOF       import AssertEOFDescriptor
from .StreamOffset    import EnforceOffsetDescriptor
from .StreamPadding   import PaddingDescriptor
from .Strings         import BytestringDescriptor
from .Strings         import BytestringsDescriptor
from .Strings         import CBytestringDescriptor
from .Strings         import CBytestringsDescriptor

STANDARD_DESCRIPTORS = [
    AlignmentDescriptor,
    AssertEOFDescriptor,
    BytestringDescriptor,
    BytestringsDescriptor,
    CBytestringDescriptor,
    CBytestringsDescriptor,
    DescriptorDescriptor,
    DynamicObjectDescriptor,
    DynamicObjectsDescriptor,
    EnforceOffsetDescriptor,
    ObjectDescriptor,
    PaddingDescriptor,
    *PRIMITIVE_DESCRIPTORS,
    *PRIMITIVE_ARRAY_DESCRIPTORS,
    SectionExistsDescriptor
]

STANDARD_ENDIAN_DESCRIPTORS = [
    *PRIMITIVE_ENDIAN_DESCRIPTORS,
    *PRIMITIVE_ENDIAN_ARRAY_DESCRIPTORS
]
