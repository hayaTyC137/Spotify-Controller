import time

from pynput import keyboard


special_map = {
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
}

def key_to_string(key):
    try:
        if hasattr(key, "char") and key.char:
            ch = key.char.lower()
            return special_map.get(ch, ch)
        else:
            # Для специальных клавиш убираем префикс Key.
            key_name = str(key).replace('Key.', '').lower()
            # Преобразуем некоторые специальные случаи
            if key_name in ['ctrl_l', 'ctrl_r']:
                return 'ctrl'
            elif key_name in ['shift_l', 'shift_r']:
                return 'shift'
            elif key_name in ['alt_l', 'alt_r']:
                return 'alt'
            return key_name
    except:
        return None


class GlobalHotkeys(object):
    def __init__(self, controller, current_binds):
        self.controller = controller
        self.current_binds = current_binds
        self.pressed_keys = set()
        self.listener = None

        self.processed_combinations = set()
        self.last_action_time = {}
        self.action_cooldown = 0.3

    def _get_current_combination(self):
        modifiers = []
        main_keys = []

        for key in self.pressed_keys:
            # Проверяем различные варианты модификаторов
            if (key == keyboard.Key.ctrl or
                    key == keyboard.Key.ctrl_l or
                    key == keyboard.Key.ctrl_r):
                if "ctrl" not in modifiers:
                    modifiers.append("ctrl")
            elif (key == keyboard.Key.shift or
                  key == keyboard.Key.shift_l or
                  key == keyboard.Key.shift_r):
                if "shift" not in modifiers:
                    modifiers.append("shift")
            elif (key == keyboard.Key.alt or
                  key == keyboard.Key.alt_l or
                  key == keyboard.Key.alt_r):
                if "alt" not in modifiers:
                    modifiers.append("alt")
            else:
                key_str = key_to_string(key)
                if key_str and key_str not in main_keys:
                    main_keys.append(key_str)

        # Берем только первую основную клавишу для комбинации
        main_key = main_keys[0] if main_keys else None

        if modifiers and main_key:
            # Сортируем модификаторы для консистентности
            combination = "+".join(sorted(modifiers)) + "+" + main_key
        elif main_key:
            combination = main_key
        else:
            combination = None

        return combination

    def _can_execute_action(self, action):
        """Проверяет, можно ли выполнить действие (защита от спама)"""
        current_time = time.time()
        last_time = self.last_action_time.get(action, 0)

        if current_time - last_time >= self.action_cooldown:
            self.last_action_time[action] = current_time
            return True
        return False

    def on_key_press(self, key):
        self.pressed_keys.add(key)
        current_combo = self._get_current_combination()

        if current_combo:
            # Проверяем, была ли уже обработана эта комбинация
            if current_combo not in self.processed_combinations:
                self.processed_combinations.add(current_combo)

                # Перебираем все биды пользователя
                for action, user_bind in self.current_binds.items():
                    if (user_bind and
                            user_bind != "Не установлено" and
                            current_combo == user_bind and
                            self._can_execute_action(action)):

                        #print(f"Выполняется действие: {action} для комбинации: {current_combo}")

                        # Вызываем соответствующее действие
                        try:
                            if action == "play":
                                self.controller.play_pause()
                            elif action == "next":
                                self.controller.next_track()
                            elif action == "prev":
                                self.controller.previous_track()
                        except Exception as e:
                            print(f"Ошибка при выполнении действия {action}: {e}")

                        break  # Выходим из цикла после первого совпадения

    def on_key_release(self, key):
        self.pressed_keys.discard(key)

        # Очищаем обработанные комбинации при отпускании любой клавиши
        # Это позволяет повторно использовать ту же комбинацию
        current_combo = self._get_current_combination()
        if current_combo:
            # Если текущая комбинация изменилась, очищаем processed_combinations
            pass
        else:
            # Если больше нет активных комбинаций, очищаем все
            self.processed_combinations.clear()

    def start_listener(self):
        if self.listener is None or not self.listener.running:
            self.listener = keyboard.Listener(
                on_press=self.on_key_press,
                on_release=self.on_key_release
            )
            self.listener.start()

    def stop_listener(self):
        if self.listener and self.listener.running:
            self.listener.stop()
            self.listener = None

    def update_binds(self, new_binds):
        """Метод для безопасного обновления биндов"""
        self.current_binds = new_binds.copy()
        self.processed_combinations.clear()