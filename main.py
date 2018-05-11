# coding=utf-8
import ConfigParser
import base64
import json
import logging
import urllib
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import imp
import endpoints

import telegram

# standard app engine imports
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import webapp2

from commands import start
from commands import login
from commands import add
from commands import remove

# Read keys.ini file at program start (don't forget to put your bot keys in there!)
keyConfig = ConfigParser.ConfigParser()
keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
keyConfig.read(["keys.ini", "..\keys.ini"])

# Telegram Bot Info
BASE_TELEGRAM_URL = 'https://api.telegram.org/bot'
telegramBot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))


# ================================

class AllWatchesValue(ndb.Model):
    # key name: AllWatches
    currentValue = ndb.StringProperty(indexed=False, default='')


# ================================

def addToAllWatches(command, chat_id, request=''):
    es = AllWatchesValue.get_or_insert('AllWatches')
    es.currentValue += ',' + str(chat_id) + ':' + command + (':' + request.replace(',', '%2C') if request != '' else '')
    es.put()


def AllWatchesContains(command, chat_id, request=''):
    es = AllWatchesValue.get_by_id('AllWatches')
    if es:
        return (',' + str(chat_id) + ':' + command + (
        ':' + request.replace(',', '%2C') if request != '' else '')) in str(es.currentValue) or \
               (str(chat_id) + ':' + command + (
               ':' + request.replace(',', '%2C') if request != '' else '') + ',') in str(es.currentValue)
    return False


def setAllWatchesValue(NewValue):
    es = AllWatchesValue.get_or_insert('AllWatches')
    es.currentValue = NewValue
    es.put()


def getAllWatches():
    es = AllWatchesValue.get_by_id('AllWatches')
    if es:
        return es.currentValue
    return ''


def removeFromAllWatches(watch):
    setAllWatchesValue(
        getAllWatches().replace(',' + watch.replace(',', '%2C'), '').replace(watch.replace(',', '%2C'), ''))


# ================================

class FacebookWebhookHandler(webapp2.RequestHandler):
    def get(self):
        verification_code = keyConfig.get('BotIDs', 'FACEBOOK_VERIFICATION_CODE')
        verify_token = self.request.get('hub.verify_token')
        if verification_code == verify_token:
            return self.request.get('hub.challenge')

    def post(self):
        urlfetch.set_default_fetch_deadline(120)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))
        if 'entry' in body:
            for entry in body['entry']:
                for message in entry['messaging']:
                    if 'message' in message and 'sender' in message:
                        facebookBot.send_text(message['sender']['id'], 'Hey Boet! I got ' + message['message']['text'])


class TelegramWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(
                BASE_TELEGRAM_URL + keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID') + '/setWebhook',
                urllib.urlencode({'url': url})))))

    def post(self):
        urlfetch.set_default_fetch_deadline(120)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        if 'message' in body or 'edited_message' in body:
            message = body['message'] if 'message' in body else body['edited_message']
            text = message.get('text')
            fr = message.get('from')
            user = fr['username'] \
                if 'username' in fr \
                else fr['first_name'] + ' ' + fr['last_name'] \
                if 'first_name' in fr and 'last_name' in fr \
                else fr['first_name'] if 'first_name' in fr \
                else 'Dave'
            if 'edited_message' in body:
                user += '(edited)'
            chat = message['chat']
            chat_id = chat['id']
            chat_type = chat['type']

            if text:
                self.TryExecuteExplicitCommand(chat_id, user, text, chat_type)
            else:
                logging.info('no text')
                return

    def TryExecuteExplicitCommand(self, chat_id, fr_username, text, chat_type):
        split = text[1:].lower().split(' ', 1)
        commandName = split[0].lower().replace(telegramBot.name.lower(), '')
        request_text = split[1] if len(split) > 1 else ''
        totalResults = 1
        if len(re.findall('^[a-z]+\d+$', commandName)) > 0:
            totalResults = re.findall('\d+$', commandName)[0]
            commandName = re.findall('^[a-z]+', commandName)[0]

        if commandName == 'add':
            return add.run(telegramBot, chat_id, fr_username, keyConfig, request_text)
        elif commandName == 'remove':
            return remove.run(telegramBot, chat_id, fr_username, keyConfig, request_text)
        elif commandName == 'login':
            return login.run(telegramBot, chat_id, fr_username, keyConfig)
        elif commandName == 'start':
            return start.run(telegramBot, chat_id, fr_username, keyConfig)
        else:
            mod = load_code_as_module(commandName)
            if mod:
                return mod.run(telegramBot, chat_id, fr_username, keyConfig, split[1] if len(split) > 1 else '',
                               totalResults)
            else:
                if chat_type == 'private':
                    errorMsg = 'I\'m sorry ' + (fr_username if not fr_username == '' else 'Dave') + \
                               ', I\'m afraid I do not recognize the ' + commandName + ' command.'
                    telegramBot.sendMessage(chat_id=chat_id, text=errorMsg)
                    return errorMsg


def result_is_not_error(result):
    error_starts_with = 'I\'m sorry '
    return result != None and result != '' and result[:len(error_starts_with)] != error_starts_with


class WebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        chat_id = self.request.get('chat_id')
        if chat_id == '':
            chat_id = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID')
        requestText = self.request.get('message')
        self.run_web_command(chat_id, requestText, 1)

    def run_web_command(self, chat_id, message, total_results):
        self.response.write(TelegramWebhookHandler().get_response(chat_id, 'private', message))
        if message[:3] == 'say':
            self.response.headers['Content-Type'] = 'audio/ogg'
        login.setPin(chat_id, '')
        login.setCount(chat_id, 0)


