from libp2p.peer.multiaddr import parse


class MultiAddress(object):
    
    def __init__(self, address):
        str_repr, byte_repr = parse.parse_addr(address)
        
        self.str_repr = str_repr
        self.byte_repr = byte_repr


    def __repr__(self):
        return "<multiaddr:{}>".format(self.str_repr)

    def as_bytes(self):
        """
        Returns the binary format as an immutable bytes object.
        """
        return bytes(self.byte_repr)
