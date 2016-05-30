def run(bot, keyConfig, chat_id, user, message):
    try:
        target = message.split(" ")[message.split(" ").index("shots_fired") + 1]
        bot.sendMessage(chat_id=chat_id, text="pew PEW pew " + target + " PEW pew PEW")
    except:
        bot.sendMessage(chat_id=chat_id, text="pew pew PEW PEW PEW")
