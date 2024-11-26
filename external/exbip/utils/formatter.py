def safe_formatter(formatter):
    def formatter_impl(value):
        try:
            return formatter(value)
        except TypeError:
            return value
        except ValueError:
            return value
    return formatter_impl

list_formatter  = safe_formatter(list)

bin8_formatter  = safe_formatter('0x{0:0>8b}'.format)
bin16_formatter = safe_formatter('0x{0:0>16b}'.format)
bin32_formatter = safe_formatter('0x{0:0>32b}'.format)
bin64_formatter = safe_formatter('0x{0:0>64b}'.format)

hex8_formatter  = safe_formatter('0x{0:0>2x}'.format)
hex16_formatter = safe_formatter('0x{0:0>4x}'.format)
hex32_formatter = safe_formatter('0x{0:0>8x}'.format)
hex64_formatter = safe_formatter('0x{0:0>16x}'.format)

HEX8_formatter  = safe_formatter('0x{0:0>2X}'.format)
HEX16_formatter = safe_formatter('0x{0:0>4X}'.format)
HEX32_formatter = safe_formatter('0x{0:0>8X}'.format)
HEX64_formatter = safe_formatter('0x{0:0>16X}'.format)
