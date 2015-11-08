import sys
sys.path.append('..')

import asyncio
import libp2p


class TestSubsystem(libp2p.reactor.BaseSubsystem):

    def init(self):
        yield from self.add_message("Hello World")
    
    def handle_message(self, msg):
        yield print(msg)


if __name__ == "__main__":
    reactor = libp2p.reactor.AsyncioReactor()
    reactor.add_subsystem("test", TestSubsystem())
    reactor.run()
