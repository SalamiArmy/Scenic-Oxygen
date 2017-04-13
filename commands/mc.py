# coding=utf-8
import json
import urllib
import urllib2

from mcstatus import MinecraftServer


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    mc_data_formatted, mc_server_found, mc_server_not_found_message = get_mc_data(keyConfig, user)
    if mc_server_found:
        bot.sendMessage(chat_id=chat_id, text=mc_data_formatted)
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text=mc_server_not_found_message)


def get_mc_data(keyConfig, user):
    mc_data_formatted = ''
    mcServer = keyConfig.get('Minecraft', 'SVR_ADDR')
    mcPort = keyConfig.get('Minecraft', 'SVR_PORT')
    dynmapPort = keyConfig.get('Minecraft', 'DYNMAP_PORT')
    mc_server_not_found_message = 'I\'m sorry ' + (
        user if not user == '' else 'Dave') + ', I\'m afraid I can\'t find any information about the Minecraft server at ' + mcServer + ':' + mcPort
    mcApiUrl = 'http://minecraft-server.li/server/api.php'
    args = {'ip': mcServer,
            'port': mcPort}
    realUrl = mcApiUrl + '?' + urllib.urlencode(args)
    mcOpener = urllib2.build_opener()
    mcOpener.addheaders = [('User-agent',
                            'Mozilla/5.0 (X11; Linux i686) ApleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]
    rawData = mcOpener.open(realUrl).read()
    data = json.loads(rawData)
    mc_server_found = 'online' in data and data['online'] == 'true'
    if mc_server_found:
        mc_data_formatted = ('The server at {0} has {1} players and replied in {2} ms' + (
            '' if dynmapPort == '' else '\nSee map: ' + mcServer + ':' + dynmapPort)).format(
            mcServer + ':' + str(mcPort),
            data['players'],
            str(data['ping']))
    return mc_data_formatted, mc_server_found, mc_server_not_found_message
