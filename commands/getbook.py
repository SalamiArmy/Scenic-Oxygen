# coding=utf-8
import json
import urllib
from bs4 import BeautifulSoup

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
    book_title = book_title.replace(',', '')
    allPreviousLinks = getPreviouslySeenBooksValue(chat_id)
    if ',' + book_title + ',' in allPreviousLinks or \
            allPreviousLinks.startswith(book_title + ',') or  \
            allPreviousLinks.endswith(',' + book_title) or  \
            allPreviousLinks == book_title:
        return True
    return False


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    args = {'key': keyConfig.get('GoodReads', 'KEY'),
            'search[field]': 'all',
            'safe': 'off',
            'q': requestText,
            'page': 1}
    realUrl = 'https://www.goodreads.com/search/index.xml?' + urllib.urlencode(args)
    raw_xml_data = urllib.urlopen(realUrl).read()
    bookTitles, ratings, total_ratings, bookIDs, bookDescriptions = book_results_parser(raw_xml_data, keyConfig)

    offset = 0
    while int(offset) < int(totalResults) and offset < len(bookTitles):
        bookTitle = bookTitles[offset]
        if not wasPreviouslySeenBook(chat_id, bookTitle):
            bookData = FormatDesc(bookDescriptions[offset])
            url = 'https://www.goodreads.com/book/show/' + bookIDs[offset] + '-' + requestText.replace(' ', '-')
            rating = ratings[offset]
            total_rating = total_ratings[offset]
            bot.sendMessage(chat_id=chat_id, text=(user + ': *' if not user == '' else '*') + bookTitle +
                                                  (' ' + str(offset+1) + ' of ' + str(totalResults) if int(totalResults) > 1 else '') + '*\n' +
                                                  ('_Rated ' + rating.encode('utf-8') + ' out of 5 by ' +
                                                  total_rating + ' GoodReads users._\n' if rating.encode('utf-8') == '0' else '')
                                                  + bookData + '\n' + url,
                            parse_mode='Markdown')
            addPreviouslySeenBooksValue(chat_id, bookTitle)
        offset += 1
    if offset == len(bookTitles):
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find any  books' +
                                              (' that you haven\'t already seen' if len(bookTitles) > 0 and offset > 0 else '') +
                                              ' for ' + requestText.encode('utf-8') + '.')

def FormatDesc(Desc):
    return Desc.replace('<br />', '\n')\
        .replace('<i>', '_')\
        .replace('</i>', '_')\
        .replace('<em>', '*')\
        .replace('</em>', '*')\
        .replace('<p>', '\n')\
        .replace('</p>', '\n')\
        .replace('<b>', '*')\
        .replace('</b>', '*')



def book_results_parser(rawMarkup, keyConfig):
    soup = BeautifulSoup(rawMarkup)
    bookDescriptions = []
    bookIDs = []
    bookTitles = []
    bookAverageRatings = []
    bookRatingsCounts = []
    for book in soup.findAll('best_book'):
        bookId = book.findAll('id')[0].string
        realUrl = 'https://www.goodreads.com/book/show.xml?key=' + keyConfig.get('GoodReads', 'KEY') + '&id=' + bookId
        raw_xml_object = urllib.urlopen(realUrl).read()
        data = BeautifulSoup(raw_xml_object)
        bookIDs.append(data.findAll('id')[0].string)
        bookDescriptions.append(data.findAll('description')[0].string if data.findAll('description')[0].string != None else '')
        bookTitles.append(data.findAll('title')[0].string)
        bookAverageRatings.append(data.findAll('average_rating')[0].string)
        bookRatingsCounts.append(data.findAll('ratings_count')[0].string)
    return bookTitles, bookAverageRatings, bookRatingsCounts, bookIDs, bookDescriptions