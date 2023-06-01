import json

settings = {
  "initial_file": "file.txt",
  "encrypted_file": "out/encrypted_file.txt",
  "decrypted_file": "out/decrypted_file.txt",
  "symmetric_key": "out/keys/symmetric_key.txt",
  "public_key": "out/keys/public_key.pem",
  "secret_key": "out/keys/secret_key.pem"
}

if __name__ == '__main__':
    with open('settings.json', 'w') as fp:
        json.dump(settings, fp)
