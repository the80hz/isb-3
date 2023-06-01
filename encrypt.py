"""
2. Шифрование данных гибридной системой
Входные параметры:
1) путь к шифруемому текстовому файлу (очевидно, что файл должен быть достаточно объемным);
2) путь к закрытому ключу ассиметричного алгоритма;
3) путь к зашированному ключу симметричного алгоритма;
4) путь, по которому сохранить зашифрованный текстовый файл;

2.1. Расшифровать симметричный ключ.
2.2. Зашифровать текст симметричным алгоритмом и сохранить по указанному пути.
"""

# Path: encrypt.py

import argparse
import os

from cryptography.hazmat.primitives import serialization, asymmetric, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_file(data_path, private_key_path, symmetric_key_path, encrypted_data_path):
    # 2.1. Расшифровать симметричный ключ.
    with open(symmetric_key_path, 'rb') as f:
        symmetric_key = f.read()
    with open(private_key_path, 'rb') as f:
        private_key_bytes = f.read()
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    symmetric_key = private_key.decrypt(
        symmetric_key,
        padding=asymmetric.padding.OAEP(
            mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # 2.2. Зашифровать текст симметричным алгоритмом и сохранить по указанному пути.
    with open(data_path, 'rb') as f:
        data = f.read()
    cipher = Cipher(algorithms.Camellia(symmetric_key), modes.CBC(os.urandom(16)))
    encryptor = cipher.encryptor()
    ct = encryptor.update(data) + encryptor.finalize()
    with open(encrypted_data_path, 'wb') as f:
        f.write(ct)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt data')
    parser.add_argument('--data_path', type=str,
                        default='file.txt', help='Path to data file')
    parser.add_argument('--public_key_path', type=str,
                        default='out/keys/public_key.pem', help='Path to public key')
    parser.add_argument('--symmetric_key_path', type=str,
                        default='out/keys/symmetric_key.txt', help='Path to symmetric key')
    parser.add_argument('--encrypted_data_path', type=str,
                        default='out/encrypted_file.txt', help='Path to encrypted data file')
    args = parser.parse_args()

    encrypt_file(args.data_path, args.public_key_path, args.symmetric_key_path, args.encrypted_data_path)
