from Crypto.PublicKey import RSA

def generate_keys():
    key = RSA.generate(2048)

    # Save the private key
    with open('key/private_key.pem', 'wb') as priv_file:
        priv_file.write(key.export_key())
    
    # Save the public key
    with open('key/public_key.pem', 'wb') as pub_file:
        pub_file.write(key.publickey().export_key())

    print("✅ Keys generated successfully inside the 'key' folder.")

if __name__ == "__main__":
    generate_keys()
