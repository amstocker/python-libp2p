"""
Abstract base class for libp2p subsystems that plug into the reactor.
"""
from libp2p.reactor import get_reactor, coroutine


class BaseSubsystem(object):

    def __init__(self, reactor=None, **kwargs):
        self._reactor = reactor or get_reactor()
        self._queue = self._reactor.queue()
        self._running = False

    @coroutine
    def run(self):
        self._running = True
        while self._running:
            for msg in self._queue.get():
                yield from self.handle(msg):

    @coroutine
    def add_message(self, msg):
        yield from self._queue.add(msg)

    @coroutine
    def handle(self, msg):
        raise NotImplemented

    @coroutine
    def send_subsys_msg(self, name, msg):
        yield from self._reactor.add_subsys_msg(name, msg)
