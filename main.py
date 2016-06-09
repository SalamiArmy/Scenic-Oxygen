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
            self.TryParseIntent(chat_id, user, text)

    def TryExecuteExplicitCommand(self, chat_id, fr_username, text):
        split = text[1:].lower().split(" ", 1)
        try:
            mod = importlib.import_module('commands.' + split[0])
            mod.run(bot, keyConfig, chat_id, fr_username, split[1] if len(split) > 1 else '')
        except:
            print("Unexpected error running command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))

    def TryParseIntent(self, chat_id, fr_username, text):
        import vocabs
        try:
            intent = vocabs.engine.determine_intent(text)
        except:
            print("Unexpected error parsing intentions: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
        try:
            getIntention = next(intent)
            while getIntention and getIntention.get('confidence') > 0:
                if 'WeatherKeyword' in getIntention and 'Location' in getIntention:
                    import commands.getweather as getweather
                    getweather.run(bot, keyConfig, chat_id, fr_username, getIntention.get('Location'))
                if 'MusicVerb' in getIntention and 'Sound' in getIntention:
                    import commands.getsound as getsound
                    getsound.run(bot, keyConfig, chat_id, fr_username, getIntention.get('Sound'))
                if 'ImageVerb' in getIntention and 'Image' in getIntention:
                    import commands.get as get
                    get.run(bot, keyConfig, chat_id, fr_username, getIntention.get('Image'))
                getIntention = next(intent)
        except:
            print("Unexpected error running command:" + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))


class RunTestsHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        testmodules = [
            'tests.test_bitcoin',
            'tests.test_cric',
            'tests.test_get',
            'tests.test_getbook',
            'tests.test_getfig',
            'tests.test_getgif',
            'tests.test_gethuge',
            'tests.test_gethugegif',
            'tests.test_getlyrics',
            'tests.test_getmovie',
            'tests.test_getquote',
            'tests.test_getshow',
            'tests.test_getvid',
            'tests.test_getweather',
            'tests.test_getxxx',
            'tests.test_giphy',
            'tests.test_iss',
            'tests.test_place',
            'tests.test_rand',
            'tests.test_torrent',
            'tests.test_translate',
            'tests.test_urban',
            'tests.test_wiki',
            'tests.test_define',
            'tests.test_getanswer',
            'tests.test_getgame',
            'tests.test_getsound',
            'tests.test_imgur',
            'tests.test_isis',
            'tests.test_launch',
            'tests.test_mc',
            'tests.test_reverseimage',
            'tests.test_define',
            'tests.test_getanswer',
            'tests.test_getgame',
            'tests.test_getsound',
            'tests.test_imgur',
            'tests.test_isis',
            'tests.test_launch',
            'tests.test_mc',
            'tests.test_reverseimage',
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
