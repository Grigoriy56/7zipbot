import telebot
import zipfile
import os
from telebot import types
name = ''
work = ''
iteratsion = 1

bot = telebot.TeleBot("1385764658:AAEgHq3te2sX89u5ivf4t9LxdEjXr1yhNps")


def photo_processing():
    os.chdir('photos')
    files_names = os.listdir()
    global name, work
    zip_file = zipfile.ZipFile(work+'_'+name+'.zip', "w")
    for file in files_names:
        zip_file.write(file, compress_type=zipfile.ZIP_DEFLATED)
        os.remove(file)
    zip_file.close()


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    key_сw = types.InlineKeyboardButton(text='КР', callback_data='cw')
    keyboard.add(key_сw)
    key_hw = types.InlineKeyboardButton(text='ДР', callback_data='hw')
    keyboard.add(key_hw)
    bot.send_message(message.from_user.id, text='Привет. Я помогу тебе сдать работу.', reply_markup=keyboard)
    bot.register_next_step_handler(bot.send_message(message.chat.id,
                                'Напиши в формате dd.mm.year дату работы.'), reg_name)


@bot.callback_query_handler(func=lambda call:True)
def quary_handler(call):
    global work
    if call.data == 'cw':
        work = 'cw'
    else:
        work = 'hw'


def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, 'Отправь фото по порядку одним сообщением. После загрузки всех фото пропишите /send')


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    global iteratsion
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = file_info.file_path[:7] + str(iteratsion) + '.jpg'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            bot.reply_to(message, "Фото добавлены в архив. /send")
            iteratsion += 1
    except Exception as e:
        bot.reply_to(message, 'Произошла ошибка. Наругайте Гришу.')


@bot.message_handler(commands=['send'])
def send_photos(message):
    photo_processing()
    global work, name, iteratsion
    with open(work+'_'+name+'.zip', 'rb') as file:
        bot.send_document(message.chat.id, file)
    os.remove(work+'_'+name+'.zip')
    os.chdir('..')
    name = ''
    work = ''
    iteratsion = 1


@bot.message_handler(content_types=['text'])
def restart_message(message):
    bot.send_message(message.chat.id, 'Напиши мне /start, я по-другому не понимаю :(')


bot.polling()
