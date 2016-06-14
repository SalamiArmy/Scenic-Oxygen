# coding=utf-8

from mcstatus import MinecraftServer


def run(bot, keyConfig, chat_id, user, message):

    mcServer = keyConfig.get('Minecraft', 'SVR_ADDR')
    mcPort = int(keyConfig.get('Minecraft', 'SVR_PORT'))
    dynmapPort = keyConfig.get('Minecraft', 'DYNMAP_PORT')
    status = MinecraftServer(mcServer, mcPort).status()
    bot.sendMessage(chat_id=chat_id, text=('The server at {0} has {1} players and replied in {2} ms' +
                                           ('' if dynmapPort == '' else '\nSee map: ' + mcServer + ':' + dynmapPort)) \
                    .format(mcServer + ':' + str(mcPort), status.players.online, status.latency))
    return True