from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA
from base64 import b64decode
def decode(cipherData):
    f = open("private_key.txt","r")
    private_key = f.read()
    f.close()
    decoded_key = b64decode(str.encode(private_key))
    rsa_key = RSA.importKey(decoded_key)
    key = PKCS1_OAEP.new(rsa_key)

    raw_cipher_data = b64decode(cipherData)
    phn = key.decrypt(raw_cipher_data)
    phn = phn.decode('utf-8')
    return (phn)
