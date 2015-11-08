"""
Implementation of Reactor using asyncio.
"""
import asyncio
import functools

from libp2p.reactor.base_reactor import BaseReactor


class AsyncioReactor(BaseReactor):

    def __init__(self, loop=None, **options):
        self._loop = loop or asyncio.get_event_loop()
        self._subsystems = {}
        self._running = True

    def add_subsystem(self, name, subsys_obj):
        """
        Registers an async subsystem with the asyncio event loop.  `subsys_obj`
        must inherit from `libp2p.reactor.BaseSubsystem`.
        """
        self._subsystems[name] = subsys_obj

    def run(self):
        """
        Starts all subsystems and runs until `self.stop()` is called.
        """
        self._running = True
        fs = asyncio.wait([asyncio.async(s.run())
                            for s in self._subsystems.values()])
        self._loop.run_until_complete(fs)
        self._running = False

    def stop(self):
        return self._loop.stop()

    def is_running(self):
        return self._loop.is_running()

    @property
    def _tasks(self):
        """
        Returns all tasks scheduled on the current event loop.
        """
        return asyncio.Task.all_tasks()

    def schedule_task(self, delay, func_or_coro, *args, **kwargs):
        """
        Starts a task with the given `delay` (in seconds).  `func_or_coro` must
        be a function or a coroutine.
        """
        # loop indefinitely?
        loop = kwargs.pop('loop', False)

        @asyncio.coroutine
        def job():
            yield from asyncio.sleep(delay)
            # check to see if job is a coroutine...
            if asyncio.iscoroutinefunction(func_or_coro):
                yield from func_or_coro()
            else:
                yield func_or_coro()
            # if we are looping, create a new task for this job
            if loop:
                self._loop.create_task(job())

        return self._loop.create_task(job())
