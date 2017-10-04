from google.appengine.ext import ndb
from google.appengine.api import urlfetch

class TokenValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')

def getTokenValue(repo_url):
    es = TokenValue.get_by_id(str(repo_url))
    if es:
        return es.currentValue
    return ''

# ================================

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    request_text = str(message)
    raw_data = urlfetch.fetch('https://api.github.com/repos/' + request_text.split(' ')[0] +'/' + request_text.split(' ')[1] +'/hooks',
                              "{\r\n  \"name\": \"web\",\r\n  \"active\": true,\r\n  \"config\": {\r\n    \"url\": \"" +
                              keyConfig.get('InternetShortcut', 'URL') +
                              "/github_webhook\",\r\n    \"content_type\": \"json\"\r\n  }\r\n}",
                              urlfetch.POST, {'Authorization': 'token ' + request_text.split(' ')[2]})
    bot.sendMessage(chat_id=chat_id, text=raw_data.content)