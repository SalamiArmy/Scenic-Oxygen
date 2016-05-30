import random


def choose(msg):
    split = msg.split(" ")
    return split[random.randrange(0, len(split))]

def run(bot, keyConfig, chat_id, user, message):
    bot.sendMessage(chat_id=chat_id, text=choose(message))
