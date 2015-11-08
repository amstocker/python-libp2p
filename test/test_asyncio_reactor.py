import sys
sys.path.append('..')

import asyncio
from libp2p import reactor

from pprint import pprint


class TestSubsystem(reactor.BaseSubsystem):

    def init(self):
        self.reactor.schedule_task(2, self.some_async_task, loop=True)
        self.reactor.schedule_task(5, self.some_task, loop=True)
        yield from self.add_message("Hello World")

    @asyncio.coroutine
    def some_async_task(self):
        yield from self.add_message("async stuff")

    def some_task(self):
        print("SS1: blocking stuff")

    def handle_message(self, msg):
        yield print("SS1 processing message: ", msg)


class TestSubsystem2(reactor.BaseSubsystem):

    def __init__(self, other):
        self.other = other
        super().__init__(self)

    def init(self):
        self.reactor.schedule_task(3, self.some_async_task, loop=True)
        self.reactor.schedule_task(4, self.some_task, loop=True)
        yield from self.add_message("Hello World")

    @asyncio.coroutine
    def some_async_task(self):
        yield from self.other.add_message("msg from test2")

    def some_task(self):
        print("SS2: blocking stuff")

    def handle_message(self, msg):
        yield print("SS2 processing message: ", msg)


if __name__ == "__main__":
    r = reactor.get_reactor()

    # here I would like to be able to do:
    #   `r.set_protocol_handler(protocol, t1)`
    t1 = TestSubsystem()
    r.add_subsystem("test1", t1)
    r.add_subsystem("test2", TestSubsystem2(t1))
    r.run()
