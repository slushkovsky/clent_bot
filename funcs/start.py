import config 
import db


def cmd_start(bot, update): 
    __session = db.Session() 
    __session.add(db.User(telegram_id=update.message.from_user.id, chat_id=update.message.chat_id))
    __session.commit()

    update.message.reply_text(text=config.MSG_START) 
