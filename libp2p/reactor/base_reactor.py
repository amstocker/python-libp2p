"""
This is an abstract base class for the reactor implementations used in
libp2p.
"""


class BaseReactor(object):
    """
    An reactor implementation must implement coroutine functionality and
    also network protocol functionality.
    """
    
    def run(*args, **kwargs):
        raise NotImplemented

    def add_event(*args, **kwargs):
        raise NotImplemented

    def cancel_event(*args, **kwargs):
        raise NotImplemented

    """
    etc...

    build asyncio reactor first then flesh this out.
    """
