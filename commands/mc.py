# coding=utf-8
import ConfigParser
import os

import telegram
#reverse image search imports:

from mcstatus import MinecraftServer


def run(chat_id, user, message):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()


    mcServer = keyConfig.get('Minecraft', 'SVR_ADDR')
    mcPort = int(keyConfig.get('Minecraft', 'SVR_PORT'))
    dynmapPort = keyConfig.get('Minecraft', 'DYNMAP_PORT')
    status = MinecraftServer(mcServer, mcPort).status()
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    userWithCurrentChatAction = chat_id
    urlForCurrentChatAction = ('The server at {0} has {1} players and replied in {2} ms' +
                               ('' if dynmapPort == '' else '\nSee map: ' + mcServer + ':' + dynmapPort)) \
        .format(mcServer + ':' + str(mcPort), status.players.online, status.latency)
    bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)