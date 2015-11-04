from collections import namedtuple

from libp2p.peer.multiaddr.exceptions import ProtocolException


# Definitions of protocol names, codes, and address sizes--respectively.

IP4  =  'ip4'
TCP  =  'tcp'
UDP  =  'udp'
DCCP = 'dccp'
IP6  =  'ip6'
SCTP = 'sctp'
IPFS = 'ipfs'


__protocol_names = {
            IP4  : (  IP4,   4,  32),
            TCP  : (  TCP,   6,  16),
            UDP  : (  UDP,  17,  16),
            DCCP : ( DCCP,  33,  16),
            IP6  : (  IP6,  41, 128),
            SCTP : ( SCTP, 132,  16),
            IPFS : ( IPFS,  21,  -1)   # IPFS hashes are varint encoded
        }

__protocol_codes = dict([(p[1], p) for p in __protocol_names.values()])


Protocol = namedtuple('Protocol', ('name', 'code', 'size'))


def get_by_code(code):
    try:
        args = __protocol_codes[int(code)]
    except:
        try:
            msg = "Invalid protocol code: {}".format(code)
        except:
            msg = "Invalid protocol code"
        raise ProtocolException(msg)
    else:
        return Protocol(*args)


def get_by_name(name):
    try:
        args =  __protocol_names[str(name).lower()]
    except:
        try:
            msg = "Invalid protocol name: {}".format(name)
        except:
            msg = "Invalid protocol name"
        raise ProtocolException(msg)
    else:
        return Protocol(*args)
