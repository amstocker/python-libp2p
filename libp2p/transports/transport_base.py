"""
Abstract base classes for transports.
"""


class TransportBase:
    """
    Abstract base class for Transport objects.
    """
    def create_connection(self, address, **kwargs):
        raise NotImplemented

    def create_listener(self, **kwargs):
        raise NotImplemented

