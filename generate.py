"""
1. Генерация ключей гибридной системы
Входные параметры:
1) путь, по которому сериализовать зашифрованный симметричный ключ;
2) путь, по которому сериализовать открытый ключ;
3) путь, по которому сериазизовать закрытый ключ.

1.1. Сгеренировать ключ для симметричного алгоритма Camellia.
1.2. Сгенерировать ключи для ассиметричного алгоритма RSA.
1.3. Сериализовать ассиметричные ключи.
1.4. Зашифровать ключ симметричного шифрования открытым ключом и сохранить по указанному пути.
"""

# Path: generate.py

import argparse
import os

from cryptography.hazmat.primitives import serialization, asymmetric, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_keys(symmetric_key_path: str, public_key_path: str, private_key_path: str):
    """
    Генерация ключей гибридной системы
    :param symmetric_key_path:  путь, по которому сериализовать зашифрованный симметричный ключ;
    :param public_key_path:     путь, по которому сериализовать открытый ключ;
    :param private_key_path:    путь, по которому сериазизовать закрытый ключ.
    :return:
    """
    # 1.1. Сгеренировать ключ для симметричного алгоритма Camellia.
    symmetric_key = os.urandom(16)

    # 1.2. Сгенерировать ключи для ассиметричного алгоритма RSA.
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # 1.3. Сериализовать ассиметричные ключи.
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # 1.4. Зашифровать ключ симметричного шифрования открытым ключом и сохранить по указанному пути.
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        asymmetric.padding.OAEP(
            mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(symmetric_key_path, 'wb') as f:
        f.write(encrypted_symmetric_key)
    with open(public_key_path, 'wb') as f:
        f.write(public_key_bytes)
    with open(private_key_path, 'wb') as f:
        f.write(private_key_bytes)


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
