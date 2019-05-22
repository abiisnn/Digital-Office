import codecs
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# CIPHER
# Supongamos que uriel le envia un memorandum confidencial a Gaboxd

# Quiere enviar este mensaje:
message = 'Hola mundo, soy un mensaje en texto plano, todo el mundo puede leerme.'
message = message.encode()

# Consulta a la bd y obtiene la siguiente direccion de la llave PUBLICA de Gaboxd
fileName = "publicKeys/Gaboxd_publicKey.txt"
public_key = RSA.importKey(open(fileName).read())

# Uriel cifra el mensaje con la llave publica de Gaboxd que tiene guardada en la BD
cipher = PKCS1_OAEP.new(public_key)
encrypted_message  = cipher.encrypt(message)

# No se exactamente como guardar en la bd el texto cifrado, pero esto te puede servir:
hexify = codecs.getencoder ('hex')
m = hexify(encrypted_message)[0]

encrypted_message = m.decode()
print("MENSAJE CIFRADO\n")
print(encrypted_message)
print(type(encrypted_message))
print("\n\n")


# RECUPERAR DE LA BD
encrypted_message = encrypted_message.encode()
hexify = codecs.getdecoder('hex')
encrypted_message = hexify(encrypted_message)[0]

# Cuando Gabo ve el mensaje, usa su llave privada para verlo:
fileName = "privateKeys/Gaboxd_privateKey.txt"
private_key = RSA.importKey(open(fileName).read())

cipher = PKCS1_OAEP.new(private_key)
message = cipher.decrypt(encrypted_message)


print("MENSAJE ORIGINAL\n")
print(message)
print("\n\n")

