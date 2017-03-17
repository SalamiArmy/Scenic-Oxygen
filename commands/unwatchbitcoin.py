# coding=utf-8
from commands import watchbitcoin

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    watchbitcoin.unwatch(bot, chat_id, message)
