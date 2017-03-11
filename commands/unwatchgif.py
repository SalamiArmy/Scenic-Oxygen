# coding=utf-8
from commands import retry_on_telegram_error

watchedCommandName = 'getgif'

from commands import watchgif

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    watches = watchgif.getAllWatches()
    if ',' + chat_id + ':' + message + ',' in watches or ',' + chat_id + ':' + message in watches:
        watchgif.setWatchValue(watches.replace(',' + chat_id + ':' + message + ',', ',').replace(',' + chat_id + ':' + message, ''))
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
