from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import os

def encrypt_file(file_path, public_key_path):
    # Load the public key
    with open(public_key_path, 'rb') as key_file:
        public_key = RSA.import_key(key_file.read())

    # AES Key Generation (for data encryption)
    aes_key = get_random_bytes(16)  # AES key (16 bytes for AES-128)

    # Encrypt the AES key using RSA
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_aes_key = cipher_rsa.encrypt(aes_key)

    # Encrypt the file data
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    with open(file_path, 'rb') as file:
        file_data = file.read()

    ciphertext, tag = cipher_aes.encrypt_and_digest(file_data)

    # Save the encrypted data
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as enc_file:
        enc_file.write(enc_aes_key + cipher_aes.nonce + tag + ciphertext)

    return encrypted_file_path

if __name__ == "__main__":
    encrypt_file("test.txt", "key/public_key.pem")
