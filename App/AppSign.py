from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

key = RSA.generate(1024)
private_key=key.exportKey()
public_key = key.publickey().exportKey()

print(private_key)
print(public_key)