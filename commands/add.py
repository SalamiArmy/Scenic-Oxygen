import base64
import json
import logging

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

class TokenValue(ndb.Model):
    # key name: str(repo_url)
    currentValue = ndb.StringProperty(indexed=False, default='')

def getTokenValue(repo_url):
    es = TokenValue.get_by_id(str(repo_url))
    if es:
        return str(es.currentValue)
    return ''

def setTokenValue(repo_url, NewValue):
    es = TokenValue.get_or_insert(str(repo_url))
    logging.info('setting token value for ' + str(repo_url) + ' to ' + str(NewValue))
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
            setTokenValue(repo_url, request_token)
            update_commands(repo_url, request_token)
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


def update_commands(repo_url, token):
    github_contents_url = 'https://api.github.com/repos/' + repo_url + '/contents/commands'
    logging.info('Executing github hook request against ' + github_contents_url +
                 ' using the following basic auth header: ' +
                 'Basic %s' % base64.b64encode(repo_url.split('/')[0] + ':' + token))
    raw_data = urlfetch.fetch(url=github_contents_url,
                              headers={'Authorization': 'Basic %s' % base64.b64encode(repo_url.split('/')[0] + ':' + token)})
    logging.info('Got raw_data as ' + raw_data.content)
    json_data = json.loads(raw_data.content)
    if json_data and len(json_data) > 0:
        if 'message' not in json_data:
            logging.info('more than 0 commands found!')
            for command_data in json_data:
                logging.info('Got command meta data as ')
                logging.info(command_data)
                if 'name' in command_data and \
                                command_data['name'] != '__init__.py' and \
                                command_data['name'] != 'add.py' and \
                                command_data['name'] != 'remove.py' and \
                                command_data['name'] != 'login.py' and \
                                command_data['name'] != 'start.py':
                    raw_data = urlfetch.fetch(url='https://raw.githubusercontent.com/' + repo_url +
                                                  '/master/commands/' + command_data['name'],
                                              headers={'Authorization': 'Basic %s' % base64.b64encode(repo_url.split('/')[0] + ':' + token)})
                    setCommandCode(str(command_data['name']).replace('.py', ''), raw_data.content)
            return ''
        else:
            return json_data['message']

def remove_commands(repo_url, token):
    logging.info('Executing github hook request using the following basic auth header: ' +
                 'Basic %s' % base64.b64encode(repo_url.split('/')[0] + ':' + token))
    raw_data = urlfetch.fetch(url='https://api.github.com/repos/' +
                                  repo_url + '/contents/commands',
                              headers={'Authorization': 'Basic %s' % base64.b64encode(repo_url.split('/')[0] + ':' + token)})
    logging.info('Got raw_data as ' + raw_data.content)
    json_data = json.loads(raw_data.content)
    if json_data and len(json_data) > 0:
        if 'message' not in json_data:
            logging.info('more than 0 commands found!')
            for command_data in json_data:
                logging.info('Got command_data as ')
                logging.info(command_data)
                if 'name' in command_data and not command_data['name'] == '__init__.py' and \
                        not command_data['name'] == 'add.py' and \
                        not command_data['name'] == 'remove.py' and \
                        not command_data['name'] == 'login.py' and \
                        not command_data['name'] == 'start.py':
                    setCommandCode(str(command_data['name']).replace('.py', ''), '')
            return ''
        else:
            return json_data['message']

def create_hook(bot, chat_id, keyConfig, repo_url, token):
    raw_data = urlfetch.fetch(
        'https://api.github.com/repos/' + repo_url + '/hooks',
        "{\r\n  \"name\": \"web\",\r\n  \"active\": true,\r\n  \"config\": {\r\n    \"url\": \"" +
        keyConfig.get('InternetShortcut', 'URL') +
        "/github_webhook\",\r\n    \"content_type\": \"json\"\r\n  }\r\n}",
        urlfetch.POST, {'Authorization': 'token ' + token})
    json_data = json.loads(raw_data.content)
    if raw_data.status_code == 200:
        if 'id' in json_data:
            setHookIDValue(repo_url, json_data['id'])
            bot.sendMessage(chat_id=chat_id, text='Webhook created:\n' + raw_data)
    else:
        if 'message' in json_data:
            bot.sendMessage(chat_id=chat_id, text=json_data['message'])
        if 'errors' in json_data:
            for error in json_data['errors']:
                bot.sendMessage(chat_id=chat_id, text=error['message'])

def remove_hook(repo_url, token):
    hookID = getHookIDValue(repo_url)
    raw_data = urlfetch.fetch('https://api.github.com/repos/' + repo_url + '/hooks/' + hookID,
                              method=urlfetch.DELETE, headers={'Authorization': 'token ' + token})
    setHookIDValue(repo_url, '')
    return raw_data.content
