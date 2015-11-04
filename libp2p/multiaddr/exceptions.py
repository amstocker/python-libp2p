
class MultiAddressException(Exception):
    pass


class AddressException(MultiAddressException):
    pass


class ProtocolException(MultiAddressException):
    pass
