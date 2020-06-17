import asyncio
import os
import sys
import time
import random

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PasswordHashInvalidError, PhoneNumberInvalidError
from telethon.network import ConnectionTcpAbridged
from telethon.utils import get_display_name
from telethon.sessions import StringSession

try:
   import requests
   import bs4
except:
   print("[!] Requests Bulunamadı. Yükleniyor...")
   print("[!] Bs4 Bulunamadı. Yükleniyor...")

   if os.name == 'nt':
      os.system("python3.8 -m pip install requests")
      os.system("python3.8 -m pip install bs4")
   else:
      os.system("pip3 install requests")
      os.system("pip3 install bs4")


# Original Source https://github.com/LonamiWebs/Telethon/master/telethon_examples/interactive_telegram_client.py #
loop = asyncio.get_event_loop()

class InteractiveTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash,
                 telefon=None, proxy=None):
        super().__init__(
            session_user_id, api_id, api_hash,
            connection=ConnectionTcpAbridged,
            proxy=proxy
        )
        self.found_media = {}
        print('@AsenaUserBot String Alıcıya Hoş Geldiniz')
        print('[i] Telegramın Sunucularına Bağlanılıyor...')
        try:
            loop.run_until_complete(self.connect())
        except IOError:
            print('[!] Bağlanılırken bir hata oluştu. Yeniden deneniyor...')
            loop.run_until_complete(self.connect())

        if not loop.run_until_complete(self.is_user_authorized()):
            if telefon == None:
               user_phone = input('[?] Telefon Numaranız (Örnek: +90xxxxxxxxxx): ')
            else:
               user_phone = telefon
            try:
                loop.run_until_complete(self.sign_in(user_phone))
                self_user = None
            except PhoneNumberInvalidError:
                print("[!] Geçersiz Bir Numara Girdiniz Örnekte Gibi Giriniz. Örnek: +90xxxxxxxxxx")
                exit(1)
            except ValueError:
               print("[!] Geçersiz Bir Numara Girdiniz Örnekte Gibi Giriniz. Örnek: +90xxxxxxxxxx")
               exit(1)

            while self_user is None:
                code = input('[?] Telegramdan Gelen Beş (5) Haneli Kodu Giriniz: ')
                try:
                    self_user =\
                        loop.run_until_complete(self.sign_in(code=code))
                except PhoneCodeInvalidError:
                    print("[!] Kodu Yanlış Yazdınız. Lütfen Tekrar Deneyiniz. [Fazla Deneme Yapmak Ban Yemenize Neden Olur]")
                except SessionPasswordNeededError:
                    pw = input('[i] İki aşamalı doğrulama tespit edildi. '
                                 '[?] Şifrenizi Yazınız: ')
                    try:
                        self_user =\
                            loop.run_until_complete(self.sign_in(password=pw))
                    except PasswordHashInvalidError:
                        print("[!] 2 Aşamalı Şifrenizi Yanlış Yazdınız. Lütfen Tekrar Deneyiz. [Fazla Deneme Yapmak Ban Yemenize Neden Olur]")


if __name__ == '__main__':
   print("[i] Asena String V3\n@AsenaUserBot\n\n")
   print("[1] OtoMatik API ID/HASH Alıcı")
   print("[2] String Alıcı\n")
   
   try:
      secim = int(input("[?] Seçim Yapın: "))
   except:
      print("[!] Lütfen Sadece Rakam Giriniz!")

   if secim == 2:
      API_ID = input('[?] API ID\'iniz [Hazır Key\'leri Kullanmak İçin Boş Bırakınız]: ')
      if API_ID == "":
         print("[i] Hazır Keyler Kullanılıyor...")
         API_ID = 4
         API_HASH = "014b35b6184100b085b0d0572f9b5103"
      else:
         API_HASH = input('[?] API HASH\'iniz: ')

      client = InteractiveTelegramClient(StringSession(), API_ID, API_HASH)
      print("[i] String Keyiniz Aşağıdadır!\n\n\n" + client.session.save())
   elif secim == 1:
      numara = input("[?] Telefon Numaranız: ")
      try:
         rastgele = requests.post("https://my.telegram.org/auth/send_password", data={"phone": numara}).json()["random_hash"]
      except:
         print("[!] Kod Gönderilemedi. Telefon Numaranızı Kontrol Ediniz.")
         exit(1)
      
      sifre = input("[?] Telegram'dan Gelen Kodu Yazınız: ")
      try:
         cookie = requests.post("https://my.telegram.org/auth/login", data={"phone": numara, "random_hash": rastgele, "password": sifre}).cookies.get_dict()
      except:
         print("[!] Büyük İhtimal Kodu Yanlış Yazdınız. Lütfen Scripti Yeniden Başlatın.")
         exit(1)
      app = requests.post("https://my.telegram.org/apps", cookies=cookie).text
      soup = bs4.BeautifulSoup(app, features="html.parser")

      if soup.title.string == "Create new application":
         print("[i] Uygulamanız Yok. Oluşturuluyor...")
         hashh = soup.find("input", {"name": "hash"}).get("value")
         AppInfo = {
            "hash": hashh,
            "app_title":"Asena UserBot",
            "app_shortname": "asenaus" + str(random.randint(9, 99)) + str(time.time()).replace(".", ""),
            "app_url": "",
            "app_platform": "android",
            "app_desc": ""
         }
         app = requests.post("https://my.telegram.org/apps/create", data=AppInfo, cookies=cookie).text
         print(app)
         print("[i] Uygulama başarıyla oluşturuldu!")
         print("[i] API ID/HASH alınıyor...")
         newapp = requests.get("https://my.telegram.org/apps", cookies=cookie).text
         newsoup = bs4.BeautifulSoup(newapp, features="html.parser")

         g_inputs = newsoup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
         app_id = g_inputs[0].string
         api_hash = g_inputs[1].string
         print("[i] Bilgiler Getirildi! Lütfen Bunları Not Ediniz.\n\n")
         print(f"[i] API ID: {app_id}")
         print(f"[i] API HASH: {api_hash}")
         try:
            stringonay = int(input("[?] String Almak İster Misiniz? [Evet için 1 Yazınız]: "))
         except:
            print("[!] Lütfen Sadece Sayı Yazınız!")

         if stringonay == 1:
            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
            print("[i] String Keyiniz Aşağıdadır!\n\n\n" + client.session.save())
         else:
            print("[i] Script Durduruluyor...")
            exit(1)
      elif  soup.title.string == "App configuration":
         print("[i] Halihazır da Uygulama Oluşturmuşsunuz. API ID/HASH Çekiliyor...")
         g_inputs = soup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
         app_id = g_inputs[0].string
         api_hash = g_inputs[1].string
         print("[i] Bilgiler Getirildi! Lütfen Bunları Not Ediniz.\n\n")
         print(f"[i] API ID: {app_id}")
         print(f"[i] API HASH: {api_hash}")
         try:
            stringonay = int(input("[?] String Almak İster Misiniz? [Evet için 1 Yazınız]: "))
         except:
            print("[!] Lütfen Sadece Sayı Yazınız!")

         if stringonay == 1:
            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
            print("[i] String Keyiniz Aşağıdadır!\n\n\n" + client.session.save())
         else:
            print("[i] Script Durduruluyor...")
            exit(1)
      else:
         print("[!] Bir Hata Oluştu.")
         exit(1)
   else:
      print("[!] Bilinmeyen seçim.")