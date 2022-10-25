import hashlib


def getMd5Hexa(byte_input):
    return hashlib.md5(byte_input).hexdigest()
