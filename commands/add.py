import io
import json

from google.appengine.api import urlfetch

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    request_text = str(message)
    update_commands(request_text)
    create_hook(bot, chat_id, keyConfig, request_text)

def update_commands(request_text):
    raw_data = urlfetch.fetch(url='https://api.github.com/repos/' +
                        request_text.split(' ')[0] + '/' +
                        request_text.split(' ')[1] +
                        '/contents/commands',
                        headers={'Authorization': 'token ' + request_text.split(' ')[2]})
    json_data = json.loads(raw_data.content)
    if (len(json_data) > 0):
        for command_data in json_data:
            if 'name' in command_data:
                raw_data = urlfetch.fetch(url='https://raw.githubusercontent.com/' +
                                    request_text.split(' ')[0] + '/' +
                                    request_text.split(' ')[1] +
                                    '/master/commands/' + command_data['name'],
                                    headers={'Authorization': 'token ' + request_text.split(' ')[2]})
                command_file = io.FileIO(command_data['name'], 'w')
                command_file.write(raw_data.content)

def create_hook(bot, chat_id, keyConfig, request_text):
    raw_data = urlfetch.fetch(
        'https://api.github.com/repos/' + request_text.split(' ')[0] + '/' + request_text.split(' ')[1] + '/hooks',
        "{\r\n  \"name\": \"web\",\r\n  \"active\": true,\r\n  \"config\": {\r\n    \"url\": \"" +
        keyConfig.get('InternetShortcut', 'URL') +
        "/github_webhook\",\r\n    \"content_type\": \"json\"\r\n  }\r\n}",
        urlfetch.POST, {'Authorization': 'token ' + request_text.split(' ')[2]})
    bot.sendMessage(chat_id=chat_id, text=raw_data.content)