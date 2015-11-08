import sys
sys.path.append('..')

import asyncio
import libp2p


class TestSubsystem(libp2p.reactor.BaseSubsystem):

    def init(self):
        self.reactor.schedule_task(2, self.some_task, loop=True)
        yield from self.add_message("Hello World")

    @asyncio.coroutine
    def some_task(self):
        yield print("some sweet task")

    def handle_message(self, msg):
        yield print(msg)


if __name__ == "__main__":
    reactor = libp2p.reactor.AsyncioReactor()
    reactor.add_subsystem("test", TestSubsystem())
    reactor.run()
