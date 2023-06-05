import os
import json
import argparse

from generate import generate_keys
from encrypt import encrypt_file
from decrypt import decrypt_file
import settings


lyrics = ['О, горячий суп наварили!\nО, великий суп наварили!\n', 'Ешь суп,\nГорячий суп!\n']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt and decrypt file using hybrid crypto-system')
    parser.add_argument('--settings', type=str, help='settings path')
    parser.add_argument('-g', '--generate', action='store_true', help='generate keys')
    parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt file')
    parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt file')
    args = parser.parse_args()

    if not args.settings:
        parser.print_help()
        exit()

    try:
        with open(args.settings, 'r') as f:
            settings = json.load(f)
    except Exception as ex:
        print(ex)

    if args.generate:
        generate_keys(settings['symmetric_key'], settings['public_key'],
                      settings['private_key'])

    if args.encrypt:
        encrypt_file(settings['initial_file'], settings['private_key'],
                     settings['symmetric_key'], settings['encrypted_file'])

    if args.decrypt:
        decrypt_file(settings['encrypted_file'], settings['private_key'],
                     settings['symmetric_key'], settings['decrypted_file'])
