@bot.message_handler(commands=['add_to_startup'])
def add_to_startup(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите путь к файлу:")
    bot.register_next_step_handler(message, add_file_to_startup)

def add_file_to_startup(message):
    chat_id = message.chat.id
    file_path = message.text.strip()
    if file_path:
        if os.path.exists(file_path):
            username = os.getlogin()
            startup_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
            file_name = os.path.basename(file_path)
            destination = os.path.join(startup_path, file_name)
            shutil.copy2(file_path, destination)
            bot.send_message(chat_id, "Файл успешно добавлен в автозагрузку.")
        else:
            bot.send_message(chat_id, "Указанный файл не существует.")
    else:
        bot.send_message(chat_id, "Вы не ввели путь к файлу.")

@bot.message_handler(commands=['remove_from_startup'])
def remove_from_startup(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите путь к файлу в автозагрузке:")
    bot.register_next_step_handler(message, remove_file_from_startup)

def remove_file_from_startup(message):
    chat_id = message.chat.id
    file_path = message.text.strip()
    if file_path:
        if os.path.exists(file_path):
            username = os.getlogin()
            startup_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
            file_name = os.path.basename(file_path)
            file_to_remove = os.path.join(startup_path, file_name)
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
                bot.send_message(chat_id, "Файл успешно удален из автозагрузки.")
            else:
                bot.send_message(chat_id, "Указанный файл не найден в автозагрузке.")
        else:
            bot.send_message(chat_id, "Указанный файл не существует.")
    else:
        bot.send_message(chat_id, "Вы не ввели путь к файлу.")
