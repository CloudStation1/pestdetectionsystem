#this is just for testing this module
import telegramMsgSender as bot
import time

t = bot.notifier()
t.sendPhoto(open(r"/root/cloudComputing/pestdetectionsystem/node/test_data/test.jpg", 'rb'), 'test pic, Match: 0')