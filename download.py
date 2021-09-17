import os
import sys
import json
import uuid
import requests
from zipfile import ZipFile

os.system('color')
ROOT = os.path.dirname(os.path.realpath(__file__))
MANIFEST_URL = 'https://launchermeta.mojang.com/mc/game/version_manifest_v2.json'
MANIFEST = json.loads(requests.get(MANIFEST_URL).text)

class Font:
    RESET = '\033[0m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    BRIGHT_RED = '\033[0;91m'
    BRIGHT_GREEN = '\033[0;92m'
    BRIGHT_YELLOW = '\033[0;93m'
    BRIGHT_BLUE = '\033[0;94m'
    
    @staticmethod
    def red(message: str) -> str: return f'{Font.RED}{message}{Font.RESET}'
    
    @staticmethod
    def green(message: str) -> str: return f'{Font.GREEN}{message}{Font.RESET}'

    @staticmethod
    def yellow(message: str) -> str: return f'{Font.YELLOW}{message}{Font.RESET}'

    @staticmethod
    def blue(message: str) -> str: return f'{Font.BLUE}{message}{Font.RESET}'

    @staticmethod
    def bred(message: str) -> str: return f'{Font.BRIGHT_RED}{message}{Font.RESET}'
    
    @staticmethod
    def bgreen(message: str) -> str: return f'{Font.BRIGHT_GREEN}{message}{Font.RESET}'

    @staticmethod
    def byellow(message: str) -> str: return f'{Font.BRIGHT_YELLOW}{message}{Font.RESET}'

    @staticmethod
    def bblue(message: str) -> str: return f'{Font.BRIGHT_BLUE}{message}{Font.RESET}'

def download(url: str, path: str, filename=None):
    if filename is None:
        filename = url.split('/')[-1]
    os.makedirs(path, exist_ok = True)
    if not os.path.exists(f'{path}{url.split("/")[-1]}'):
        print('Загрузка: {} '.format(Font.byellow(filename)).ljust(60, '.'), end='')
        file = requests.get(url, allow_redirects = True)
        open(f'{path}{url.split("/")[-1]}', 'wb').write(file.content)
        print(Font.bgreen('OK'))

def unpack(filepath: str):
    with ZipFile(filepath, 'r') as zipObj:
        for filename in zipObj.namelist():
            if filename.endswith('.dll'):
                print(' Распаковка: {} '.format(Font.byellow(filename)).ljust(60, '.'), end='')
                zipObj.extract(filename, os.path.dirname(filepath))
                print(Font.bgreen('OK'))
    os.remove(filepath)

def client_download(version: str):
    os.system('cls||clear')
    print('Выбрана версия: {}'.format(Font.bgreen(version)))
    for client in MANIFEST['versions']:
        if version == client['id']:
            print(Font.bgreen('Версия найдена!'))
            data = json.loads(requests.get(client['url']).text)
            clientRoot = f"{ROOT}/client/{client['id']}"
            
            # Загрузка основного JAR-файла клиента
            clientInfo = data['downloads']['client']
            filename = clientInfo['url'].split('/')[-1]
            download(clientInfo['url'], f'{clientRoot}/libraries/')
            
            # Загрузка библиотек
            for library in data['libraries']:
                if 'rules' in library:
                    if library['rules'][0]['action'] == 'allow' and 'os' in library['rules'][0]:
                        continue;
                if 'natives' in library:
                    if 'windows' in library['natives']:
                        native = library['downloads']['classifiers']['natives-windows']
                        download(native['url'], f'{clientRoot}/libraries/natives/', library['name'])
                        unpack(f'{clientRoot}/libraries/natives/{native["url"].split("/")[-1]}')
                else:
                    file = library['downloads']['artifact']
                    download(file['url'], f'{clientRoot}/libraries/')
            
            # Загрузка ассетов
            download(data['assetIndex']['url'], f'{clientRoot}/assets/indexes/')
            assetIndex = json.loads(requests.get(data['assetIndex']['url']).text)
            
            for object in assetIndex['objects']:
                fileHash = assetIndex['objects'][object]['hash']
                download(f'http://resources.download.minecraft.net/{fileHash[:2]}/{fileHash}', f'{clientRoot}/assets/objects/{fileHash[:2]}/', object.split('/')[-1])

            # Создание BAT-файла
            username = input('Введите имя вашего персонажа (по умолчанию: {}) : '.format(Font.byellow('Steve'))) or 'Steve'
            with open(f"{ROOT}/client/{client['id']}/client-run-{username}.bat", 'a') as batFile:
                batFile.write(f'SET username={username}\n')
                batFile.write(f'SET uuid={uuid.uuid4().hex}\n')
                batFile.write(f'SET accessToken={uuid.uuid4().hex}\n')
                batFile.write(f'CLS\n')
                batFile.write(f'java -Djava.library.path=./libraries/natives/ -cp "./libraries/*" {data["mainClass"]} --username %username% --version {data["id"]} --gameDir . --assetsDir ./assets --assetIndex {data["assets"]} --uuid %uuid% --accessToken %accessToken% --userType mojang\n')
                batFile.write(f'PAUSE\n')
                batFile.write(f'RMDIR /s /q saves\n')
                batFile.write(f'RMDIR /s /q resourcepacks\n')
                batFile.write(f'RMDIR /s /q logs\n')
                batFile.write(f'RMDIR /s /q config\n')
                batFile.write(f'RM options.txt\n')
        
            print(f"Готово! Для запуска используйте: {ROOT}/client/{client['id']}/client-run-{username}.bat")
            os.startfile(f'{ROOT}/client/{client["id"]}/')
            
def main(args):
    print(f'Введите команду из списка:')
    print(f'')
    print('{} - загрузить последний релиз [{}]'.format(Font.byellow('release'), Font.bgreen(MANIFEST['latest']['release'])))
    print('{} - загрузить последний снапшот [{}]'.format(Font.byellow('snapshot'), Font.bgreen(MANIFEST['latest']['snapshot'])))
    print('{} - выбрать из списка старых релизов'.format(Font.byellow('old')))
    print(f'')
    command = input('Команда (по умолчанию: {}) : '.format(Font.byellow('release'))) or 'release'
    
    if command == 'release':
        command = MANIFEST['latest']['release']
    if command == 'snapshot':
        command = MANIFEST['latest']['snapshot']
    if command == 'old':
        clients = []
        for client in MANIFEST['versions']:
            if client['type'] == 'release':
                clients.append('[{}]'.format(Font.byellow(client['id'].center(10))))
        os.system('cls||clear')
        print('Доступны следующие версии для загрузки:')
        for i in range(len(clients) // 6):
            print(' '.join(clients[:6]))
            del clients[0:6]
        command = input('Команда (по умолчанию: {}) : '.format(Font.byellow(MANIFEST['latest']['release']))) or MANIFEST['latest']['release']
    client_download(command)    


if __name__ == "__main__":
    main(sys.argv)