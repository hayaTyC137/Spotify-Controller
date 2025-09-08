import pystray
from pystray import MenuItem, Menu
from PIL import Image

import SpotifyControllLogic

def create_Tray_icon():
    return Image.open("SpotifyLogoController.png")


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



