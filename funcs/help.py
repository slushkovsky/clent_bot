import config 

def cmd_help(bot, update): 
    update.message.reply_text(text=config.MSG_HELP)
