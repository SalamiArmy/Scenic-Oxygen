# coding=utf-8
from commands.watchtopgames import unwatch

watchedCommandName = 'define'

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    unwatch(bot, chat_id, message)


