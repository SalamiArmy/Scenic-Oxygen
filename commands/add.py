import base64
import json
import logging

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

class TokenValue(ndb.Model):
    # key name: str(repo_url)
    currentValue = ndb.StringProperty(indexed=False, default='')

def getTokenValue(repo_url):
    es = TokenValue.get_by_id(str(repo_url).lower())
    if es:
        return str(es.currentValue)
    return ''

def setTokenValue(repo_url, NewValue):
    es = TokenValue.get_or_insert(str(repo_url).lower())
    logging.info('setting token value for ' + str(repo_url).lower() + ' to ' + str(NewValue))
    es.currentValue = str(NewValue)
    es.put()

class HookIDValue(ndb.Model):
    # key name: str(repo_url)
    currentValue = ndb.StringProperty(indexed=False, default='')

def getHookIDValue(repo_url):
    es = HookIDValue.get_by_id(str(repo_url))
    if es:
        return str(es.currentValue)
    return ''

def setHookIDValue(repo_url, NewValue):
    es = HookIDValue.get_or_insert(str(repo_url))
    es.currentValue = str(NewValue)
    es.put()

class CommandsValue(ndb.Model):
    # key name: command_name
    codeValue = ndb.TextProperty(indexed=False, default='')

def setCommandCode(command_name, NewValue):
    es = CommandsValue.get_or_insert(command_name)
    es.codeValue = str(NewValue)
    es.put()

# ================================

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    request_text = str(message)
    repo_url, request_token = parse_repo_url_and_token(request_text)
    stored_token = getTokenValue(repo_url)
    if request_token != '':
        if stored_token != request_token:
            create_hook(bot, chat_id, keyConfig, repo_url, request_token)
        else:
            bot.sendMessage(chat_id=chat_id, text='The commands at ' + repo_url + ' have already been hooked.')
    else:
        bot.sendMessage(chat_id=chat_id, text='A Github token is required. ' +
                                              'With permission to read all commands in the repo ' +
                                              'and create hooks.')

def parse_repo_url_and_token(request_text):
    repo_url = request_text.split(' ')[0] + '/' + request_text.split(' ')[1]
    token = request_text.split(' ')[2]
    return repo_url, token

def create_hook(bot, chat_id, keyConfig, repo_url, token):
    setTokenValue(repo_url, token)
    raw_data = urlfetch.fetch(
        'https://api.github.com/repos/' + repo_url + '/hooks',
        "{\r\n  \"name\": \"web\",\r\n  \"active\": true,\r\n  \"config\": {\r\n    \"url\": \"" +
        keyConfig.get('InternetShortcut', 'URL') +
        "/github_webhook\",\r\n    \"content_type\": \"json\"\r\n  }\r\n}",
        urlfetch.POST, {'Authorization': 'token ' + token})
    json_data = json.loads(raw_data.content)
    logging.info('webhook create api call status code: ' + str(raw_data.status_code))
    if raw_data.status_code >= 200 and raw_data.status_code < 300:
        if 'id' in json_data:
            setHookIDValue(repo_url, json_data['id'])
            bot.sendMessage(chat_id=chat_id, text='Webhook created:\n' + raw_data.content)
            return True
        else:
            bot.sendMessage(chat_id=chat_id, text='Webhook creation failed:\n' + raw_data.content)
            return False
    else:
        if 'message' in json_data:
            bot.sendMessage(chat_id=chat_id, text=json_data['message'])
        else:
            bot.sendMessage(chat_id=chat_id, text='Webhook creation failed:\n' + raw_data.content)
        if 'errors' in json_data:
            for error in json_data['errors']:
                bot.sendMessage(chat_id=chat_id, text=error['message'])
        return False

def remove_hook(bot, chat_id, repo_url, token, hookID):
    raw_data = urlfetch.fetch('https://api.github.com/repos/' + repo_url + '/hooks/' + hookID,
                              method=urlfetch.DELETE, headers={'Authorization': 'token ' + token})
    logging.info('webhook remove api call status code: ' + str(raw_data.status_code))
    if raw_data.status_code >= 200 and raw_data.status_code < 300:
        setHookIDValue(repo_url, '')
        bot.sendMessage(chat_id=chat_id, text='Webhook removed.')
        return True
    else:
        return False
