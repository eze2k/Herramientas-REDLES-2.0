import sys
import glob
import gnupg


def encrypt_files(file, output_file):
    gpg = gnupg.GPG(options={"--allow-weak-key-signatures": None})
    with open(file, "rb") as f:
        status = gpg.encrypt_file(
            f,
            recipients=["bases@sintys.gov.ar", "emore@desarrollosocial.gob.ar"],
            output=output_file,
        )
    if status.ok:
        print("OK")
    else:
        print(status.stderr)


# paquetes2 = glob.glob("*paquete2*")
# print(paquetes2)
# for file in paquetes2:
#     print(file)
#     encrypt_files(file, f"{file}.gpg")
