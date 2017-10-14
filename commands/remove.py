import base64
import add
import json
import logging

from google.appengine.api import urlfetch

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    request_text = str(message)
    repo_url, token = add.parse_repo_url_and_token(request_text)
    existing_token = add.getTokenValue(repo_url)
    request_token = request_text.split(' ')[2]
    if request_token != '':
        if existing_token != '':
            if existing_token == request_token:
                if add.remove_hook(bot, chat_id, keyConfig, repo_url, token):
                    add.setTokenValue(repo_url, '')
                    add.remove_commands(repo_url, token)
            else:
                bot.sendMessage(chat_id=chat_id, text='Wrong token in request.')
        else:
            bot.sendMessage(chat_id=chat_id, text='The commands at ' + repo_url +
                                                  ' have not been hooked.')
    else:
        bot.sendMessage(chat_id=chat_id, text='A Github token is required. ' +
                                              'With permission to list all commands in the repo ' +
                                              'and delete hooks.')

def remove_commands(self, repo_url, token):
    raw_data = urlfetch.fetch(url='https://api.github.com/repos/' +
                                  repo_url + '/contents/commands',
                              headers={'Authorization': 'Basic %s' % base64.b64encode(
                                  repo_url.split('/')[0] + ':' + token)})
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
                    add.setCommandCode(str(command_data['name']).replace('.py', ''), '')
            return ''
        else:
            return json_data['message']