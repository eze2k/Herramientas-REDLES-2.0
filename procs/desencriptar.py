import sys
import gnupg


def decrypt_file(file, passphrase, output_file):
    gpg = gnupg.GPG()
    with open(file, "rb") as f:
        status = gpg.decrypt_file(f, passphrase=passphrase, output=output_file)

    if status.ok:
        print("OK")
    else:
        print(status.stderr)
