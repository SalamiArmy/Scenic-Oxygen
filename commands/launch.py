# coding=utf-8
import datetime
import json
import urllib2

import telegram

from dateutil import tz


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    formattedLaunchInfo = ''
    formattedLaunchInfo, has_results = get_launch_data(formattedLaunchInfo, keyConfig)
    if has_results:
        bot.sendMessage(chat_id=chat_id, text=formattedLaunchInfo,
                        parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any upcoming rocket launches.')


def get_launch_data(formattedLaunchInfo, keyConfig):
    rocketUrl = 'https://launchlibrary.net/1.1/launch/next/5'
    rocketUrlRequest = urllib2.Request(rocketUrl, headers={'User-Agent': "Magic Browser"})
    rocketData = json.load(urllib2.urlopen(rocketUrlRequest))
    has_results = 'launches' in rocketData
    if has_results:
        blast = rocketData['launches']
        formattedLaunchInfo = formatted_launch_message(blast, keyConfig)
    return formattedLaunchInfo, has_results


def formatted_launch_message(blast, keyConfig):
    b1 = blast[0]
    b2 = blast[1]
    b3 = blast[2]
    b4 = blast[3]
    b5 = blast[4]
    utc_zone = tz.tzutc()
    local_zone = tz.tzoffset('Offset TZ from server to local',
                             int(keyConfig.get('BotAdministration', 'Timezone')) * 60 * 60)
    blast1UtcTime = datetime.datetime.strptime(b1['net'], '%B %d, %Y %H:%M:%S %Z')
    if blast1UtcTime.hour >= '22' or blast1UtcTime.hour == 0:
        blast1UtcTime = blast1UtcTime + datetime.timedelta(days=1)
    blast1UtcTime = blast1UtcTime.replace(tzinfo=utc_zone)
    blast1LocalString = str(blast1UtcTime.astimezone(local_zone))
    blast1LocalTime = datetime.datetime.strptime(blast1LocalString, '%Y-%m-%d %H:%M:%S' +
                                                 keyConfig.get('BotAdministration', 'Timezone') + ':00')
    blast2UtcTime = datetime.datetime.strptime(b2['net'], '%B %d, %Y %H:%M:%S %Z')
    if blast2UtcTime.hour >= '22' or blast2UtcTime.hour == 0:
        blast2UtcTime = blast2UtcTime + datetime.timedelta(days=1)
    blast2UtcTime = blast2UtcTime.replace(tzinfo=utc_zone)
    blast2LocalString = str(blast2UtcTime.astimezone(local_zone))
    blast2LocalTime = datetime.datetime.strptime(blast2LocalString, '%Y-%m-%d %H:%M:%S' +
                                                 keyConfig.get('BotAdministration', 'Timezone') + ':00')
    blast3UtcTime = datetime.datetime.strptime(b3['net'], '%B %d, %Y %H:%M:%S %Z')
    if blast3UtcTime.hour >= '22' or blast3UtcTime.hour == 0:
        blast3UtcTime = blast3UtcTime + datetime.timedelta(days=1)
    blast3UtcTime = blast3UtcTime.replace(tzinfo=utc_zone)
    blast3LocalString = str(blast3UtcTime.astimezone(local_zone))
    blast3LocalTime = datetime.datetime.strptime(blast3LocalString, '%Y-%m-%d %H:%M:%S' +
                                                 keyConfig.get('BotAdministration', 'Timezone') + ':00')
    blast4UtcTime = datetime.datetime.strptime(b4['net'], '%B %d, %Y %H:%M:%S %Z')
    if blast4UtcTime.hour >= '22' or blast4UtcTime.hour == 0:
        blast4UtcTime = blast4UtcTime + datetime.timedelta(days=1)
    blast4UtcTime = blast4UtcTime.replace(tzinfo=utc_zone)
    blast4LocalString = str(blast4UtcTime.astimezone(local_zone))
    blast4LocalTime = datetime.datetime.strptime(blast4LocalString, '%Y-%m-%d %H:%M:%S' +
                                                 keyConfig.get('BotAdministration', 'Timezone') + ':00')
    blast5UtcTime = datetime.datetime.strptime(b5['net'], '%B %d, %Y %H:%M:%S %Z')
    if blast5UtcTime.hour >= '22' or blast5UtcTime.hour == 0:
        blast5UtcTime = blast5UtcTime + datetime.timedelta(days=1)
    blast5UtcTime = blast5UtcTime.replace(tzinfo=utc_zone)
    blast5LocalString = str(blast5UtcTime.astimezone(local_zone))
    blast5LocalTime = datetime.datetime.strptime(blast5LocalString, '%Y-%m-%d %H:%M:%S' +
                                                 keyConfig.get('BotAdministration', 'Timezone') + ':00')
    formattedLaunchInfo = 'Upcoming Rocket Launches:\n\n' + \
                          str(blast1LocalTime) + \
                          '\n*' + b1['name'] + \
                          '*\nLaunching from ' + ('[' if b1['location']['pads'][0]['mapURL'] != '' else '') + \
                          b1['location']['pads'][0]['name'] + \
                          ('](' + b1['location']['pads'][0]['mapURL'] + ')' if b1['location']['pads'][0][
                                                                                   'mapURL'] != '' else '') + \
                          ('\nWatch live at ' + b1['vidURL'] if 'vidURL' in b1 and b1['vidURL'] != '' and b1[
                                                                                                              'vidURL'] != None else '') + '\n\n' + \
                          str(blast2LocalTime) + \
                          '\n*' + b2['name'] + \
                          '*\nLaunching from ' + ('[' if b2['location']['pads'][0]['mapURL'] != '' else '') + \
                          b2['location']['pads'][0]['name'] + \
                          ('](' + b2['location']['pads'][0]['mapURL'] + ')' if b2['location']['pads'][0][
                                                                                   'mapURL'] != '' else '') + \
                          ('\nWatch live at ' + b2['vidURL'] if 'vidURL' in b2 and b2['vidURL'] != '' and b2[
                                                                                                              'vidURL'] != None else '') + '\n\n' + \
                          str(blast3LocalTime) + \
                          '\n*' + b3['name'] + \
                          '*\nLaunching from ' + ('[' if b3['location']['pads'][0]['mapURL'] != '' else '') + \
                          b3['location']['pads'][0]['name'] + \
                          ('](' + b3['location']['pads'][0]['mapURL'] + ')' if b3['location']['pads'][0][
                                                                                   'mapURL'] != '' else '') + \
                          ('\nWatch live at ' + b3['vidURL'] if 'vidURL' in b3 and b3['vidURL'] != '' and b3[
                                                                                                              'vidURL'] != None else '') + '\n\n' + \
                          str(blast4LocalTime) + \
                          '\n*' + b4['name'] + \
                          '*\nLaunching from ' + ('[' if b4['location']['pads'][0]['mapURL'] != '' else '') + \
                          b4['location']['pads'][0]['name'] + \
                          ('](' + b4['location']['pads'][0]['mapURL'] + ')' if b4['location']['pads'][0][
                                                                                   'mapURL'] != '' else '') + \
                          ('\nWatch live at ' + b4['vidURL'] if 'vidURL' in b4 and b4['vidURL'] != '' and b4[
                                                                                                              'vidURL'] != None else '') + '\n\n' + \
                          str(blast5LocalTime) + \
                          '\n*' + b5['name'] + \
                          '*\nLaunching from ' + ('[' if b5['location']['pads'][0]['mapURL'] != '' else '') + \
                          b5['location']['pads'][0]['name'] + \
                          ('](' + b5['location']['pads'][0]['mapURL'] + ')' if b5['location']['pads'][0][
                                                                                   'mapURL'] != '' else '') + \
                          ('\nWatch live at ' + b5['vidURL'] if 'vidURL' in b5 and b5['vidURL'] != '' and b5[
                                                                                                              'vidURL'] != None else '')
    return formattedLaunchInfo