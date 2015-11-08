"""
Varint encoding library.

ref:  https://developers.google.com/protocol-buffers/docs/encoding?hl=en
"""


def uvarint_encode(value):
    buf = bytearray()
    bits = value & 0x7f
    value >>= 7
    size = 1
    while value:
        buf.append(0x80|bits)
        bits = value & 0x7f
        value >>= 7
        size += 1
    buf.append(bits)
    return bytes(buf), size


def uvarint_decode(buf):
    if not isinstance(buf, (bytes, bytearray)):
        buf = bytes(buf)
    size = result = shift = 0
    while True:
        b = buf[size]
        result |= ((b & 0x7f) << shift)
        size += 1
        if not (b & 0x80):
            return result, size
        shift += 7
