# coding=utf-8

watchedCommandName = 'get'

from commands import watch

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    watches = watch.getAllWatches()
    if ',' + chat_id + ':' + message + ',' in watches or ',' + chat_id + ':' + message in watches:
        watch.setWatchValue(watches.replace(',' + chat_id + ':' + message + ',', ',').replace(',' + chat_id + ':' + message, ''))
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
