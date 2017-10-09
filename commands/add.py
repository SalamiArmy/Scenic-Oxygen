import json

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
    repo_url = request_text.split(' ')[0] + '/' + request_text.split(' ')[1]
    token = request_text.split(' ')[2]
    if getTokenValue(repo_url) == request_text.split(' ')[2]:
        bot.sendMessage(chat_id=chat_id, text='The commands at ' + repo_url + ' have already been hooked.')
    else:
        update_commands(repo_url, token)
        create_hook(bot, chat_id, keyConfig, request_text)

def update_commands(repo_url, token):
    raw_data = urlfetch.fetch(url='https://api.github.com/repos/' +
                                  repo_url + '/contents/commands',
                              headers={'Authorization': 'token ' + token})
    json_data = json.loads(raw_data.content)
    if len(json_data) > 0:
        for command_data in json_data:
            if 'name' in command_data:
                raw_data = urlfetch.fetch(url='https://raw.githubusercontent.com/' + repo_url +
                                              '/master/commands/' + command_data['name'],
                                          headers={'Authorization': 'token ' + token})
                if not command_data['name'] == '__init__.py':
                    setCommandCode(str(command_data['name']).replace('.py', ''), raw_data.content)

def create_hook(bot, chat_id, keyConfig, request_text):
    repo_url = request_text.split(' ')[0] + '/' + request_text.split(' ')[1]
    raw_data = urlfetch.fetch(
        'https://api.github.com/repos/' + repo_url + '/hooks',
        "{\r\n  \"name\": \"web\",\r\n  \"active\": true,\r\n  \"config\": {\r\n    \"url\": \"" +
        keyConfig.get('InternetShortcut', 'URL') +
        "/github_webhook\",\r\n    \"content_type\": \"json\"\r\n  }\r\n}",
        urlfetch.POST, {'Authorization': 'token ' + request_text.split(' ')[2]})
    setTokenValue(repo_url, request_text.split(' ')[2])
    bot.sendMessage(chat_id=chat_id, text=raw_data.content)