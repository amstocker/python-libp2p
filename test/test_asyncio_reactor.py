import sys
sys.path.append('..')

import asyncio
from libp2p import reactor

from pprint import pprint


class TestSubsystem(reactor.BaseSubsystem):

    def init(self):
        self.reactor.schedule_task(2, self.some_async_task, loop=True)
        self.reactor.schedule_task(3, self.some_task, loop=True)
        yield from self.add_message("Hello World")

    @asyncio.coroutine
    def some_async_task(self):
        yield print("some sweet async task")

    def some_task(self):
        print('='*10 + ' RUNNING TASKS ' + '='*10)
        pprint(self.reactor._tasks)
        print('='*35)

    def handle_message(self, msg):
        yield print(msg)


if __name__ == "__main__":
    r = reactor.get_reactor()
    r.add_subsystem("test", TestSubsystem())
    r.run()
