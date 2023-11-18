import bpy


class Encodable:
    @staticmethod
    def attr():
        raise NotImplementedError

    @staticmethod
    def enum_id():
        raise NotImplementedError

    @staticmethod
    def enum_item():
        raise NotImplementedError

    @staticmethod
    def encode(value):
        raise NotImplementedError


    @classmethod
    def prop_getter(cls, self):
        attr = cls.attr()
        if attr not in self:
            self[attr] = ""
        return self[attr]

    @classmethod
    def prop_setter(cls, self, value):
        attr = cls.attr()
        cls.encode(value)
        self[attr] = value


class UTF8Encodable(Encodable):
    @staticmethod
    def attr():
        return "utf8_override_name"

    @staticmethod
    def enum_id():
        return "UTF8"

    @staticmethod
    def enum_item():
        return "UTF8", "UTF-8", "This object has a UTF-8-encodable override name"

    @staticmethod
    def encode(value):
        try:
            return value.encode("utf8")
        except UnicodeEncodeError:
            raise ValueError(f"Cannot be encoded as UTF-8: '{value}'")


class SJISEncodable(Encodable):
    @staticmethod
    def attr():
        return "sjis_override_name"

    @staticmethod
    def enum_id():
        return "SJIS"

    @staticmethod
    def enum_item():
        return "SJIS", "Shift-JIS", "This object has a Shift-JIS-encodable override name"

    @staticmethod
    def encode(value):
        try:
            return value.encode("shiftjis")
        except UnicodeEncodeError: raise\
            ValueError(f"Cannot be encoded as Shift-JIS: '{value}'")


class HEXEncodable(Encodable):
    @staticmethod
    def attr():
        return "hex_override_name"

    @staticmethod
    def enum_id():
        return "HEX"

    @staticmethod
    def enum_item():
        return "HEX", "Hex", "This object has an override name only representable as hexadecimal numbers"

    @staticmethod
    def encode(value):
        try:
            return bytes.fromhex(value)
        except ValueError:
            raise ValueError(f"Not a valid hex string: '{value}'")


def override_name_prop(encodable):
    return bpy.props.StringProperty(
        name="Override Name",
        description="The name that the object will be given upon export",
        get=encodable.prop_getter,
        set=encodable.prop_setter
    )


USED_ENCODINGS = [UTF8Encodable, SJISEncodable, HEXEncodable]


def get_active_encoding(self):
    for encoding in USED_ENCODINGS:
        if self.override_name_encoding == encoding.enum_id():
            return encoding
    raise NotImplementedError(f"CRITICAL INTERNAL ERROR: Unrecognised Override Name Encoding '{self.override_name_encoding}'")


def draw(self, layout):
    col = layout.column()
    col.prop(self, "name")
    col.prop(self, "has_override_name")
    if self.has_override_name:
        row = col.split(0.2)
        row.prop(self, "override_name_encoding")
        encoding = self.get_active_encoding()
        row.prop(self, encoding.attr())


def gfs_name_getter(self):
    if self.has_override_name:
        encoding = self.get_active_encoding()
        return encoding.encode(self[encoding.attr()])
    else:
        return self.name


class GFSNamedProperty:
    name: bpy.props.StringProperty(name="Name")

    def get_active_encoding(self):
        return None

    @property
    def gfs_name(self):
        return self.name

    def draw(self, layout):
        col = layout.column()
        col.prop(self, "name")


if len(USED_ENCODINGS):
    # Blender property definitions
    GFSNamedProperty.__annotations__["has_override_name"] = bpy.props.BoolProperty(
        name="Has Override Name",
        description="Whether the object has an override name"
    )
    GFSNamedProperty.__annotations__["override_name_encoding"] = bpy.props.EnumProperty(
            items=[encoding.enum_item() for encoding in USED_ENCODINGS],
            name="Override Name Encoding",
            description="The encoding scheme that is used to serialise the name on export",
            default=USED_ENCODINGS[0].enum_id()
        )
    for encoding in USED_ENCODINGS:
        GFSNamedProperty.__annotations__[encoding.attr()] = override_name_prop(encoding)

    # Prop group method redefinitions
    setattr(GFSNamedProperty, "draw", draw)
    setattr(GFSNamedProperty, "get_active_encoding", get_active_encoding)
    setattr(GFSNamedProperty, "gfs_name", property(fget=gfs_name_getter))
