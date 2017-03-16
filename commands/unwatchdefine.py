# coding=utf-8
import main
from commands import watchdefine

watchedCommandName = 'define'

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    watches = main.getAllWatches()
    if ',' + watchedCommandName + ':' + str(chat_id) + ':' + message + ',' in watches or ',' + watchedCommandName + ':' \
            + str(chat_id) + ':' + message in watches:
        main.removeFromAllWatches(watchedCommandName + ':' + str(chat_id) + ':' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' not found.')
    if watchdefine.getWatchValue(chat_id) != '':
        watchdefine.setWatchValue(chat_id, '')
