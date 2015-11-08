from libp2p.reactor.base_subsystem import *
from libp2p.reactor.base_reactor import *
from libp2p.reactor.asyncio_reactor import *


default_reactor_cls = AsyncioReactor

_reactor = None

def get_reactor():
    global _reactor

    if _reactor:
        return _reactor
    else:
        _reactor = default_reactor_cls()
        return _reactor
