import telebot

# Замените на свой токен и ID чата
token = '6858417984:AAHHM_2Oj-KAvw3muNtpqb7kOE5HS_2FH-U'
chat_id = 1882056354

bot = telebot.TeleBot(token)

# Функция для отправки файла
def send_file(file_path):
 with open(file_path, 'rb') as f:
  bot.send_document(chat_id=chat_id, document=f)

# Отправляем файл
send_file('result.txt')