class Login(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(10)
        user = self.request.get('username')
        if user != '':
            self.response.write(TelegramWebhookHandler().TryExecuteExplicitCommand(user, 'Web', '/login', 'private'))
        else:
            self.response.write(keyConfig.get('InternetShortcut', 'URL') + '/login?username=')
        return self.response


class TriggerAllWatches(webapp2.RequestHandler):
    def get(self):
        AllWatches = getAllWatches()
        watches_split = AllWatches.split(',')
        if len(watches_split) >= 1:
            for watch in watches_split:
                print('got watch ' + watch)
                split = watch.split(':')
                if len(split) >= 2:
                    removeGet = split[1].replace('get', 'watch')
                    mod = load_code_as_module(removeGet)
                    chat_id = split[0]
                    request_text = (split[2] if len(split) == 3 else '')
                    removeCommaEncoding = request_text.replace('%2C', ',')
                    mod.run(telegramBot, chat_id, 'Watcher', keyConfig, removeCommaEncoding)
                else:
                    print('removing from all watches: ' + watch)
                    removeFromAllWatches(watch)


class GithubWebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(120)
        logging.info('request body:')
        logging.info(self.request.body)
        body = json.loads(self.request.body)
        if 'repository' in body and 'owner' in body['repository'] and 'login' in body['repository'][
            'owner'] and 'name' in body['repository']:
            repo_url = body['repository']['owner']['login'] + '/' + body['repository']['name']
            logging.info('Got repo_url as ' + repo_url)
            token = add.getTokenValue(repo_url)
            if token != '':
                response = self.update_commands(repo_url, token)
                if response == '':
                    commitMsg = ''
                    if 'commits' in body:
                        for commit in body['commits']:
                            commitMsg += '\n' + commit['message']
                        telegramBot.sendMessage(
                            chat_id=keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID'),
                            text='Admins, The Scenic-Oxygen Github Webhook ' +
                                 'has performed update for:\n' + commitMsg + '\nSee ' + body['compare'],
                            disable_web_page_preview=True)
                    else:
                        telegramBot.sendMessage(
                            chat_id=keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID'),
                            text='Admins, The Scenic-Oxygen Github Webhook ' +
                                 'has performed update for: ' + repo_url,
                            disable_web_page_preview=True)
                    self.response.write('Commands imported from ' + repo_url)
                else:
                    telegramBot.sendMessage(
                        chat_id=keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID'),
                        text='Admins, The Scenic-Oxygen Github Webhook ' +
                             'has failed to perform automatic update for ' + body['compare'] +
                             '\n' + response,
                        disable_web_page_preview=True)
                    self.response.write(response)
                    if response == 'Bad credentials':
                        raise endpoints.UnauthorizedException()
                    else:
                        raise endpoints.InternalServerErrorException()
            else:
                raise endpoints.InternalServerErrorException('Internal data store error: no token found ' +
                                                             'in the data store for ' + repo_url)
        else:
            self.response.write('unrecognized ' + json.dumps(body))
            raise endpoints.InternalServerErrorException()

    def update_commands(self, repo_url, token):
        github_contents_url = 'https://api.github.com/repos/' + repo_url + '/contents/commands'
        raw_data = urlfetch.fetch(url=github_contents_url,
                                  headers={'Authorization': 'Basic %s' % base64.b64encode(
                                      repo_url.split('/')[0] + ':' + token)})
        logging.info('Got raw_data as ' + raw_data.content)
        json_data = json.loads(raw_data.content)
        if json_data and len(json_data) > 0:
            if 'message' not in json_data:
                for command_data in json_data:
                    logging.info('Got command meta data as ')
                    logging.info(command_data)
                    if 'name' in command_data and \
                                    command_data['name'] != '__init__.py' and \
                                    command_data['name'] != 'add.py' and \
                                    command_data['name'] != 'classicget.py' and \
                                    command_data['name'] != 'remove.py' and \
                                    command_data['name'] != 'login.py' and \
                                    command_data['name'] != 'start.py':
                        raw_data = urlfetch.fetch(url='https://raw.githubusercontent.com/' + repo_url +
                                                      '/master/commands/' + command_data['name'],
                                                  headers={'Authorization': 'Basic %s' % base64.b64encode(
                                                      repo_url.split('/')[0] + ':' + token)})
                        add.setCommandCode(str(command_data['name']).replace('.py', ''), raw_data.content)
                return ''
            else:
                return json_data['message']


def load_code_as_module(module_name):
    if module_name != '':
        get_value_from_data_store = add.CommandsValue.get_by_id(module_name)
        if get_value_from_data_store:
            command_code = str(get_value_from_data_store.codeValue)
            if command_code != '':
                module = sys.modules.setdefault(module_name, imp.new_module(module_name))
                logging.info('begin loading module ' + module_name)
                exec command_code in module.__dict__
                return module
    return None


def ReloadAllCommands():
    es = add.CommandsValue.query().fetch()
    if len(es) > 0:
        for mod in es:
            command_name = str(mod.key._Key__pairs[0][1])
            load_code_as_module(command_name)


class GetCommandsHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(10)
        self.response.write(TelegramWebhookHandler().commandCascade)
        return self.response


app = webapp2.WSGIApplication([
    ('/allwatches', TriggerAllWatches),
    ('/login', Login),
    ('/list_commands', GetCommandsHandler),
    ('/telegram_webhook', TelegramWebhookHandler),
    ('/github_webhook', GithubWebhookHandler),
    ('/facebook_webhook', FacebookWebhookHandler),
    ('/webhook', WebhookHandler)
], debug=True)
