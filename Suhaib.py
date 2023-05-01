import re
import os
from pyrogram import Client, filters
from pyrogram.types import Message
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Set up Telegram API credentials
API_ID = os.environ.get('API_ID', '23990433')
API_HASH = os.environ.get('API_HASH', 'e6c4b6ee1933711bc4da9d7d17e1eb20')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '5830549215:AAFPIBMULsTr6WpnIXkM1Ics7Xdv1wJn9Ys')

# Set up the Pyrogram client
app = Client('my_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private)
async def handle_private_message(bot, message):
    url = message.text
    chat_id, message_id = get_chat_id_message_id(url)
    if chat_id and message_id:
        try:
            post = await bot.get_messages(chat_id, message_id)
            await message.reply(post.text, parse_mode='HTML')
        except:
            await message.reply('Sorry, I couldn\'t retrieve the post from the private channel.')

@app.on_message(filters.channel)
async def handle_channel_message(bot, message):
    url = message.text
    chat_id, message_id = get_chat_id_message_id(url)
    if chat_id and message_id:
        try:
            post = await bot.get_messages(chat_id, message_id)
            await message.reply(post.text, parse_mode='HTML')
        except:
            await message.reply('Sorry, I couldn\'t retrieve the post from the public channel.')

def get_chat_id_message_id(url):
    match = re.search(r'(https?://[^\s]+)', url)
    if match:
        url = match.group(0)
    else:
        return None, None

    if 't.me/c/' in url:
        chat_id, message_id = url.split('/')[-2:]
        return int(chat_id), int(message_id)
    elif 't.me/' in url:
        chat_id, message_id = url.split('/')[-2:]
        return int('-100' + chat_id), int(message_id)
    else:
        return None, None

def main():
    app.run()

if __name__ == '__main__':
    main()
