from google.cloud import logging
from google.auth import app_engine

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    client = logging.Client(
        project=keyConfig.get('Logging', 'APP_ENGINE_PROJECT_KEY'),
        credentials=app_engine.Credentials()
    )
    list_entries = client.list_entries()
    bot.sendMessage(chat_id=chat_id, text=list_entries.num_results)