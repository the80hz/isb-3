import argparse
import logging
import os

from cryptography.hazmat.primitives import serialization, asymmetric, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Настраиваем базовые параметры логирования
logging.basicConfig(level=logging.INFO)


def decrypt_file(encrypted_data_path: str, private_key_path: str,
                 symmetric_key_path: str, decrypted_data_path: str) -> None:
    """
    3. Дешифрование данных гибридной системой
    Входные параметры:
    :param encrypted_data_path:     путь к зашифрованному текстовому файлу;
    :param private_key_path:        путь к закрытому ключу ассиметричного алгоритма;
    :param symmetric_key_path:      путь к зашифрованному ключу симметричного алгоритма;
    :param decrypted_data_path:     путь, по которому сохранить расшифрованный текстовый файл.
    :return:
    """
    logging.info('Starting decryption process...')
    try:
        with open(symmetric_key_path, 'rb') as f:
            symmetric_key = f.read()
        logging.info('Symmetric key loaded.')
    except FileNotFoundError:
        logging.error('Symmetric key file not found')
        return

    try:
        with open(private_key_path, 'rb') as f:
            private_key_bytes = f.read()
        logging.info('Private key loaded.')
    except FileNotFoundError:
        logging.error('Private key file not found')
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
        with open(encrypted_data_path, 'rb') as f:
            encrypted_data = f.read()
        logging.info('Encrypted data file loaded.')
    except FileNotFoundError:
        logging.error('Encrypted data file not found')
        return

    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.Camellia(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    logging.info('Data decrypted.')

    try:
        with open(decrypted_data_path, 'wb') as f:
            f.write(decrypted_data)
        logging.info('Decrypted data saved.')
    except FileNotFoundError:
        os.makedirs(os.path.dirname(decrypted_data_path))
        with open(decrypted_data_path, 'wb') as f:
            f.write(decrypted_data)
        logging.info('Decrypted data saved.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decrypt data')
    parser.add_argument('--encrypted_data_path', type=str,
                        default='out/encrypted_file.txt', help='Path to encrypted data file')
    parser.add_argument('--private_key_path', type=str,
                        default='out/keys/private_key.pem', help='Path to public key')
    parser.add_argument('--symmetric_key_path', type=str,
                        default='out/keys/symmetric_key.txt', help='Path to symmetric key')
    parser.add_argument('--decrypted_data_path', type=str,
                        default='out/decrypted_file.txt', help='Path to decrypted data')
    args = parser.parse_args()

    decrypt_file(args.encrypted_data_path, args.private_key_path, args.symmetric_key_path, args.decrypted_data_path)
