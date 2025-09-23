
import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import argparse

from Logic import SpotifyControllLogic
from Logic.GlobalHotkeysLogic import GlobalHotkeys# Импорт класса
from Logic.TrayLogic import TrayManager
from Logic.AutoStartManagerLogic import AutostartManager
controller = SpotifyControllLogic.SpotifyController()

# Парсинг аргументов командной строки
parser = argparse.ArgumentParser()
parser.add_argument('--minimized', action='store_true', help='Запуск в свернутом виде')
args = parser.parse_args()

"Горячие клавиши"
play_key = "Не установлено"
next_key = "Не установлено"
prev_key = "Не установлено"


waiting = False
setting_for = None

# Нажатые кнопки
pressed_keys = set()



def set_key(action):
    global waiting, setting_for

    waiting = True
    setting_for = action
    if action == "play":
        play_label.config(text="Нажмите клавишу")
    elif action == "next":
        next_label.config(text="Нажмите клавишу")
    elif action == "prev":
        prev_label.config(text="Нажмите клавишу")


# Кнопку нажали
def on_key_press(event):
    pressed_keys.add(event.keysym)
    process_key_combo(event)

# Кнопку отпустили
def on_key_release(event):
    pressed_keys.discard(event.keysym)


def process_key_combo(event):
    # Не реагируем на отпускание Ctrl, Shift, Alt
    if event.keysym in ["Control_L", "Control_R", "Shift_L", "Shift_R", "Alt_L", "Alt_R"]:
        return  # Выходим из функции

    global play_key, next_key, prev_key, waiting, setting_for

    modifiers = []
    if any(key in pressed_keys for key in ["Shift_L", "Shift_R"]):
        modifiers.append("shift")
    if any(key in pressed_keys for key in ["Control_L", "Control_R"]):
        modifiers.append("ctrl")
    if any(key in pressed_keys for key in ["Alt_L", "Alt_R"]):
        modifiers.append("alt")

    main_key = event.keysym.lower()
    special_map = {
        "exclam": "1",
        "at": "2",
        "numbersign": "3",
        "dollar": "4",
        "percent": "5",
        "asciicircum": "6",
        "ampersand": "7",
        "asterisk": "8",
        "parenleft": "9",
        "parenright": "0",

    }

    if main_key in special_map:
        main_key = special_map[main_key]

    if modifiers:
        combo = "+".join(modifiers) + "+" + main_key
    else:
        combo = main_key

    if waiting:
        # Сохраняем клавишу
        if setting_for == "play":
            play_key = combo
            play_label.config(text=play_key)
        elif setting_for == "next":
            next_key = combo
            next_label.config(text=next_key)
        elif setting_for == "prev":
            prev_key = combo
            prev_label.config(text=prev_key)
        waiting = False
        updated_binds = {
            "play": play_key,
            "next": next_key,
            "prev": prev_key
        }
        globalHotkeys.update_binds(updated_binds)
        #print(f"Обновлены биды: {updated_binds}")


def reset_key(action):
    """Сброс горячей клавиши"""
    global play_key, next_key, prev_key

    if action == "play":
        play_key = "Не установлено"
        play_label.config(text=play_key)
    elif action == "next":
        next_key = "Не установлено"
        next_label.config(text=next_key)
    elif action == "prev":
        prev_key = "Не установлено"
        prev_label.config(text=prev_key)

    # Обновляем биды
    updated_binds = {
        "play": play_key,
        "next": next_key,
        "prev": prev_key
    }
    globalHotkeys.update_binds(updated_binds)

current_binds = {

    "play": play_key,
    "next": next_key,
    "prev": prev_key

}

globalHotkeys = GlobalHotkeys(controller, current_binds)
globalHotkeys.start_listener()
"Главный фрейм"
root = Tk()
root.geometry("370x270")
root.title("Spotify Controller")
root.resizable(False, False)

if args.minimized:
    root.withdraw()
else:
    pass

tray_manager = TrayManager(root)
tray_manager.setup_Tray()


try:
    # Для exe файла
    import sys
    import os

    if getattr(sys, 'frozen', False):
        # Если запущено из exe файла
        base_path = sys._MEIPASS
    else:
        # Если запущено из исходного кода
        base_path = os.path.dirname(__file__)

    icon_path = os.path.join(base_path, "SpotifyLogoController.png")
    iconOfTheController = tk.PhotoImage(file=icon_path)
    root.iconphoto(False, iconOfTheController)

except (tk.TclError, FileNotFoundError):
    print("Icon file not found, using default icon")

