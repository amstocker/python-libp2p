import asyncio

from libp2p.exceptions import Libp2pException
from libp2p.reactor.base_reactor import *
from libp2p.reactor.asyncio_reactor import *
from libp2p.reactor.base_subsystem import *

"""
By default 
"""
_reactor_cls = AsyncioReactor
_reactor = None


def use_reactor_cls(cls):
    if not issubclass(cls, BaseReactor):
        raise Libp2pException
    else:
        global _reactor_cls
        _reactor_cls = cls


def get_reactor():
    global _reactor

    if _reactor:
        return _reactor
    else:
        _reactor = _reactor_cls()
        return _reactor
