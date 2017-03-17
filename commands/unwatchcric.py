# coding=utf-8
from commands.watchcric import unwatch

watchedCommandName = 'cric'

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    unwatch(bot, chat_id, message)


