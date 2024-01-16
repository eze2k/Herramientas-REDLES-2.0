import sys
import glob
import gnupg
import os
import shutil
import glob
from procs.console import console
import tarfile
import zipfile


def decrypt_file(file):
    gpg = gnupg.GPG()
    filename = os.path.splitext(file)[0]
    with open(file, "rb") as f:
        status = gpg.decrypt_file(
            f, passphrase="PasswordFalso", output=f"out/{filename}"
        )

    if status.ok:
        print("OK")
        # shutil.move(file, f"in/{filename}")
    else:
        print(status.stderr)


def encrypt_files(file):
    gpg = gnupg.GPG(options={"--allow-weak-key-signatures": None})
    with open(file, "rb") as f:
        status = gpg.encrypt_file(
            f,
            recipients=["bases@sintys.gov.ar", "emore@desarrollosocial.gob.ar"],
            output=f"out/{file}.gpg",
        )
    if status.ok:
        print("OK")
        shutil.move(file, f"in/{file}")
    else:
        print(status.stderr)


def runEncrypt():
    paquetes2 = (
        glob.glob("*Paquete2*.txt")
        + glob.glob("*Hijos*.txt")
        + glob.glob("*Efectores*.txt")
    )
    print(paquetes2)
    for file in paquetes2:
        print(file)
        encrypt_files(file)
    console.log("Se efectuo la limpieza/combinacion con exito.")
    input("[Presione ENTER para continuar.]")


def runDecrypt():
    paquetes2 = glob.glob("*.pgp")
    print(paquetes2)
    file_extensions = [".txt", ".csv"]
    for file in paquetes2:
        print(file)
        tar = os.path.splitext(file)[0]
        print(tar)
        decrypt_file(file)
        # Extract the files from the source archive to the temporary folder
        with tarfile.open(f"out/{tar}", "r:gz") as tar:
            # Get a list of all the members (files/folders) in the tar file
            members = tar.getmembers()

            # Create a new zip file to store the extracted archives
            with zipfile.ZipFile(
                f"out/{file}_resultado.zip", "w", compression=zipfile.ZIP_DEFLATED
            ) as zip:
                # Loop through all members in the tar file
                for member in members:
                    # Check if the member is a file and located in the desired subfolder
                    if member.isfile() and "expediente/resultado" in member.name:
                        # Extract the file to a temporary location
                        tar.extract(member, path="temp/")

                        # Add the extracted file to the zip file without the subfolder structure
                        zip.write(
                            os.path.join("temp", member.name),
                            arcname=os.path.basename(member.name),
                        )

                        # Delete the extracted file from the temporary location
                        os.remove(os.path.join("temp", member.name))
                        shutil.rmtree("temp/")

    console.log("Se efectuo la limpieza/combinacion con exito.")
    input("[Presione ENTER para continuar.]")
