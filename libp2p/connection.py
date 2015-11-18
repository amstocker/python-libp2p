class ConnectionBase:
    """
    Abstract base class for Connection objects.
    """
    @property
    def is_listener(self):
        raise NotImplemented

    # @coroutine
    def dial(self):
        raise NotImplemented
    
    # @coroutine
    def accept(self):
        raise NotImplemented
