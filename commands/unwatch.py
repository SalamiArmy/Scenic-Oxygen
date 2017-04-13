# coding=utf-8
from commands.watch import unwatch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    unwatch(bot, chat_id, message)


