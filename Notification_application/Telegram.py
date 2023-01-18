import requests

class Main:

    def Notification(self,link,message):
        base_url = "https://api.telegram.org/bot5928782166:AAF7TvP32JMgiyhXEDhZnCgE4LaGF48JFAk/sendPhoto"
        parameters = {
        "chat_id" : "-615882008",
        "photo" : link,
        "caption" : message
        }
        resp = requests.get(base_url, data = parameters)
        print(resp.text)

        

