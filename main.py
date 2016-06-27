import ConfigParser
import importlib
import json
import logging
import unittest
import urllib
import sys

import urllib2
import telegram

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import webapp2

import vocabs

BASE_URL = 'https://api.telegram.org/bot'

# Read keys.ini file at program start (don't forget to put your keys in there!)
keyConfig = ConfigParser.ConfigParser()
keyConfig.read(["keys.ini", "..\keys.ini"])

bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(
            BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(
            BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(
                BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        if 'message' in body:
            message = body['message']
            text = message.get('text')
            fr = message.get('from')
            user = fr['username'] \
                if 'username' in fr \
                else fr['first_name'] + ' ' + fr['last_name'] \
                if 'first_name' in fr and 'last_name' in fr \
                else fr['first_name'] if 'first_name' in fr \
                else 'Dave'
            chat = message['chat']
            chat_id = chat['id']

            if not text:
                logging.info('no text')
                return

            if text.startswith('/'):
                self.TryExecuteExplicitCommand(chat_id, user, text)
            else:
                if len(text) < 200:
                    self.TryParseIntent(chat_id, user, text)

    def TryExecuteExplicitCommand(self, chat_id, fr_username, text):
        split = text[1:].lower().split(" ", 1)
        try:
            mod = importlib.import_module('commands.' + split[0].lower().replace(bot.name.lower(), ""))
            mod.run(bot, keyConfig, chat_id, fr_username, split[1] if len(split) > 1 else '')
        except:
            print("Unexpected error running command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))

    def TryParseIntent(self, chat_id, fr_username, text):
        for intent in vocabs.engine.determine_intent(text):
            try:
                confidence_percent = intent.get('confidence', 0.0)*100
                if intent and (confidence_percent > 0 or bot.name in text):
                    if 'WeatherKeyword' in intent and 'Location' in intent:
                        import commands.getweather as getweather
                        getweather.run(bot, keyConfig, chat_id, fr_username, intent.get('Location'), confidence_percent)
                    if 'MusicVerb' in intent and 'Sound' in intent:
                        import commands.getsound as getsound
                        getsound.run(bot, keyConfig, chat_id, fr_username, intent.get('Sound'), confidence_percent)
                    if 'ImageVerb' in intent and 'Image' in intent:
                        import commands.get as get
                        intent_get = intent.get('Image')
                        if len(intent_get) > 4:
                            get.run(bot, keyConfig, chat_id, fr_username, intent_get, confidence_percent)
                    if 'QuestionKeyword' in intent:
                        vocabs.run_command_hierarchy(bot, keyConfig, chat_id, fr_username, text,
                                                     intent.get('WhoWhatHow') if 'WhoWhatHow' in intent else '',
                                                     confidence_percent)
            except:
                print("Unexpected error running command:" + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))


class RunTestsHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        testmodules = [
            'command_tests.test_bitcoin',
            'command_tests.test_cric',
            'command_tests.test_get',
            'command_tests.test_getbook',
            'command_tests.test_getfig',
            'command_tests.test_getgif',
            'command_tests.test_gethuge',
            'command_tests.test_gethugegif',
            'command_tests.test_getlyrics',
            'command_tests.test_getmovie',
            'command_tests.test_getquote',
            'command_tests.test_getshow',
            'command_tests.test_getvid',
            'command_tests.test_getweather',
            'command_tests.test_getxxx',
            'command_tests.test_giphy',
            'command_tests.test_iss',
            'command_tests.test_place',
            'command_tests.test_rand',
            'command_tests.test_torrent',
            'command_tests.test_translate',
            'command_tests.test_urban',
            'command_tests.test_wiki',
            'command_tests.test_define',
            'command_tests.test_getanswer',
            'command_tests.test_getgame',
            'command_tests.test_getsound',
            'command_tests.test_imgur',
            'command_tests.test_isis',
            'command_tests.test_launch',
            'command_tests.test_mc',
            'command_tests.test_reverseimage',
            'command_tests.test_define',
            'command_tests.test_getanswer',
            'command_tests.test_getgame',
            'command_tests.test_getsound',
            'command_tests.test_imgur',
            'command_tests.test_isis',
            'command_tests.test_launch',
            'command_tests.test_mc',
            'command_tests.test_reverseimage',
        ]
        suite = unittest.TestSuite()

        formattedResultText = ''
        for t in testmodules:
            try:
                getTest = unittest.defaultTestLoader.loadTestsFromName(t)
                suite.addTest(getTest)
            except:
                formattedResultText += "Unexpected error during import of module " + \
                                       t + ": " + str(sys.exc_info()[1]) + '\n'

        formattedResultText += str(unittest.TextTestRunner().run(suite))\
            .replace('<unittest.runner.TextTestResult ', '')\
            .replace('>', '')
        self.response.write(formattedResultText)


class WebCommandRunHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        text = self.request.get('text')
        if not text:
            self.response.write('Argument missing: \'text\'.')
            return
        chat_id = self.request.get('chat_id')
        if not chat_id:
            chat_id = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        if text.startswith('/'):
            WebhookHandler.TryExecuteExplicitCommand(chat_id, "Admin", text)
        else:
            WebhookHandler.TryParseIntent(chat_id, "Admin", text)

app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
    ('/run_tests', RunTestsHandler),
    ('/run', WebCommandRunHandler)
], debug=True)
