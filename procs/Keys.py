import subprocess


def run():
    print("Recordar instalar GNUP4WIN antes de correr esto.")
    keys = [
        "keys/sintys pub.asc",
        "keys/eze key.asc",
        "keys/eze key secret.asc",
        "sintys pub.asc",
    ]
    passphrases = ["PasswordFalso", "PasswordFalso", "PasswordFalso", "PasswordFalso"]

    for key_file, passphrase in zip(keys, passphrases):
        # Import the key
        subprocess.run(
            ["gpg", "--batch", "--import", key_file], input=passphrase, text=True
        )

    # List keys to get the fingerprints
    result = subprocess.run(
        ["gpg", "--list-keys", "--with-colons"], capture_output=True, text=True
    )
    output = result.stdout.splitlines()
    fingerprints = [line.split(":")[4] for line in output if line.startswith("pub")]

    # Sign the keys with ultimate trust
    for fingerprint in fingerprints:
        subprocess.run(
            ["gpg", "--batch", "--command-fd", "0", "--edit-key", fingerprint],
            input="trust\n5\ny\nsave\n",
            text=True,
        )

    print("Llaves de encriptacion instaladas, presione [ENTER] para salir.")
    input("")
