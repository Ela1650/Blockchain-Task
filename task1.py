# 1. Write a python code that generates public and private keys, signs a message using the private key, and verifies the signature using the public key.

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def generate_keys():
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    # Generate public key
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(private_key, message):
    return private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def verify_signature(public_key, message, signature):
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        return False

# Main code
private_key, public_key = generate_keys()

print("Private Key generated.")
print("Public Key generated.")

message = b"Hello, this is a secret message!"
signature = sign_message(private_key, message)

print("\nSignature:")
print(signature.hex())

if verify_signature(public_key, message, signature):
    print("\nSignature verified successfully!")
else:
    print("\nSignature verification failed.")
