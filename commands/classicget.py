from google.cloud import logging
from google.auth import app_engine

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    PROJECT_IDS = [keyConfig.get('Logging', 'HEY-BOET'),
                   keyConfig.get('Logging', 'SCENIC-OXYGEN-113812'),
                   keyConfig.get('Logging', 'IMAGEBOET')]
    client = logging.Client(
        credentials=app_engine.Credentials(service_account_id=keyConfig.get('Google', 'GCSE_APP_ID'))
    )
    list_entries = client.list_entries(project_ids=PROJECT_IDS)
    bot.sendMessage(chat_id=chat_id, text=list_entries.num_results)