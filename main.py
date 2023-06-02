import os
import json

from generate import generate_keys
from encrypt import encrypt_file
from decrypt import decrypt_file
import settings


lyrics = ['О, горячий суп наварили!\nО, великий суп наварили!\n', 'Ешь суп,\nГорячий суп!\n']

if __name__ == '__main__':
    if not os.path.exists('settings.json'):
        settings.get_settings()
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    if not os.path.exists(settings['initial_file']):
        try:
            with open(settings['initial_file'], 'w') as f:
                f.write('')
        except FileNotFoundError:
            print('Something went wrong')
    if not os.path.exists(settings['output_folder']):
        try:
            os.makedirs(settings['output_folder'])
        except FileNotFoundError:
            print('Something went wrong')

    if not os.path.exists(settings['output_keys_folder']):
        try:
            os.makedirs(settings['output_keys_folder'])
        except FileNotFoundError:
            print('Something went wrong')

    if os.path.getsize(settings['initial_file']) == 0:
        try:
            with open(settings['initial_file'], 'w', encoding='utf-8') as f:
                f.write(f'{lyrics[0] * 4}{lyrics[1] * 4}{lyrics[0] * 2}{lyrics[1] * 8}{lyrics[0] * 2}{lyrics[1] * 4}')
        except FileNotFoundError:
            print('Something went wrong')

    generate_keys(settings['symmetric_key'], settings['public_key'],
                  settings['private_key'])

    encrypt_file(settings['initial_file'], settings['private_key'],
                 settings['symmetric_key'], settings['encrypted_file'])

    decrypt_file(settings['encrypted_file'], settings['private_key'],
                 settings['symmetric_key'], settings['decrypted_file'])
