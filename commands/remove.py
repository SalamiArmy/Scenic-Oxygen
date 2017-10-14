import add

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