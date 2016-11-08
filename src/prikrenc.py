import armor
import base64
import blowfish

def encrypt_kr(json_str, key):

    json_str = bytes(json_str, "utf-8")

    cipher = blowfish.Cipher(bytes(key, "utf-8"))

    enc = b"".join(cipher.encrypt_ecb_cts(json_str))

    b64 = str(base64.b64encode(enc), "utf-8")
    b64 = armor.insert_newlines(b64, 60)
    a = armor.armor("RSPLUS PRIVATE KEYRING", "", b64)

    return a

def decrypt_kr(bf_str, key):
    x, n = armor.unarmor("RSPLUS PRIVATE KEYRING", bf_str)
    del n
    b64 = x.replace("\n", "")
    b64 = bytes(b64, "utf-8")

    enc = base64.b64decode(b64)
    
    cipher = blowfish.Cipher(bytes(key, "utf-8"))

    json_str = b"".join(cipher.decrypt_ecb_cts(enc))

    return str(json_str, "utf-8")
