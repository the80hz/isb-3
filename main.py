import os
import json

from generate import generate_keys
from encrypt import encrypt_file
from decrypt import decrypt_file


if __name__ == '__main__':
    # read settings from 'settings.json'
    with open('settings.json') as json_file:
        json_data = json.load(json_file)
        initial_file = json_data['initial_file']
        encrypted_file = json_data['encrypted_file']
        decrypted_file = json_data['decrypted_file']
        symmetric_key = json_data['symmetric_key']
        public_key = json_data['public_key']
        secret_key = json_data['secret_key']

    # generate keys
    generate_keys(symmetric_key, public_key, secret_key)
    