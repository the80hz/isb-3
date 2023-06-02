"""
2. Шифрование данных гибридной системой
Входные параметры:
1) путь к шифруемому текстовому файлу;
2) путь к закрытому ключу ассиметричного алгоритма;
3) путь к зашифрованному ключу симметричного алгоритма;
4) путь, по которому сохранить зашифрованный текстовый файл;

2.1. Расшифровать симметричный ключ.
2.2. Зашифровать текст симметричным алгоритмом и сохранить по указанному пути.
"""


import argparse
import os

from cryptography.hazmat.primitives import serialization, asymmetric, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_file(data_path: str, private_key_path: str, symmetric_key_path: str, encrypted_data_path: str) -> None:
    """
    2. Шифрование данных гибридной системой
    :param data_path:           путь к шифруемому текстовому файлу;
    :param private_key_path:    путь к закрытому ключу ассиметричного алгоритма;
    :param symmetric_key_path:  путь к зашифрованному ключу симметричного алгоритма;
    :param encrypted_data_path: путь, по которому сохранить зашифрованный текстовый файл;
    :return:
    """
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

    with open(data_path, 'rb') as f:
        data = f.read()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.Camellia(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(encrypted_data_path, 'wb') as f:
        f.write(iv)
        f.write(encrypted_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt data')
    parser.add_argument('--data_path', type=str,
                        default='file.txt', help='Path to data file')
    parser.add_argument('--private_key_path', type=str,
                        default='out/keys/private_key.pem', help='Path to public key')
    parser.add_argument('--symmetric_key_path', type=str,
                        default='out/keys/symmetric_key.txt', help='Path to symmetric key')
    parser.add_argument('--encrypted_data_path', type=str,
                        default='out/encrypted_file.txt', help='Path to encrypted data file')
    args = parser.parse_args()

    encrypt_file(args.data_path, args.private_key_path, args.symmetric_key_path, args.encrypted_data_path)
