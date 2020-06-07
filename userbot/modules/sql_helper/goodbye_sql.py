try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError

from sqlalchemy import BigInteger, Column, Numeric, String, UnicodeText


class Goodbye(BASE):
    __tablename__ = "goodbye"
    chat_id = Column(String(14), primary_key=True)
    previous_goodbye = Column(BigInteger)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, chat_id, previous_goodbye, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.previous_goodbye = previous_goodbye
        self.reply = reply
        self.f_mesg_id = f_mesg_id


Goodbye.__table__.create(checkfirst=True)


def get_goodbye(chat_id):
    try:
        return SESSION.query(Goodbye).get(str(chat_id))
    finally:
        SESSION.close()


def get_current_goodbye_settings(chat_id):
    try:
        return SESSION.query(Goodbye).filter(
            Goodbye.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_goodbye_setting(chat_id, previous_goodbye, reply, f_mesg_id):
    to_check = get_goodbye(chat_id)
    if not to_check:
        adder = Goodbye(chat_id, previous_goodbye, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        rem = SESSION.query(Goodbye).get(str(chat_id))
        SESSION.delete(rem)
        SESSION.commit()
        adder = Goodbye(chat_id, previous_goodbye, reply, f_mesg_id)
        SESSION.commit()
        return False


def rm_goodbye_setting(chat_id):
    try:
        rem = SESSION.query(Goodbye).get(str(chat_id))
        if rem:
            SESSION.delete(rem)
            SESSION.commit()
            return True
    except BaseException:
        return False


def update_previous_goodbye(chat_id, previous_goodbye):
    row = SESSION.query(Goodbye).get(str(chat_id))
    row.previous_goodbye = previous_goodbye
    SESSION.commit()
