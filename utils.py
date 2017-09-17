import logging

from telegram import MessageEntity


def get_cmd_arg(update, strip=True): 
    entities = update.message.entities

    if len(entities) == 0: 
        logging.warning(f'Message {update.message.text} didn\'t contain any command')
        return None 

    if entities[0].type == MessageEntity.BOT_COMMAND: 
        arg = update.message.text[entities[0].length + 1:]
 
        if strip: 
            arg = arg.strip() 
        
        return arg

    else: 
        loggin.warning(f'Wrong command position in message {udpate.message.text}') 
        return None

    logging.error('Unexpected exit of function')
    return None
