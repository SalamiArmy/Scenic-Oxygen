# coding=utf-8
import json
import urllib

import telegram

from commands import retry_on_telegram_error


def run(bot, chat_id, user, keyConfig, message):
    requestText = message.replace(bot.name, "").strip()

    from goodreads import client
    gc = client.GoodreadsClient('10Ue8n1lsEjQplndZfcvsA', 'fWaEQmDQipgUVdXttQx1NvHPzvUUoVoAMFUR6ZQOU')
    books = gc.search_books(requestText)

    if len(books) > 0:
        bookTitle = books[0].title
        bookData = books[0].description
        image_url = books[0].image_url
        url = books[0].link
        return bot.sendMessage(chat_id=chat_id, text=(user + ': *' if not user == '' else '*') + bookTitle + '*\n' +
                                                     bookData + '\n' +
                                                     url,
                               parse_mode='Markdown')
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                              ', I\'m afraid I can\'t find any books for ' +\
                                              requestText.encode('utf-8') + '.')
