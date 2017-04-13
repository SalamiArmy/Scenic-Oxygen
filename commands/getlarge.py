# coding=utf-8
from commands import get


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': "image",
            'safe': "off",
            'q': requestText,
            "imgSize": "large"}
    if totalResults > 1:
        get.Send_Images(bot, chat_id, user, requestText, args, totalResults)
    else:
        get.Send_First_Valid_Image(bot, chat_id, user, requestText, args)


