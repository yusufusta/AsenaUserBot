import threading
from sqlalchemy import func, distinct, Column, String, UnicodeText
try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError


class Mesajlar(BASE):
    __tablename__ = "mesaj"
    komut = Column(UnicodeText, primary_key=True, nullable=False)
    mesaj = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, komut, mesaj):
        self.komut = komut  # ensure string
        self.mesaj = mesaj

    def __repr__(self):
        return "<Mesaj '%s' için %s>" % (self.komut, self.mesaj)

    def __eq__(self, other):
        return bool(isinstance(other, Mesajlar)
                    and self.komut == other.komut
                    and self.mesaj == other.mesaj)


Mesajlar.__table__.create(checkfirst=True)

KOMUT_INSERTION_LOCK = threading.RLock()

def ekle_mesaj(komut, mesaj):
    with KOMUT_INSERTION_LOCK:
        try:
            SESSION.query(Mesajlar).filter(Mesajlar.komut == komut).delete()
        except:
            pass

        komut = Mesajlar(komut, mesaj)
        SESSION.merge(komut)
        SESSION.commit()


def getir_mesaj(komu):
    try:
        MESAJ = SESSION.query(Mesajlar).filter(Mesajlar.komut == komu).first()
        return MESAJ.mesaj
    except:
        return False
    

def sil_mesaj(komu):
    try:
        SESSION.query(Mesajlar).filter(Mesajlar.komut == komu).delete()
        SESSION.commit()
    except Exception as e:
        return e
    return True
