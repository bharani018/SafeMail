from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import sys
def decrypt_file(encrypted_file_path, private_key_path):
    # Load the private key
    with open(private_key_path, 'rb') as key_file:
        private_key = RSA.import_key(key_file.read())

    # Read the encrypted file content
    with open(encrypted_file_path, 'rb') as enc_file:
        enc_aes_key = enc_file.read(256)  # RSA-2048 encrypted key is 256 bytes
        nonce = enc_file.read(16)
        tag = enc_file.read(16)
        ciphertext = enc_file.read()

    # Decrypt the AES key using RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(enc_aes_key)

    # Decrypt the file content using AES
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher_aes.decrypt_and_verify(ciphertext, tag)

    # Save decrypted file
    decrypted_file_path = encrypted_file_path.replace('.enc', '_decrypted.txt')
    with open(decrypted_file_path, 'wb') as dec_file:
        dec_file.write(decrypted_data)

    print(f"✅ Decrypted successfully: {decrypted_file_path}")

if __name__ == "__main__":
    
    decrypt_file(sys.argv[1], sys.argv[2])  # Use command-line arguments

