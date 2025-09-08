# Версия V1.0 💾
Приложение SpotifyController, работает без API подключения, полностью оффлайн приложение написанное на python. Версия пока сыровата, есть несколько багов, которые будут фиксится позже. Примером служит не подключенный модуль по получению информации об авторе треков и самого трека. Все приложение написано, с использованием нейросети для получении информации как что фиксить. Однако вся логика писалась с попыткой использования принципа ООП. Любое изменение или модификация приложения в ваших руках, я ток рад если кто-то захочет переделать, программа полностью в руках комьюнити.

# Технологии ⚙️
- Python 3.13

# Библиотеки 📝
- Стадартная библиотека python
- win32api
- win32con
- win32gui
- pynnput
- psutil
- pywin32
- tkinter
- time
- threading
- sys и os

# Как выглядит
- Для запуска программы, требуется зайти в папку dist, там находиться файл SpotifyController.exe
<img width="502" height="360" alt="image" src="https://github.com/user-attachments/assets/8d67b405-3e64-45eb-89ce-4ea5bbcb8989" />
- Можете сами скомпилировать exe файл

# Как скомпилировать exe файл
- В терминале пропишите путь к директории файле `cd путь `

- Пропишите команду `pyinstaller SpotifyController.spec`

- После введите команду для компилирования

`pyinstaller --onefile --noconsole --name "SpotifyController" --add-data "SpotifyLogoController.png;." --hidden-import psutil --hidden-import psutil._psutil_windows --hidden-import win32api --hidden-import win32con --hidden-import win32gui --hidden-import pynput.keyboard._win32 GUI.py`



# Version V1.0 💾
The SpotifyController application works without connecting to the API and is a completely standalone application written in Python. The version is still under development and contains several bugs that will be fixed later. An example is the disabled module for obtaining information about the author of the tracks and the track itself. The entire application is written using a neural network to obtain information about what needs to be fixed. However, all the logic was written with an attempt to use the OOP principle. Any changes or modifications to the application are in your hands, and I would be happy if anyone wanted to rework it; the program is completely in the hands of the community.

# Technologies ⚙️
- Python 3.13

# Libraries 📝
- Standard Python library
- win32api
- win32con
- win32gui
- pynnput
- psutil
- pywin32
- tkinter
- time
- threading
- sys and os

# How to compile an exe file

- In the terminal, enter the path to the file directory `cd path`

- Enter the command `pyinstaller SpotifyController.spec`

- Then enter the command to compile

`pyinstaller --onefile --noconsole --name “SpotifyController” --add-data “SpotifyLogoController.png;.” --hidden-import psutil --hidden-import psutil._psutil_windows --hidden-import win32api --hidden-import win32con --hidden-import win32gui --hidden-import pynput.keyboard._win32 GUI.py`

