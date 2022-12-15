# Author : Soni, Sameer
# Date : 15.12.2022

import os
import telebot
from dotenv import load_dotenv

load_dotenv()

class notifier:
    def __init__(self):
        api_key = os.getenv('API_KEY')
        self.chat_id = os.getenv('CHAT')
        self.bot = telebot.TeleBot(api_key)

    def sendTelegramMsg(self, message):
        self.bot.send_message(self.chat_id, message)