import os
import subprocess

def install_packages_from_directory(directory="."):
    # Obtener la lista de archivos en el directorio actual
    files = os.listdir(directory)

    # Iterar sobre los archivos y ejecutar pip install para cada uno
    for file in files:
        if file.endswith('.whl') or file.endswith('.tar.gz'):
            file_path = os.path.join(directory, file)
            subprocess.run(['pip', 'install', '--no-index', '--find-links=' + directory, '--no-cache-dir', file_path])

if __name__ == "__main__":
    # Instala los paquetes desde el directorio actual
    install_packages_from_directory()
