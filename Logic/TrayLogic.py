import os
import sys

import pystray
from pystray import MenuItem, Menu
from PIL import Image

import SpotifyControllLogic


def create_Tray_icon():
    try:
        # Определяем базовый путь для ресурсов
        if getattr(sys, 'frozen', False):
            # Если запущено из exe файла
            base_path = sys._MEIPASS
        else:
            # Если запущено из исходного кода
            base_path = os.path.dirname(__file__)

        icon_path = os.path.join(base_path, "SpotifyLogoController.png")
        return Image.open(icon_path)

    except (FileNotFoundError, Exception) as e:
        print(f"Icon file not found: {e}")
        # Создаем простую иконку по умолчанию, если файл не найден
        return Image.new('RGB', (64, 64), color='green')


def quit_tray(icon, item):
    icon.stop()


class TrayManager:
    def __init__(self, root_window=None):
        self.tray_icon = None
        self.controller = SpotifyControllLogic.SpotifyController()
        self.root_window = root_window

    def show_window(self, icon, item):
        if self.root_window:
            self.root_window.deiconify()
            self.root_window.lift()

    def quit_application(self, icon, item):
        icon.stop()
        if self.root_window:
            self.root_window.destroy()


    def setup_Tray(self):
        tray_icon = create_Tray_icon()

        menu = Menu(
            MenuItem("Показать окно", self.show_window, default=True),
            Menu.SEPARATOR,
            MenuItem('Quit', self.quit_application)
        )

        self.tray_icon = pystray.Icon("Spotify Tray Icon", tray_icon, "Spotify Controller", menu)

    def run_Tray(self):
        if self.tray_icon:
            self.tray_icon.run()