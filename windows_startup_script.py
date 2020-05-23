from telethon import TelegramClient
API_KEY="Bunu buraya yazın"
API_HASH="Bunu buraya yazın"
#my.telegram.org adresinden alın
bot = TelegramClient('userbot',API_KEY,API_HASH)
bot.start()

#Bu komut dosyası botunuzu çalıştırmaz, sadece bir oturum oluşturur.
