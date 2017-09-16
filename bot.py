import re
import sqlite3
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


TOKEN = '429132851:AAH1a7lDh1ilDmP9yG8u_ps-pwE0VgfN6Iw'
DB_PATH = 'parsers.db'
PARSERS_TABLE_NAME = 'parsers'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def db_exec(command, commit=False): 
    db = sqlite3.connect(DB_PATH)
    result = list(db.cursor().execute(command))
    db.commit()
    return result

def db_create(): 
    db_exec(f'CREATE TABLE IF NOT EXISTS {PARSERS_TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, regex TEXT NOT NULL)', commit=True)

def db_list_parsers():
    return db_exec(f'SELECT * FROM {PARSERS_TABLE_NAME}')

def db_add_parser(regex): 
    db_exec(f'INSERT INTO {PARSERS_TABLE_NAME} (regex) VALUES ("{regex}")', commit=True)

def db_remove_parser(id): 
    db_exec(f'DELETE FROM {PARSERS_TABLE_NAME} WHERE id={id}', commit=True)

def cmd_start(bot, update):
    bot.send_message(update.message.chat_id, text='Hello') 

def cmd_list_parsers(bot, update): 
    bot.send_message(update.message.chat_id, text='\n'.join(f'{id}. {parser}' for id, parser in db_list_parsers()))

def cmd_add_parser(bot, update):
    m = re.match('^/[^ ]+ (.+)$', update.message.text) 

    if m is None: 
        bot.send_message(update.message.chat_id, text='Invalid argument') 
    else:
        db_add_parser(m.group(1)) 
        bot.send_message(update.message.chat_id, text='OK') 

def cmd_remove_parser(bot, update): 
    m = re.match('^/[^ ]+ (\d+)$', update.message.text) 

    if m is None: 
        bot.send_message(update.message.chat_id, text='Invalid argument') 
    else:
        db_remove_parser(m.group(1))
        bot.send_message(update.message.chat_id, text='OK') 


def on_forwarded(bot, update): 
    msg = update.message.text 
    sender = update.message.forward_from.username
    first_name = update.message.forward_from.first_name
    last_name = update.message.forward_from.last_name
    date = update.message.forward_date

    parsers = db_list_parsers()

    for id, parser in parsers: 
        match = re.search(parser, msg)   

        if match is not None: 
            bot.send_message(update.message.chat_id, text=f'{date} {first_name} {last_name} @{sender} (parser {id}: {parser}):\n{msg}')
            return

if __name__ == '__main__': 
    db_create()

    bot = Updater(token=TOKEN)
  
    bot.dispatcher.add_handler(CommandHandler('start', cmd_start))
    bot.dispatcher.add_handler(CommandHandler('list_parsers', cmd_list_parsers))
    bot.dispatcher.add_handler(CommandHandler('add_parser', cmd_add_parser)) 
    bot.dispatcher.add_handler(CommandHandler('remove_parser', cmd_remove_parser)) 
 
    bot.dispatcher.add_handler(MessageHandler(Filters.forwarded, on_forwarded))  

    bot.start_polling()
