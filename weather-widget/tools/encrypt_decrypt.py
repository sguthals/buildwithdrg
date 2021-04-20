from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256
import base64

def encrypt(text, key):
    bs = 16
    key = sha256(key.encode()).digest()
    pl = lambda s: bs - len(s) % bs
    pad = lambda s: s + pl(s) * bytes([pl(s)])
    encodeAES = lambda c, i, s: c.encrypt(pad(s.encode()))
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = encodeAES(cipher, iv, text)
    return base64.b64encode(iv + ct).decode()


def decrypt(data, key): 
    data = base64.b64decode(data)
    iv = data[:16] 
    ct = data[16:]
    key = sha256(key.encode()).digest()
    unpad = lambda pd: pd[:-pd[-1]]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decodeAES = unpad(cipher.decrypt(ct)).decode()
    return decodeAES

