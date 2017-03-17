# coding=utf-8
from commands.watchdefine import Unwatch

watchedCommandName = 'define'

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    Unwatch(bot, chat_id, message)


