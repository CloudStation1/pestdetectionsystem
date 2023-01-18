
import Telegram
#a="https://github.com/CloudStation1/pestdetectionsystem/blob/1361ec75fea982105a83e63420fbfda6af61fb96/WebServer/Webapp/static/images/rat-image.jpeg"
a={'photo':open(r'WebServer/Webapp/static/images/rat-image.jpeg','rb')}
b="This is Message"
object=Telegram.Main()

object.Notification(a,b)
