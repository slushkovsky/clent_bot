import re
from sqlalchemy.orm.exc import NoResultFound

from telegram import ParseMode

import db
import utils
import config


def cmd_list_parsers(bot, update):
    __session = db.Session() 
    parsers = __session.query(db.Parser).filter_by(user=update.message.from_user.id).all() 
 
    if len(parsers) == 0: 
        bot.send_message(update.message.chat_id, text='You haven\'t any parser') 
    else: 
        bot.send_message(update.message.chat_id, text='\n'.join(f'{parser.id}. {parser.regex}' for parser in parsers))

def cmd_add_parser(bot, update):
    arg = utils.get_cmd_arg(update)

    if arg is None: 
        bot.send_message(update.message.chat_id, text=config.MSG_ERROR_INVALID_ARGUMENT)
    elif len(arg) == 0:
        bot.send_message(update.message.chat_id, text=config.MSG_ERROR_EMPTY_ARGUMENT)  
    else:
        __session = db.Session()
        __session.add(db.Parser(regex=arg.strip(), user=update.message.from_user.id))
        __session.commit()

        bot.send_message(update.message.chat_id, text='OK') 

def cmd_remove_parser(bot, update): 
    arg = utils.get_cmd_arg(update)

    if arg is None: 
        bot.send_message(update.message.chat_id, text=config.MSG_ERROR_INVALID_ARGUMENT) 
    elif len(arg) == 0: 
        bot.send_message(update.message.chat_id, text=config.MSG_ERROR_EMPTY_ARGUMENT) 
    else:
        try: 
            parser_id = int(arg)  
        except ValueError: 
            bot.send_message(update.message.chat_id, text='Argument must be an integer (id of a parser)') 
        else: 
            try: 
                __session = db.Session()
                __session.delete(__session.query(db.Parser).filter_by(id=parser_id, user=update.message.from_user.id).one())
                __session.commit()
            except NoResultFound:
                bot.send_message(update.message.chat_id, text=f'No such parser with id {parser_id}') 
            else: 
                bot.send_message(update.message.chat_id, text='OK')

def on_forwarded(bot, update): 
    msg = update.message.text 
    sender = update.message.forward_from.username
    first_name = update.message.forward_from.first_name
    last_name = update.message.forward_from.last_name
    date = update.message.forward_date

    __session = db.Session() 
    parsers = __session.query(db.Parser).filter_by(user=update.message.from_user.id).all()

    for parser in parsers: 
        match = re.search(parser.regex, msg)   

        if match is not None: 
            bot.send_message(
                chat_id=update.message.chat_id, 
                text=f'<b>{parser.regex}</b> {date}\n{first_name} {last_name} @{sender}\n{msg}',
                parse_mode=ParseMode.HTML
            )
            return 
