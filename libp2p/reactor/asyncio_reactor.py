"""
Implementation of Reactor using asyncio.
"""
import asyncio

from .base_reactor import BaseReactor


class AsyncIOReactor(BaseReactor):
    
    def __init__(self, loop=None, **options):
        self._loop = loop or asyncio.get_event_loop()
        self._subsystems = {}

    def add_subsystem(self, name, subsys_obj):
        self._subsystems[name] = subsys_obj

    def run(self):
        tasks = asyncio.wait(
                  [asyncio.ensure_future(s) for s in self._subsystems.values()]
                )

        self._loop.run_until_complete(tasks)
        self._loop.close()
