# coding=utf-8
import json
import urllib
import urllib2

from mcstatus import MinecraftServer


def run(bot, keyConfig, chat_id, user, message):
    mcApiUrl = 'http://minecraft-server.li/server/api.php'
    args = {'ip': keyConfig.get('Minecraft', 'SVR_ADDR'),
            'port': keyConfig.get('Minecraft', 'SVR_PORT')}
    realUrl = mcApiUrl + '?' + urllib.urlencode(args)
    mcOpener = urllib2.build_opener()
    mcOpener.addheaders = [('User-agent',
                                'Mozilla/5.0 (X11; Linux i686) ApleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]
    rawData = mcOpener.open(realUrl).read()
    data = json.loads(rawData)
    mcServer = keyConfig.get('Minecraft', 'SVR_ADDR')
    mcPort = int(keyConfig.get('Minecraft', 'SVR_PORT'))
    if 'online' in data and data['online'] == 'true':
        dynmapPort = keyConfig.get('Minecraft', 'DYNMAP_PORT')
        print('got players online as ' + data['players'])
        print('got ping as ' + str(data['ping']))
        bot.sendMessage(chat_id=chat_id, text=('The server at {0} has {1} players and replied in {2} ms' +
                                               ('' if dynmapPort == '' else '\nSee map: ' + mcServer + ':' + dynmapPort)) \
                        .format(mcServer + ':' + str(mcPort), data['players'], str(data['ping'])))
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find any information about the Minecraft server at ' +
                                              mcServer + ':' + str(mcPort))