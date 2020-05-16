from pydrive.auth import GoogleAuth


def main():
    gauth = GoogleAuth()
    # Kayıtlı istemci kimlik bilgilerini yüklemeyi dene
    gauth.LoadCredentialsFile("secret.json")
    if gauth.credentials is None:
        # Orada değillerse kimlik doğrulaması yap
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Süresi dolmuşsa yenile
        gauth.Refresh()
    else:
        # Kaydedilen kimlik bilgilerini başlat
        gauth.Authorize()
    # Geçerli kimlik bilgilerini bir dosyaya kaydet
    gauth.SaveCredentialsFile("secret.json")


if __name__ == '__main__':
    main()
