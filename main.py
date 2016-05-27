import ConfigParser
import importlib
import json
import logging
import unittest
import urllib
import sys

# standard app engine imports
import urllib2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import webapp2

BASE_URL = 'https://api.telegram.org/bot'

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
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        self.response.write(json.dumps(json.load(urllib2.urlopen(
            BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        self.response.write(json.dumps(json.load(urllib2.urlopen(
            BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
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

        update_id = body['update_id']
        message = body['message']
        text = message.get('text')
        fr = message.get('from')
        fr_username = fr['username']
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        if text.startswith('/'):
            split = text[1:].lower().split(" ", 1)
            try:
                mod = importlib.import_module('commands.' + split[0])
                mod.run(chat_id, fr_username, split[1] if len(split) > 1 else '')
            except:
                print("Unexpected error running command:", sys.exc_info()[1])
        else:
            if not text:
                print('Webhook body member missing: \'message\'.')
                return

            import vocabs.intend_getweather as intend_getweather
            try:
                intent = intend_getweather.get_intention(text)
                if intent != None:
                    import commands.getweather as getweather
                    getweather.run(chat_id, fr_username, intent.get('location'))
            except:
                print("Unexpected error running command:" + str(sys.exc_info()[1]))

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
        chatId = self.request.get('chat_id')
        if not chatId:
            keyConfig = ConfigParser.ConfigParser()
            keyConfig.read(["keys.ini", "..\keys.ini"])
            chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        if text.startswith('/'):
            split = text[1:].lower().split(" ", 1)
            mod = importlib.import_module('commands.' + split[0])
            try:
                requestText = split[1] if len(split) > 1 else ''
                mod.run(chatId, "Admin", requestText)
                self.response.write('Command ' + split[0] + ' ran with request text ' + requestText + ' successfully.')
            except:
                self.response.write("Unexpected error running command:" + str(sys.exc_info()[1]))
        else:
            if not text:
                self.response.write('Webhook body member missing: \'message\'.')
                return

            import vocabs.intend_getweather as intend_getweather
            try:
                intent = intend_getweather.get_intention(text)
                if intent is not None:
                    import commands.getweather as getweather
                    getweather.run(chatId, 'Admin', intent.get('Location'))
                    self.response.write('getting weather for ' + intent.get('Location'))
            except:
                self.response.write("Unexpected error running command:" + str(sys.exc_info()[1]))


class WebCommandIntentHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)

        message = self.request.get('message')
        if not message:
            self.response.write('Argument missing: \'message\'.')
            return

        if not message.startswith('/'):
            import vocabs.intend_getweather as intend_getweather
            try:
                intent = intend_getweather.get_intention(message)
                self.response.write(json.dumps(intent, indent=4))
            except:
                self.response.write("Unexpected error running command:" + str(sys.exc_info()[1]))
        else:
            self.response.write('Argument \'message\' value must not start with \'/\'.')

app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
    ('/run_tests', RunTestsHandler),
    ('/run', WebCommandRunHandler),
    ('/get_intention', WebCommandIntentHandler)
], debug=True)
