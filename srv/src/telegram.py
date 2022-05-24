import logging
from telebot import TeleBot, types
import __init__

logger = logging.getLogger(__name__)

logger.debug('Start telegram bot')
logger.info('Start telegram bot')
logger.warning('Start telegram bot')
logger.error('Start telegram bot')
logger.critical('Start telegram bot')

token = '5161380886:AAE8CULGj5CCLC2MH5Y4qFd6liz5dapWego'
assert token, 'Telegram bot token not found'

bot = TeleBot(token)

_control_panel = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
_btn_user_info = types.KeyboardButton('My info')
_btn_start = types.KeyboardButton('Photo')
_btn_add_api = types.KeyboardButton('Add EMCD api')
_control_panel.add(_btn_start, _btn_user_info, _btn_add_api)


@bot.message_handler(commands=['start', 'help'])
def cmd_help(message: types.Message):
    _html = f'Hello <b>{message.from_user.full_name}</b>' \
            '\nAvailable commands:' \
            '\n /start - display this text' \
            '\n /help - display this text' \
            '\n /web - link to meok website'
    bot.send_message(message.chat.id, _html, parse_mode='html', reply_markup=_control_panel)

    logger.debug(f'Message text: {message.text}')
    logger.debug(f'Message content_type: {message.content_type}')
    logger.debug(f'Message timestamp: {message.date}')
    _user: types.User = message.from_user
    logger.debug(
        f'User id: {_user.id} username: {_user.username} first: {_user.first_name} last: {_user.last_name} full: {_user.full_name} '
        f'lang: {_user.language_code} is_bot: {_user.is_bot}')
    _chat: types.Chat = message.chat
    logger.debug(
        f'Chat id: {_chat.id} username: {_chat.username} last: {_chat.last_name} first: {_chat.first_name} type: {_chat.type} bio: {_chat.bio} '
        f'dsc: {_chat.description} invite_link: {_chat.invite_link} link_id: {_chat.linked_chat_id} '
        f'location: {_chat.location} title: {_chat.title}')


@bot.message_handler(commands=['web'])
def cmd_website(message: types.Message):
    _markup = types.InlineKeyboardMarkup()
    _markup.add(types.InlineKeyboardButton('meok website', url='https://bazha.ru'))
    bot.send_message(message.chat.id, 'Go web?', reply_markup=_markup)


@bot.message_handler(content_types=['text'])
def control_message(message: types.Message):
    logger.debug(f'Message content_type: {message.content_type}')
    logger.debug(f'Message timestamp: {message.date}')
    logger.debug(f'Message text: {message.text}')
    if 'photo' in message.text.lower():
        _photo = open('../assets/img/homer.jpg', 'rb')
        bot.send_photo(message.chat.id, _photo)
    else:
        bot.send_message(message.chat.id, "What do you need?", reply_markup=_control_panel)


@bot.message_handler(content_types=['photo', 'video', 'sticker'])
def control_file(message: types.Message):
    bot.send_message(message.chat.id, 'File received')


bot.polling(non_stop=True)
