# minecraft-downloader
Это скрипт для загрузки игры Minecraft

## Описание
Скрипт автоматически анализирует **version_manifest_v2.json** с сайта Mojang и скачивает полностью все нужные библиотеки и ресурсы. Версию игры можно менять, включая самую свежую предварительную. В конце загрузки будет создан BAT-файл **client-run-[имя_игрока].bat** для запуска игры с нужным именем игрока. **UUID** и **AccessToken** генерируются случайные, но могут быть изменены в BAT-файле вручную.

## Как пользоваться
1. Запустить скрипт и выбрать из 3-х возможных вариантов: **release**, **snapshot** или **old**

<p align="center"><img src="https://github.com/IVZaytsev/minecraft-builder/blob/main/readme/downloader1.png?raw=true" alt="Выбор требуемого режима"/></p>

2. Если выбран **old**, то будет предложено ввести номер версии игры:

<p align="center"><img src="https://github.com/IVZaytsev/minecraft-builder/blob/main/readme/downloader2.png?raw=true" alt="Выбор версии для скачивания"/></p>

3. После выбора начнётся загрузка файлов игры, дождитесь её окончания (процесс может занимать до 10 минут).

<p align="center"><img src="https://github.com/IVZaytsev/minecraft-builder/blob/main/readme/downloader3.png?raw=true" alt="Загрузка ресурсов"/></p>

4. По окончанию загрузки будет предложено ввести **имя игрока** для создания запускающего игру BAT-файла

<p align="center"><img src="https://github.com/IVZaytsev/minecraft-builder/blob/main/readme/downloader4.png?raw=true" alt="Завершение работы"/></p>

5. После создания BAT-файла будет открыта папка, в которой находится игра и BAT-файл для её запуска. Клиент полностью готов и может быть скопирован куда-угодно.

## Особенности
1. Структура клиента отличается от оригинальной для наглядности и уменьшения количества каталогов
2. Новые версии Minecraft (>1.17) требуют наличия Java 16. Имейте это ввиду: если при запуске вы видите сообщение типа **Unsupported class file major version 60**, значит вам необходимо скачать нужную Java.