#Elaborado por Felipe Bedoya, 2022.

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import argparse
import os
import time

# Parser de argumentos para pasar por parametro la ruta
parser = argparse.ArgumentParser(description='Google Drive Connector')
parser.add_argument('-i', '--id', help='ID del archivo a descargar', required=True)
parser.add_argument('-p', '--path', help='Ruta donde se descargara el archivo', required=True)

args = parser.parse_args()

# Inicializa el servidor de autenticacion gdrive
gauth = GoogleAuth()
gauth.CommandLineAuth()

# Acceso al drive
drive = GoogleDrive(gauth)


# Descarga del archivo
def recursive_download(folder_id, download_path):
    if download_path[-1] != '/':
        download_path += '/'
    folder = drive.CreateFile({'id': folder_id})
    os.mkdir(download_path + folder['title'])
    download_path = download_path + folder['title']
    file_list = drive.ListFile({'q': "'" + folder_id + "' in parents and trashed=false"}).GetList()
    for i, file1 in enumerate(sorted(file_list, key=lambda x: x['title']), start=1):
        print('Downloading {} from GDrive ({}/{})'.format(file1['title'], i, len(file_list)))
        if file1['mimeType'] == 'application/vnd.google-apps.folder':
            recursive_download(file1['id'], download_path)
        else:
            file1.GetContentFile(download_path + '/' + file1['title'])
            file1.Trash()


recursive_download(args.id, args.path)
