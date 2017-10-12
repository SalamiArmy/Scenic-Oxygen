import base64
import json
import logging

from google.appengine.api import urlfetch

import add

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    request_text = str(message)
    repo_url, token = add.parse_repo_url_and_token(request_text)
    if add.getTokenValue(repo_url) == request_text.split(' ')[2]:
        remove_hook_response = remove_hook(repo_url, token)
        remove_commands(repo_url, token)
        bot.sendMessage(chat_id=chat_id, text=remove_hook_response)
    else:
        bot.sendMessage(chat_id=chat_id, text='The commands at ' + repo_url +
                                              ' have not been hooked or wrong token in request.')

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
                logging.info('Got command_data as ' + command_data)
                if 'name' in command_data and not command_data['name'] == '__init__.py':
                    add.setCommandCode(str(command_data['name']).replace('.py', ''), '')
            return ''
        else:
            return json_data['message']

def remove_hook(repo_url, token):
    hookID = add.getHookIDValue(repo_url)
    raw_data = urlfetch.fetch('https://api.github.com/repos/' + repo_url + '/hooks/' + hookID,
                              method=urlfetch.DELETE, headers={'Authorization': 'token ' + token})
    add.setTokenValue(repo_url, '')
    return raw_data.content