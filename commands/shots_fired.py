def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    try:
        target = message.split(" ")[message.split(" ").index("shots_fired") + 1]
        bot.sendMessage(chat_id=chat_id, text="pew PEW pew " + target + " PEW pew PEW")
    except:
        bot.sendMessage(chat_id=chat_id, text="pew pew PEW PEW PEW")
    return True
