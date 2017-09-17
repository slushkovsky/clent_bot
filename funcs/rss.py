import logging
from sqlalchemy.orm.exc import NoResultFound

import db
import utils
import config


def cmd_list_rss(bot, update): 
    __session = db.Session() 
    rss_list = __session.query(db.RSS).filter_by(user=update.message.from_user.id).all() 

    if len(rss_list) == 0: 
        bot.send_message(update.message.chat_id, text='Unfortinately, you haven\'t any RSS subscription right now')
    else: 
        bot.send_message(update.message.chat_id, text='\n'.join((f'{rss.id}: {rss.link}' for rss in rss_list)))  

def cmd_add_rss(bot, update): 
    arg = utils.get_cmd_arg(update)

    if arg is None: 
        bot.send_message(update.message.chat_id, text=config.MSG_ERROR_INVALID_ARGUMENT)
    elif len(arg) == 0: 
        bot.send_message(update.message.chat_id, text=config.MSG_ERROR_EMPTY_ARGUMENT) 
    else: 
        __session = db.Session() 
        __session.add(db.RSS(user=update.message.from_user.id, link=arg))
        __session.commit()

        bot.send_message(update.message.chat_id, text='OK')   

def cmd_remove_rss(bot, update): 
    arg = utils.get_cmd_arg(update)

    if arg is None: 
        bot.send_message(update.message.chat_id, text=config.MSG_ERROR_INVALID_ARGUMENT) 
    elif len(arg) == 0: 
        bot.send_message(update.message.chat_id, text=config.MSG_ERROR_EMPTY_ARGUMENT) 
    else: 
        try: 
            rss_id = int(arg)  
        except: 
            bot.send_message(update.message.chat_id, text='Argument must be an integer') 
        else:
            try:  
                __session = db.Session() 
                __session.delete(__session.query(db.RSS).filter_by(id=rss_id).one())
                __session.commit()
            except NoResultFound: 
                bot.send_message(update.message.chat_id, text=f'No such rss with id {rss_id}') 
            else: 
                bot.send_message(update.message.chat_id, text='OK')
