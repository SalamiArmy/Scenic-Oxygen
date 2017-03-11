# coding=utf-8
import main

watchedCommandName = 'getgif'

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    watches = main.getAllWatches()
    if ',' + chat_id + ':' + message + ',' in watches or ',' + chat_id + ':' + message in watches:
        main.removeFromAllWatches(chat_id + ':' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
