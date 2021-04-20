import os
import pickle
import json

from tools.encrypt_decrypt import decrypt


def get_key(val):
    p = os.environ[val]
    with open("key.bin", "rb") as fh:
        data = pickle.loads(fh.read())
    key = decrypt(data, p)
    return key
