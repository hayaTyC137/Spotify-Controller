import sys
import os
import winreg
import platform
from winreg import HKEY_CURRENT_USER


def get_exe_path():
    """Получаем путь к файлу"""
    if getattr(sys, "frozen", False):
        #Если запускаем exe файл
        exe_path = os.path.realpath(sys.argv[0])
        # print(f"Реальный путь к exe: {exe_path}")  # ОТЛАДКА
        return f'"{exe_path}"'
    else:
        #Если запускаем из исходного кода (то-есть .py)
        path = f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'
        # print(f"Путь разработки: {path}")  # ОТЛАДКА
        return path


class AutostartManager:
    def __init__(self, app_name = "Spotify Controller"):
        self.app_name = app_name
        self.registry_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

    def is_autostart_enabled(self):
        """Проверяем запущен ли автозапуск"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key, 0, winreg.KEY_READ ) as key:
                value, _ = winreg.QueryValueEx(key, self.app_name)
                return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    def enable_autostart(self):
        """Включает автозагрузку приложения"""
        exe_path = get_exe_path()
        try:
            if not exe_path.endswith('--minimized'):
                exe_path += ' --minimized'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key, 0, winreg.KEY_WRITE ) as key:
                winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, exe_path)
            return True
        except Exception as e:
            # print(f"Ошибка включения автозапуска + {e}")
            return False

    def disable_autostart(self):
        exe_path = get_exe_path()
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key, 0, winreg.KEY_WRITE ) as key:
                winreg.DeleteValue(key, self.app_name)
            return True
        except Exception:
            # print(f"Ошибка выключения автозапуска + {Exception}")
            return False