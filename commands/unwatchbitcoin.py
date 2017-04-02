# coding=utf-8
from commands.watchbitcoin import unwatch

def run(bot, chat_id, user, keyConfig, message, intention_confidence=0.0):
    unwatch(bot, chat_id, message, True)
