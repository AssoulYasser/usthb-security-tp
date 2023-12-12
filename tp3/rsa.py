from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

def generate_rsa_key_pair(key_size=2048):
    def remove_pem_header_footer(pem_key):
        lines = pem_key.splitlines()
        return ''.join(lines[1:-1])

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )

    # Get the public key in PEM format
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Get the private key in PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Remove PEM header and footer from private and public keys
    private_key_content = remove_pem_header_footer(private_key_pem.decode('utf-8'))
    public_key_content = remove_pem_header_footer(public_key.decode('utf-8'))

    return private_key_content, public_key_content

def dectyption(private_key_der_b64,encrypted_data_b64):

    decode_base64 = lambda s: base64.b64decode(s.encode('utf-8'))

    # private_key_bytes = decode_base64(private_key_b64)
    private_key_der_bytes = decode_base64(private_key_der_b64)
    encrypted_data_bytes = decode_base64(encrypted_data_b64)

    # Load private key in DER format
    private_key = serialization.load_der_private_key(private_key_der_bytes, password=None, backend=default_backend())

    print("Ciphertext Length:", len(encrypted_data_bytes))

    # Decrypt the data
    decrypted_data = private_key.decrypt(
        encrypted_data_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data.decode('utf-8')