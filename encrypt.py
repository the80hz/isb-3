import argparse
import os
import logging

from cryptography.hazmat.primitives import serialization, asymmetric, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logging.basicConfig(level=logging.INFO)


def encrypt_file(data_path: str, private_key_path: str, symmetric_key_path: str, encrypted_data_path: str) -> None:
    """
    2. Шифрование данных гибридной системой
    :param data_path:           путь к шифруемому текстовому файлу;
    :param private_key_path:    путь к закрытому ключу ассиметричного алгоритма;
    :param symmetric_key_path:  путь к зашифрованному ключу симметричного алгоритма;
    :param encrypted_data_path: путь, по которому сохранить зашифрованный текстовый файл;
    :return:
    """
    logging.info('Starting encryption process...')
    try:
        with open(symmetric_key_path, 'rb') as f:
            symmetric_key = f.read()
        logging.info('Symmetric key loaded.')
    except FileNotFoundError:
        logging.error('Symmetric key not found')
        return

    try:
        with open(private_key_path, 'rb') as f:
            private_key_bytes = f.read()
        logging.info('Private key loaded.')
    except FileNotFoundError:
        logging.error('Private key not found')
        return

    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    symmetric_key = private_key.decrypt(
        symmetric_key,
        padding=asymmetric.padding.OAEP(
            mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    logging.info('Symmetric key decrypted.')

    try:
        with open(data_path, 'rb') as f:
            data = f.read()
        logging.info('Data file loaded.')
    except FileNotFoundError:
        logging.error('Data file not found')
        return

    iv = os.urandom(16)
    cipher = Cipher(algorithms.Camellia(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    logging.info('Data encrypted.')

    try:
        with open(encrypted_data_path, 'wb') as f:
            f.write(iv)
            f.write(encrypted_data)
        logging.info('Encrypted data saved.')
    except FileNotFoundError:
        os.makedirs(os.path.dirname(encrypted_data_path))
        with open(encrypted_data_path, 'wb') as f:
            f.write(iv)
            f.write(encrypted_data)
        logging.info('Encrypted data saved.')


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
