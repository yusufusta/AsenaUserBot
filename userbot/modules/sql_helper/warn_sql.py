# WARN PLUGIN #
# CODED BY YUSUF USTA #

import threading
from sqlalchemy import func, distinct, Column, String, UnicodeText, Integer
try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError


class Warn(BASE):
    __tablename__ = "warn"
    uid = Column(UnicodeText, primary_key=True, nullable=False)
    warn = Column(Integer, primary_key=True, nullable=False)
    sebep = Column(UnicodeText, nullable=True)

    def __init__(self, uid, warn, sebep = None):
        self.uid = uid  # ensure string
        self.warn = warn
        self.sebep = sebep
    def __repr__(self):
        return "<Warn '%s' için %s>" % (self.uid, self.warn)

    def __eq__(self, other):
        return bool(isinstance(other, Warn)
                    and self.komut == other.komut
                    and self.mesaj == other.mesaj)


Warn.__table__.create(checkfirst=True)

KOMUT_INSERTION_LOCK = threading.RLock()

def ekle_warn(userid, sebep = None):
    with KOMUT_INSERTION_LOCK:
        try:
            UYARI = SESSION.query(Warn).filter(Warn.uid == userid).first()
            wsayi = int(UYARI.warn)
            SESSION.query(Warn).filter(Warn.uid == userid).delete()
        except:
            wsayi =  0

        wsayi += 1
        if sebep == None:
            komut = Warn(userid, wsayi)
        else:
            komut = Warn(userid, wsayi, sebep)
        SESSION.merge(komut)
        SESSION.commit()



def getir_warn(userid):
    try:
        UYARI = SESSION.query(Warn).filter(Warn.uid == userid).first()
        return UYARI.warn
    except:
        return 0
    

def sil_warn(userid):
    try:
        wsayi = SESSION.query(Warn).filter(Warn.uid == userid).first().warn
        if wsayi == 0:
            return False
        nsayi = wsayi - 1
        SESSION.query(Warn).filter(Warn.uid == userid).delete()

        uyari = Warn(userid, nsayi)
        SESSION.merge(uyari)
        SESSION.commit()
        return True
    except:
        return False
    return True

def toplu_sil_warn(userid):
    try:
        uyari = Warn(userid, 0)
        SESSION.merge(uyari)
        SESSION.commit()
    except:
        return False
    return True
