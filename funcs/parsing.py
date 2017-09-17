import re
import logging

from sqlalchemy.orm.exc import NoResultFound
from telegram import ParseMode

import db
import utils
import config


@utils.from_known_user
def cmd_list_parsers(user, update):
    __session = db.Session() 
    parsers = __session.query(db.Parser).filter_by(user_id=user.id).all() 
 
    if len(parsers) == 0: 
        update.message.reply_text('You haven\'t any parser') 
    else: 
        update.message.reply_text('\n'.join(f'{parser.id}. {parser.regex}' for parser in parsers))

@utils.from_known_user
def cmd_add_parser(user, update):
    arg = utils.get_cmd_arg(update)

    if arg is None: 
        update.message.reply_text(config.MSG_ERROR_INVALID_ARGUMENT)
    elif len(arg) == 0:
        update.message.reply_text(config.MSG_ERROR_EMPTY_ARGUMENT)  
    else:
        __session = db.Session()
        __session.add(db.Parser(regex=arg.strip(), user_id=user.id))
        __session.commit()

        update.message.reply_text('OK') 

@utils.from_known_user
def cmd_remove_parser(user, update): 
    arg = utils.get_cmd_arg(update)

    if arg is None: 
        update.message.reply_text(config.MSG_ERROR_INVALID_ARGUMENT) 
    elif len(arg) == 0: 
        update.message.reply_text(config.MSG_ERROR_EMPTY_ARGUMENT) 
    else:
        try: 
            parser_id = int(arg)  
        except ValueError: 
            update.message.reply_text('Argument must be an integer (id of a parser)') 
        else: 
            try: 
                __session = db.Session()
                __session.delete(__session.query(db.Parser).filter_by(id=parser_id, user_id=user.id).one())
                __session.commit()
            except NoResultFound:
                update.message.reply_text(f'No such parser with id {parser_id}') 
            else: 
                update.message.reply_text('OK')

@utils.from_known_user 
def on_forwarded(user, update): 
    msg = update.message.text 
    sender = update.message.forward_from.username
    first_name = update.message.forward_from.first_name
    last_name = update.message.forward_from.last_name
    date = update.message.forward_date

    __session = db.Session() 
    parsers = __session.query(db.Parser).filter_by(user_id=user.id).all()

    for parser in parsers: 
        match = re.search(parser.regex, msg)   

        if match is not None: 
            update.message.reply_text( 
                text=f'<b>{parser.regex}</b> {date}\n{first_name} {last_name} @{sender}\n--------------------------------------------\n{msg}',
                parse_mode=ParseMode.HTML
            )

            break  
