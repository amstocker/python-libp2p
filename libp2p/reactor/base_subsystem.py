"""
Abstract base class for libp2p subsystems that plug into the reactor.
"""
import asyncio

import libp2p.reactor


class BaseSubsystem(object):

    def __init__(self, reactor=None, *args, **kwargs):
        self.reactor = libp2p.reactor.get_reactor()
        self._queue = asyncio.Queue()
        self._running = False

        # check to make sure method implementations are coroutines, if not then
        # wrap them with `asyncio.coroutine`.
        for method in (self.__class__.init,
                       self.__class__.handle_message):
            if not asyncio.iscoroutinefunction(method):
                method = asyncio.coroutine(method)

    @asyncio.coroutine
    def init(self, *args, **kwargs):
        pass

    @asyncio.coroutine
    def run(self):
        """
        Start this subsystem.  The defaul behavior is to wait for messages in
        the message queue and then act upon them and possible add more tasks to
        the main event loop such as network requests, etc.
        """
        # run initialization coroutine
        yield from self.init()

        self._running = True
        while self._running:
            msg = yield from self._queue.get()
            if msg:
                yield from self.handle_message(msg)

    @asyncio.coroutine
    def add_message(self, msg):
        yield from self._queue.put(msg)

    @asyncio.coroutine
    def handle_message(self, msg):
        raise NotImplemented
