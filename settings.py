import json

settings = {
    "output_folder": "out/",
    "output_keys_folder": "out/keys/",
    "initial_file": "file.txt",
    "encrypted_file": "out/encrypted_file.txt",
    "decrypted_file": "out/decrypted_file.txt",
    "symmetric_key": "out/keys/symmetric_key.txt",
    "public_key": "out/keys/public_key.pem",
    "private_key": "out/keys/private_key.pem"
}


def get_settings() -> None:
    with open('settings.json', 'w') as fp:
        json.dump(settings, fp)


if __name__ == '__main__':
    get_settings()
