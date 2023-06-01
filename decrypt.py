"""
3. Дешифрование данных гибридной системой
Входные парметры:
1) путь к зашифрованному текстовому файлу;
2) путь к закрытому ключу ассиметричного алгоритма;
3) путь к зашированному ключу симметричного алгоритма;
4) путь, по которому сохранить расшифрованный текстовый файл.

3.1. Расшифровать симметричный ключ.
3.2. Расшифровать текст симметричным алгоритмом и сохранить по указанному пути.
"""

# Path: decrypt.py

import os
import argparse

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decrypt_file(encrypted_data_path, secret_key_path, symmetric_key_path, decrypted_data_path):
    # 3.1. Расшифровать симметричный ключ.
    with open(symmetric_key_path, 'rb') as f:
        symmetric_key = f.read()
    with open(secret_key_path, 'rb') as f:
        secret_key_bytes = f.read()
    secret_key = serialization.load_pem_private_key(secret_key_bytes, password=None)
    symmetric_key = secret_key.decrypt(
        symmetric_key,
        padding=serialization.OAEP(
            mgf=serialization.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # 3.2. Расшифровать текст симметричным алгоритмом и сохранить по указанному пути.
    with open(encrypted_data_path, 'rb') as f:
        data = f.read()
    cipher = Cipher(algorithms.Camellia(symmetric_key), modes.CBC(os.urandom(16)))
    decryptor = cipher.decryptor()
    ct = decryptor.update(data) + decryptor.finalize()
    with open(decrypted_data_path, 'wb') as f:
        f.write(ct)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decrypt data')
    parser.add_argument('--encrypted_data_path', type=str, help='Path to encrypted data file')
    parser.add_argument('--secret_key_path', type=str, help='Path to secret key')
    parser.add_argument('--symmetric_key_path', type=str, help='Path to symmetric key')
    parser.add_argument('--decrypted_data_path', type=str, help='Path to decrypted data')
    args = parser.parse_args()

    decrypt_file(args.encrypted_data_path, args.secret_key_path, args.symmetric_key_path, args.decrypted_data_path)