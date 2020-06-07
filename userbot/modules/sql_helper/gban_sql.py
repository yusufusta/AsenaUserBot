try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String, UnicodeText


class GBan(BASE):
    __tablename__ = "gban"
    sender = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.sender = str(sender)


GBan.__table__.create(checkfirst=True)


def is_gbanned (sid):
    try:
        sonuc = SESSION.query(GBan).filter(GBan.sender == sid).first()
        return sonuc.sender
    except:
        return False

def gbanlist():
    try:
        return SESSION.query(GBan).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def gban(sender):
    try:
        adder = GBan(str(sender))
        SESSION.add(adder)
        SESSION.commit()
    except:
        return False


def ungban(sender):
    rem = SESSION.query(GBan).get((str(sender)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
