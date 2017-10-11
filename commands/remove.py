import logging

from google.appengine.api import urlfetch

import main
add = main.load_code_as_module('add')

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    request_text = str(message)
    repo_url, token = add.parse_repo_url_and_token(request_text)
    if add.getTokenValue(repo_url) == request_text.split(' ')[2]:
        remove_hook(bot, chat_id, keyConfig, repo_url)
        bot.sendMessage(chat_id=chat_id, text='The commands at ' + repo_url + ' have already been hooked.')
    else:
        bot.sendMessage(chat_id=chat_id, text='The commands at ' + repo_url +
                                              ' have not been hooked or wrong token in request.')

def remove_hook(bot, chat_id, keyConfig, repo_url, token):
    hookID = add.getHookIDValue(repo_url)
    raw_data = urlfetch.fetch('https://api.github.com/repos/' + repo_url + '/hooks/' + hookID,
                              method=urlfetch.DELETE, headers={'Authorization': 'token ' + token})
    add.setTokenValue(repo_url, '')
    bot.sendMessage(chat_id=chat_id, text=raw_data.content)