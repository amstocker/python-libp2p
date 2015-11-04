"""
Conversions between python types and bytes objects.
"""
from socket import AF_INET6, inet_aton, inet_ntoa, inet_ntop, inet_pton
import struct

from multiaddr import protocols
from multiaddr.exceptions import AddressException
from multiaddr.utils.base58 import b58encode, b58decode
from multiaddr.utils.varint import uvarint_encode, uvarint_decode


 ########
 # IPv4 #
 ########

def ip4_string_to_bytes(string):
    """
    Converts an ip4 address from string representation to a bytes object.
    """
    return inet_aton(string)


def ip4_bytes_to_long(ip4):
    """
    Converts an ip4 address from byte representation to a long.
    """
    return struct.unpack('!L', ip4)[0]


def ip4_long_to_bytes(ip4):
    """
    Converts an ip4 address from long representation to a bytes object.
    """
    return struct.pack('!L', ip4)


def ip4_bytes_to_string(ip4):
    """
    Converts an ip4 address from long representation to a string.
    """
    return inet_ntoa(ip4)


 ########
 # IPv6 #
 ########

def ip6_string_to_bytes(string):
    """
    Converts an ip6 address from string representation to a bytes object.
    """
    return inet_pton(AF_INET6, string)


def ip6_bytes_to_long(ip6):
    """
    Converts an ip6 address from byte representation to a long.
    """
    a, b = struct.unpack('!QQ', ip6)
    return (a << 64) | b


def ip6_long_to_bytes(ip6):
    """
    Converts an ip6 address from 16 byte long representation to a bytes object.
    """
    a, b = ip6 >> 64, ip6 % (2<<64)
    return struct.pack('!QQ', a, b)


def ip6_bytes_to_string(ip6):
    """
    Converts an ip6 address from long representation to a string.
    """
    return inet_ntop(AF_INET6, ip6)



 ########
 # Misc #
 ########

def port_to_bytes(port):
    """
    Converts a port number to an unsigned short.
    """
    return struct.pack('!H', int(port))


def port_from_bytes(port):
    """
    Converts a port number from a bytes object to an int.
    """
    return struct.unpack('!H', port)[0]


def proto_to_bytes(code):
    """
    Converts a protocol code into an unsigned varint.
    """
    return uvarint_encode(code)[0]


def proto_from_bytes(code):
    """
    Converts a protocol code from a bytes oject to an int.
    """
    return uvarint_decode(code)[0]



def multihash_to_bytes(string):
    """
    Converts a multihash string as an unsigned varint.
    """
    return uvarint_encode(b58decode(string))[0]


def multihash_to_string(mhash):
    """
    Converts a uvarint encoded multihash into a string.
    """
    return b58encode(uvarint_decode(mhash)[0])



def to_bytes(proto, string):
    """
    Properly converts address string or port to bytes based on given protocol.
    """
    if proto.name == protocols.IP4:
        addr = ip4_string_to_bytes(string)
    elif proto.name == protocols.IP6:
        addr = ip6_string_to_bytes(string)
    elif proto.name == protocols.TCP:
        addr = port_to_bytes(string)
    elif proto.name == protocols.UDP:
        addr = port_to_bytes(string)
    elif proto.name == protocols.IPFS:
        addr = multihash_to_bytes(string)
    else:
        msg = "Protocol not implemented: {}".format(proto.name)
        raise AddressException(msg)
    return addr


def to_string(proto, addr):
    """
    Properly converts bytes to string or int representation based on the given
    protocol.  Returns string representation of address and the number of bytes
    from the buffer consumed.
    """
    if proto.name == protocols.IP4:
        size = proto.size//8
        string = ip4_bytes_to_string(addr[:size])
    elif proto.name == protocols.IP6:
        size = proto.size//8
        string = ip6_bytes_to_string(addr[:size])
    elif proto.name == protocols.TCP:
        size = proto.size//8
        string = port_from_bytes(addr[:size])
    elif proto.name == protocols.UDP:
        size = proto.size//8
        string = port_from_bytes(addr[:size])
    elif proto.name == protocols.IPFS:
        varint, size = uvarint_decode(addr)
        string = b58encode(varint)
    else:
        msg = "Protocol not implemented: {}".format(proto.name)
        raise AddressException(msg)
    return string, size
