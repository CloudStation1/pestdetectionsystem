import requests
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Main:

    def Notification(self,link,message):
        base_url = "https://api.telegram.org/bot5820363513:AAHBQiy7GBUAPO18gaFz-VzqqBMspsASjgc/sendPhoto"
        parameters = {
        "chat_id" : "5269537317",
        "caption" : message
        }
        resp = requests.post(base_url, data = parameters, files=link)
        log.info(resp.text)

