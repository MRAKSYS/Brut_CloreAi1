    global code_to_execute
    chat_id = message.chat.id
    if message.text.startswith('/addcode'):
        code = message.text.replace('/addcode', '').strip()
        code_to_execute += code + '\n'  # Добавляем новый код к действующему с переносом строки
        bot.send_message(chat_id, 'Код успешно добавлен для последующего выполнения.')
    elif message.text.startswith('/runcode'):
        if not code_to_execute:
            bot.send_message(chat_id, 'Код для выполнения не найден.')
        else:
            try:
                exec(code_to_execute)
                bot.send_message(chat_id, 'Код успешно выполнен.')
                code_to_execute = ''  # Очищаем сохраненный код после выполнения
            except Exception as e:
                bot.send_message(chat_id, f'Произошла ошибка при выполнении кода: {e}')
