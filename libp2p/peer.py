from collections import namedtuple


PeerID = namedtuple('PeerID', [
    'id',
    'public_key',
    'private_key'
    ])


PeerInfo = namedtuple('PeerInfo', [
    'id',
    'multiaddrs'
    ])
