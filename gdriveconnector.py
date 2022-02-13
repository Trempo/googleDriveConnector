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

#Credenciales guardadas
gauth.LoadCredentialsFile("creds.json")

if gauth.credentials is None:
    # Si no hay credenciales, se autentica
    gauth.CommandLineAuth()
elif gauth.access_token_expired:
    # Si las credenciales ya existen, pero estan expiradas, se autentica
    gauth.Refresh()
else:
    # Si las credenciales ya existen y no estan expiradas, se usan
    gauth.Authorize()


# Acceso al drive
drive = GoogleDrive(gauth)

start_path = args.path
if start_path[-1] != '/':
    start_path += '/'

# Descarga del archivo
def recursive_download(folder_id, download_path):
    print(download_path)
    if download_path[-1] != '/':
        download_path += '/'
    folder = drive.CreateFile({'id': folder_id})
    if start_path != download_path:
        os.mkdir(download_path)
    file_list = drive.ListFile({'q': "'" + folder_id + "' in parents and trashed=false"}).GetList()
    for i, file1 in enumerate(sorted(file_list, key=lambda x: x['title']), start=1):
        print('Downloading {} from GDrive ({}/{})'.format(file1['title'], i, len(file_list)))
        if file1['mimeType'] == 'application/vnd.google-apps.folder':
            download_path += file1['title'] + '/'
            recursive_download(file1['id'], download_path)
        else:
            file1.GetContentFile(download_path + '/' + file1['title'])
            file1.Trash()


recursive_download(args.id, args.path)
