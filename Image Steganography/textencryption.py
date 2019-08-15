#ch9_encrypt_blob.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib
import base64

#Our Encryption Function
def encrypt_blob(blob, public_key):
    #Import the Public Key and use for encryption using PKCS1_OAEP
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    #compress the data first
    blob = zlib.compress(blob)

    #In determining the chunk size, determine the private key length used in bytes
    #and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
    #in chunks
    chunk_size = 470
    offset = 0
    end_loop = False
    count = 0
  ##  encrypted = ""

    while not end_loop:
        #The chunk
        chunk = blob[offset:offset + chunk_size]

        #If the data chunk is less then the chunk size, then we need to add
        #padding with " ". This indicates the we reached the end of the file
        #so we end loop here
        if len(chunk) % chunk_size != 0:
            end_loop = True
            temp = " "*(chunk_size - len(chunk))
            ##b = bytearray([temp[,encoding[,erroors]]])
            b = temp.encode()
            chunk += b

      ##  print(type(chunk))
        #Append the encrypted chunk to the overall encrypted file

        if count > 0 :
            encrypted =  encrypted + rsa_key.encrypt(chunk)
        if count == 0:
            encrypted = rsa_key.encrypt(chunk)
            count = count+1



        #Increase the offset by chunk size
        offset = offset + chunk_size

    #Base 64 encode the encrypted file
    return base64.b64encode(encrypted)

#Use the public key for encryption
fd = open("public_key.pem", "rb")
public_key = fd.read()
print(public_key)
fd.close()

#Our candidate file to be encrypted
fd = open("man.txt", "rb")
unencrypted_blob = fd.read()
fd.close()

encrypted_blob = encrypt_blob(unencrypted_blob, public_key)

#Write the encrypted contents to a file
fd = open("encrypted_txt.txt", "wb")
fd.write(encrypted_blob)
fd.close()