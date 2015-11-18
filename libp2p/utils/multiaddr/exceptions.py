from libp2p.exceptions import Libp2pException


class MultiAddressException(Libp2pException):
    pass


class AddressException(MultiAddressException):
    pass


class ProtocolException(MultiAddressException):
    pass
