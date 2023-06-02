import argparse
import os
import logging

from cryptography.hazmat.primitives import serialization, asymmetric, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

logging.basicConfig(level=logging.INFO)


def generate_keys(symmetric_key_path: str, public_key_path: str, private_key_path: str):
    """
    Генерация ключей гибридной системы
    :param symmetric_key_path:  путь, по которому сериализовать зашифрованный симметричный ключ;
    :param public_key_path:     путь, по которому сериализовать открытый ключ;
    :param private_key_path:    путь, по которому сериазизовать закрытый ключ.
    :return:
    """
    logging.info('Generating keys...')

    symmetric_key = os.urandom(16)
    logging.info('Symmetric key generated.')

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    logging.info('Asymmetric keys generated.')

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    logging.info('Asymmetric keys serialized.')

    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        asymmetric.padding.OAEP(
            mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    logging.info('Symmetric key encrypted.')

    try:
        with open(symmetric_key_path, 'wb') as f:
            f.write(encrypted_symmetric_key)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(symmetric_key_path))
        with open(symmetric_key_path, 'wb') as f:
            f.write(encrypted_symmetric_key)
    logging.info('Encrypted symmetric key saved.')

    try:
        with open(public_key_path, 'wb') as f:
            f.write(public_key_bytes)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(public_key_path))
        with open(public_key_path, 'wb') as f:
            f.write(public_key_bytes)
    logging.info('Public key saved.')

    try:
        with open(private_key_path, 'wb') as f:
            f.write(private_key_bytes)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(private_key_path))
        with open(private_key_path, 'wb') as f:
            f.write(private_key_bytes)
    logging.info('Private key saved.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate keys for hybrid crypto-system')
    parser.add_argument('--symmetric_key_path', type=str,
                        default='out/keys/symmetric_key.txt', help='Path to save symmetric key')
    parser.add_argument('--public_key_path', type=str,
                        default='out/keys/public_key.pem', help='Path to save public key')
    parser.add_argument('--private_key_path', type=str,
                        default='out/keys/private_key.pem', help='Path to save private key')
    args = parser.parse_args()

    generate_keys(args.symmetric_key_path, args.public_key_path, args.private_key_path)
