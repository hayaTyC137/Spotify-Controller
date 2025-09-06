import threading
import time

import win32api
import win32con
import psutil
import win32gui
from win32con import VK_MEDIA_PLAY_PAUSE


def send_media_key(key_code):
    """Отправляет медиа-клавишу с минимальной задержкой"""
    try:
        win32api.keybd_event(key_code, 0, 0, 0)                 # Нажатие кнопки
        time.sleep(0.05)                                        # Минимальная задержка
        win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)  # Отжатие кнопки
    except Exception as e:
        print(f"Ошибка при отправке медиа-клавиши: {e}")


def find_spotify_window_callback(hwnd, windows_list):
    title = win32gui.GetWindowText(hwnd)
    if 'spotify' in title.lower():
        windows_list.append(hwnd)
    return True


def is_spotify_running():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'Spotify.exe':
            return True
    return False


def find_spotify_window():
    found_windows = []
    win32gui.EnumWindows(find_spotify_window_callback, found_windows)
    print(f"Найдено окон Spotify: {len(found_windows)}") # Можно будет убрать
    return found_windows


class SpotifyController:
    def __init__(self):
        # Константы клавиш
        self.VK_MEDIA_PLAY_PAUSE = 0xB3     #Кнопка стоп-пауза       #Кнопка стоп
        self.VK_MEDIA_NEXT_TRACK = 0xB0     #Кнопка след трек
        self.VK_MEDIA_PREV_TRACK = 0xB1     #Кнопка пред трек

        self.last_action_time = {}
        self.action_cooldown = 0.5  # Минимальная задержка между действиями
        self.action_lock = threading.Lock()

    def _can_execute_action(self, action_name):
        """Проверяет, можно ли выполнить действие (защита от спама)"""
        current_time = time.time()
        last_time = self.last_action_time.get(action_name, 0)

        if current_time - last_time >= self.action_cooldown:
            self.last_action_time[action_name] = current_time
            return True
        return False

    def _execute_action(self, action_name, media_key):
        """Базовый метод для выполнения медиа-действий"""
        with self.action_lock:
            if not self._can_execute_action(action_name):
                #print(f"Действие {action_name} заблокировано (слишком частые вызовы)")
                return

            try:
                if not is_spotify_running():
                    print("Spotify is not running")
                    return

                #print(f"Выполняется действие: {action_name}")

                # Отправляем медиа-клавишу без фокусировки на окне
                # Это более надежно и быстрее
                send_media_key(media_key)

            except Exception as e:
                print(f"Ошибка при выполнении {action_name}: {e}")

    def play_pause(self):
        """Воспроизведение/пауза"""
        self._execute_action("play_pause", self.VK_MEDIA_PLAY_PAUSE)

    def next_track(self):
        """Следующий трек"""
        self._execute_action("next_track", self.VK_MEDIA_NEXT_TRACK)

    def previous_track(self):
        """Предыдущий трек"""
        self._execute_action("previous_track", self.VK_MEDIA_PREV_TRACK)

    def stop(self):
        """Остановка воспроизведения (использует паузу, так как Spotify не имеет отдельной кнопки стоп)"""
        # В Spotify нет отдельной кнопки "стоп", используем паузу
        self.play_pause()

"""
TO-DO:

-Доделать функции стоп, плей и т.д - X
-Сделать логику нахождения и проверки Spotify на запущенность - X

"""

