import random


def choose(msg):
    split = msg.split(" ")
    return split[random.randrange(0, len(split))]

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    bot.sendMessage(chat_id=chat_id, text=choose(message))
    return True
