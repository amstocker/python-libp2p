"""
Base 58 encoding library.
"""
ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

        
def b58encode(num, alpha=ALPHABET):
    """
    Returns num in a base58-encoded string.
    """
    encode = ''
    if (num < 0):
        return ''
    while (num >= 58):  
        mod = num % 58
        encode = alpha[mod] + encode
        num = num / 58
    if (num):
        encode = alpha[num] + encode
    return encode


def b58decode(s, alpha=ALPHABET):
    """
    Decodes the base58-encoded string s into an integer.
    """
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * alpha.index(char)
        multi = multi * 58
    return decoded
