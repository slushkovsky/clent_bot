import logging
from sqlalchemy.orm.exc import NoResultFound

import db
import utils
import config


@utils.from_known_user
def cmd_list_rss(user, update): 
    __session = db.Session() 
    rss_list = __session.query(db.RSS).filter_by(user_id=user.id).all() 

    if len(rss_list) == 0: 
        update.message.reply_text('Unfortinately, you haven\'t any RSS subscription right now')
    else: 
        update.message.reply_text('\n'.join((f'{rss.id}: {rss.link}' for rss in rss_list)))  

@utils.from_known_user
def cmd_add_rss(user, update): 
    arg = utils.get_cmd_arg(update)

    if arg is None: 
        update.message.reply_text(config.MSG_ERROR_INVALID_ARGUMENT)
    elif len(arg) == 0: 
        update.message.reply_text(config.MSG_ERROR_EMPTY_ARGUMENT) 
    else: 
        __session = db.Session() 
        __session.add(db.RSS(user_id=user.id, link=arg))
        __session.commit()

        update.message.reply_text('OK')   

@utils.from_known_user
def cmd_remove_rss(user, update): 
    arg = utils.get_cmd_arg(update)

    if arg is None: 
        update.message.reply_text(config.MSG_ERROR_INVALID_ARGUMENT) 
    elif len(arg) == 0: 
        update.message.reply_text(config.MSG_ERROR_EMPTY_ARGUMENT) 
    else: 
        try: 
            rss_id = int(arg)  
        except: 
            update.message.reply_text('Argument must be an integer') 
        else:
            try:  
                __session = db.Session() 
                __session.delete(__session.query(db.RSS).filter_by(id=rss_id).one())
                __session.commit()
            except NoResultFound: 
                update.message.reply_text(f'No such rss with id {rss_id}') 
            else: 
                update.message.reply_text('OK')
