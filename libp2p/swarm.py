import async
from collections import namedtuple


SwarmConfig = namedtuple('SwarmConfig', [
    'peerid',
    'transports',
    'multiplexers',
    'handlers'
    ])


class Swarm:

    def __init__(self, cfg):
        
        self._info = cfg.peerid             # peer id for this host
        self._transports = cfg.transports   # supported transports
        self._muxers = cfg.multiplexers     # supported multiplexers
        self._handlers = cfg.handlers       # handlers for supported protocols
        
        self._conns = {}                    # active connections
        self._muxed_conns = {}              # active multiplexed connections
        self._listeners = {}                # active listeners

    @async.coroutine
    def dial(peer_info, protocol, **kwargs):
        """
        1. Check if there is an existing connection to the given peer that is
           either straight or multiplexed.  If so, either upgrade the straight
           connection to a multiplexed one and return that, or return the
           existing multiplexed connection.
        2. If there is no existing connection, create a new one.
            2a. Check that we support the transports in at least one of the
                multiaddresses provided by the peer info.
            2b. Try creating connections with the given multiaddresses until
                one works (TODO: perferences?).
            2c. Return connection object.
        """
        pass
