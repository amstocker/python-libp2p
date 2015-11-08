"""
MultiAddress string and byte parsing.
"""
from libp2p.peer.multiaddr import protocols, conversion
from libp2p.peer.multiaddr.exceptions import AddressException
from libp2p.peer.multiaddr.exceptions import ProtocolException


def raise_invalid(string):
    try:
        msg = "Invalid address: {}".format(string)
    except:
        msg = "Invalid address"
    raise AddressException(msg)


def string_to_tuples(string):
    """
    Converts a multiaddr string into a list of tuples corresponding to each
    address part.
    """
    parts = string.split('/')[1:]
    
    # parts list should be even length
    if len(parts) % 2:
        raise_invalid(string)

    tuples = []

    for i in range(0, len(parts), 2):
        proto = protocols.get_by_name(parts[i])
        tuples.append((proto, parts[i+1]))
    
    return tuples


def tuples_to_bytes(tuples):
    """
    Converts a list of tuples corresponding to the parts of a MultiAddress into
    a bytes object.
    """
    b = bytearray()

    for proto, addr in tuples:
        b.extend(conversion.proto_to_bytes(proto.code))
        b.extend(conversion.to_bytes(proto, addr))

    return bytes(b)


def bytes_to_tuples(addr):
    """
    Converts the binary format of a multiaddr into a list of tuples
    corresponding to each part of the multiaddr.
    """
    tuples = []

    i = 0
    while i < len(addr):
        proto_code, proto_size = conversion.proto_from_bytes(addr[i:])
        proto = protocols.get_by_code(proto_code)
        string, string_size = conversion.to_string(proto, addr[i+proto_size:])
        tuples.append((proto, string))
        i += (string_size+proto_size)

    return tuples


def tuples_to_string(tuples):
    """
    Converts a list of tuples into multiaddr string representation.
    """
    return '/' + '/'.join(['/'.join((t[0].name, str(t[1]))) for t in tuples])


def string_to_bytes(string):
    """
    Converts a multiaddr string into its binary format.
    """
    return tuples_to_bytes(string_to_tuples(string))


def bytes_to_string(addr):
    """
    Converts a multiaddr in binary format to its string representation.
    """
    return tuples_to_string(bytes_to_tuples(addr))

        
def parse_addr(addr):
    """
    Returns the parsed string and binary formats of a given multiaddr.
    """
    if isinstance(addr, str):
        return addr, string_to_bytes(addr)
    elif isinstance(addr, (bytes, bytearray)):    
        return bytes_to_string(addr), addr
    else:
        msg = "Address must be type<str>, type<bytes>, or type<bytearray>"
        raise AddressException(msg) 