"Левый фрейм с управлением (просто кнопочки)"
main_Left_Frame = ttk.Frame(root, padding=8)
main_Left_Frame.pack(side="left", anchor="nw")

ttk.Label(main_Left_Frame, text="Управление", font=("Arial", 12, "bold")).pack(side="top")

button_play = ttk.Button(main_Left_Frame, text="Play", command=controller.play_pause)
button_play.pack(side="top", padx=10, pady=3, ipadx=10)


button_NextT_Track = ttk.Button(main_Left_Frame, text="Next Track", command=controller.next_track)
button_NextT_Track.pack(side="top", padx=10, pady=3, ipadx=10)

button_Previous_Track = ttk.Button(main_Left_Frame, text="Previous Track", command=controller.previous_track)
button_Previous_Track.pack(side="top", padx=10, pady=3, ipadx=10)

"Разделитель"
Separator = ttk.Separator(root, orient="vertical")
Separator.pack(fill="y", side="left", padx=8)

"Правый фрейм с биндами"
main_Right_Frame = ttk.Frame(root, padding=8)
main_Right_Frame.pack(side="right", anchor="nw")

ttk.Label(main_Right_Frame, text="Горячие клавиши", font=("Arial", 12, "bold")).pack(side="top")

# Play
play_frame = ttk.Frame(main_Right_Frame)
play_frame.pack(fill="x", pady=2)
ttk.Label(play_frame, text="Play:", width=5).pack(side="left")
play_label = ttk.Label(play_frame, text=play_key, width=13, relief="solid")
play_label.pack(side="left", padx=5)
ttk.Button(play_frame, text="Set", width=4, command=lambda: set_key("play")).pack(side="right")


# Next
next_frame = ttk.Frame(main_Right_Frame)
next_frame.pack(fill="x", pady=2)
ttk.Label(next_frame, text="Next:", width=5).pack(side="left")
next_label = ttk.Label(next_frame, text=next_key, width=13, relief="solid")
next_label.pack(side="left", padx=5)
ttk.Button(next_frame, text="Set", width=4, command=lambda: set_key("next")).pack(side="right")

# Previous
prev_frame = ttk.Frame(main_Right_Frame)
prev_frame.pack(fill="x", pady=2)
ttk.Label(prev_frame, text="Previous:", width=5).pack(side="left")
prev_label = ttk.Label(prev_frame, text=prev_key, width=13, relief="solid")
prev_label.pack(side="left", padx=5)
ttk.Button(prev_frame, text="Set", width=4, command=lambda: set_key("prev")).pack(side="right")

"Информация трека - в правом нижнем углу"
current_track = "Не выбрано"
current_artist = "Неизвестен"

# Разделитель перед информацией о треке
ttk.Separator(main_Right_Frame, orient="horizontal").pack(fill="x", pady=5)

track_label = ttk.Label(main_Right_Frame, text=f"Трек: {current_track}", font=("Arial", 10))
track_label.pack(pady=1)

artist_label = ttk.Label(main_Right_Frame, text=f"Исполнитель: {current_artist}", font=("Arial", 10))
artist_label.pack(pady=1)

#Статус
status_label = ttk.Label(main_Right_Frame, text="Готов к работе", font=("Arial", 9), foreground="green")
status_label.pack(pady=2)

autostart_manager = AutostartManager()
autostart_var = tk.BooleanVar()
autostart_var.set(autostart_manager.is_autostart_enabled())

def toggle_autostart():
    if autostart_var.get():
        if autostart_manager.enable_autostart():
            status_label.config(text="Автозапск включен", foreground="green")
        else:
            status_label.config(text="Ошибка включения автозапуска", foreground="red")
            autostart_var.set(False)
    else:
        if autostart_manager.disable_autostart():
            status_label.config(text="Автозапуск выключен", foreground="blue")
        else:
            status_label.config(text="Ошибка отключения автозапуска", foreground="red")
            autostart_var.set(True)

autostart_check = ttk.Checkbutton(main_Right_Frame, text="Автозапуск с Windows",
                                 variable=autostart_var,
                                 command=toggle_autostart)
autostart_check.pack(pady=2)


def on_closing():
    globalHotkeys.stop_listener()
    root.withdraw()

# Quit
quit_frame = ttk.Frame(main_Right_Frame)
quit_frame.pack(fill="x", pady=2)
ttk.Button(quit_frame, text="Quit", command=on_closing).pack()

tray_thread = threading.Thread(target=tray_manager.run_Tray, daemon=True)
tray_thread.start()

# Привязываем клавиши
root.bind('<KeyPress>', on_key_press)
root.bind('<KeyRelease>', on_key_release)
root.focus_set()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()