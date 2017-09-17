import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

import config
from funcs.parsing import cmd_list_parsers, cmd_add_parser, cmd_remove_parser, on_forwarded
from funcs.rss import cmd_list_rss, cmd_add_rss, cmd_remove_rss


def cmd_help(bot, update): 
    bot.send_message(update.message.chat_id, text=config.MSG_HELP) 

def cmd_start(bot, update):
    bot.send_message(update.message.chat_id, text=config.MSG_START) 

if __name__ == '__main__': 
    bot = Updater(token=config.BOT_TOKEN)
  
    commands = {
        'start': cmd_start, 
        'help': cmd_help,
        'list_parsers': cmd_list_parsers,
        'add_parser': cmd_add_parser, 
        'remove_parser': cmd_remove_parser,
        'list_rss': cmd_list_rss, 
        'add_rss': cmd_add_rss,
        'remove_rss': cmd_remove_rss
    }

    for cmd, handler in commands.items(): 
        bot.dispatcher.add_handler(CommandHandler(cmd, handler))

    bot.dispatcher.add_handler(MessageHandler(Filters.forwarded, on_forwarded))  

    bot.start_polling()
