import requests

class Main:

    def Notification(self,link,message):
        base_url = "https://api.telegram.org/bot5928782166:AAF7TvP32JMgiyhXEDhZnCgE4LaGF48JFAk/sendPhoto"
        parameters = {
        "chat_id" : "-615882008",
        "caption" : message
        }
        resp = requests.post(base_url, data = parameters, files=link)
        print(resp.text)

        

