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

import os
import cryptography
import argparse
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_keys(symmetric_key_path, public_key_path, secret_key_path):
    # 1.1. Сгеренировать ключ для симметричного алгоритма Camellia.
    symmetric_key = os.urandom(128)
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
    with open(symmetric_key_path, 'wb') as f:
        f.write(symmetric_key)
    with open(public_key_path, 'wb') as f:
        f.write(public_key_bytes)
    with open(secret_key_path, 'wb') as f:
        f.write(private_key_bytes)

    return symmetric_key, public_key, private_key


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate keys for hybrid cryptosystem')
    parser.add_argument('--symmetric_key_path', type=str, default='out/keys/symmetric_key.txt', help='Path to save symmetric key')
    parser.add_argument('--public_key_path', type=str, default='out/keys/public_key.pem', help='Path to save public key')
    parser.add_argument('--secret_key_path', type=str, default='out/keys/secret_key.pem', help='Path to save secret key')
    args = parser.parse_args()

    generate_keys(args.symmetric_key_path, args.public_key_path, args.secret_key_path)