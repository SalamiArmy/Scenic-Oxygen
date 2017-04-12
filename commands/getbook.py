# coding=utf-8
from google.appengine.ext import ndb

CommandName = 'get'

class SeenBooks(ndb.Model):
    # key name: get:str(chat_id)
    allPreviousSeenBooks = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenBooksValue(chat_id, NewValue):
    es = SeenBooks.get_or_insert(CommandName + ':' + str(chat_id))
    es.allPreviousSeenBooks = NewValue.encode('utf-8')
    es.put()

def addPreviouslySeenBooksValue(chat_id, NewValue):
    es = SeenBooks.get_or_insert(CommandName + ':' + str(chat_id))
    if es.allPreviousSeenBooks == '':
        es.allPreviousSeenBooks = NewValue.encode('utf-8').replace(',', '')
    else:
        es.allPreviousSeenBooks += ',' + NewValue.encode('utf-8').replace(',', '')
    es.put()

def getPreviouslySeenBooksValue(chat_id):
    es = SeenBooks.get_or_insert(CommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousSeenBooks.encode('utf-8')
    return ''

def wasPreviouslySeenBook(chat_id, book_title):
    allPreviousLinks = getPreviouslySeenBooksValue(chat_id)
    if ',' + book_title + ',' in allPreviousLinks or \
            allPreviousLinks.startswith(book_title + ',') or  \
            allPreviousLinks.endswith(',' + book_title) or  \
            allPreviousLinks == book_title:
        return True
    return False


def run(bot, chat_id, user, keyConfig, message):
    requestText = message.replace(bot.name, "").strip()

    from goodreads import client
    gc = client.GoodreadsClient(keyConfig.get('GoodReads', 'KEY'), keyConfig.get('GoodReads', 'SECRET'))
    books = gc.search_books(requestText)

    offset = 0
    while offset < len(books):
        book = books[offset]
        offset += 1
        bookTitle = book.title
        if not wasPreviouslySeenBook(chat_id, bookTitle):
            bookData = book.description
            url = book.link
            rating = book.average_rating
            bot.sendMessage(chat_id=chat_id, text=(user + ': *' if not user == '' else '*') + bookTitle + '*\n' +
                                                  '_Rated ' + rating.encode('utf-8') + ' out of 5_\n' + bookData +
                                                  url,
                            parse_mode='Markdown')
            addPreviouslySeenBooksValue(chat_id, bookTitle)
            break
    if offset == len(books):
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find any books' +
                                              (' that you haven\'t already seen' if len(books) > 0 and offset > 0 else '') +
                                              ' for ' + requestText.encode('utf-8') + '.')

def FormatDesc(Desc):
    return Desc.replace('<br />', '\n').replace('<i>', '_').replace('</i>', '_')

