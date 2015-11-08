import sys
sys.path.append('..')

from libp2p.peer.multiaddr import MultiAddress
from libp2p.utils.base58 import b58encode, b58decode


with open('base58_encode_decode.json') as f:
    import json
    tests = json.loads(f.read())

for d, e in tests:
    if len(d) == 0:
        continue
    i = int(d, 16)
    print("{} -> {} (should be: {})".format(d, b58encode(i), e))


ma = MultiAddress("/ip4/127.0.0.1/tcp/4001/ipfs/QmerTTan8gkTEugcb4DmFpAw8Z7bkDQfhoGh6AHzQaqD1Y")

print(ma)
print(len(ma.str_repr))
print(ma.as_bytes().__repr__())
print(len(ma.as_bytes()))

ma2 = MultiAddress(ma.as_bytes())

print(ma2)
print(len(ma2.str_repr))
print(ma2.as_bytes().__repr__())
print(len(ma2.as_bytes()))
