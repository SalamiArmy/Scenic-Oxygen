# coding=utf-8

from commands import watchgif

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    watchgif.setWatchValue(watchgif.getAllWatches().replace(',' + chat_id + ':' + message + ',', ',').replace(',' + chat_id + ':' + message, ''))
