# coding=utf-8
import ConfigParser
import os

import telegram
#reverse image search imports:
from bs4 import BeautifulSoup
from StringIO import StringIO
import pycurl, json
import certifi


def run(chat_id, user, message):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()


    code = retrieve_google_image_search_results(requestText)
    jsonResults = json.loads(google_image_results_parser(code))
    resultsText = ''
    if 'result_qty' in jsonResults and len(jsonResults['result_qty']) > 0:
        for jsonResult in jsonResults['result_qty']:
            resultsText += jsonResult + '\n'
    if 'title' in jsonResults and len(jsonResults['title']) > 0:
        for jsonResult in jsonResults['title']:
            resultsText += jsonResult + '\n'
    if 'description' in jsonResults and len(jsonResults['description']) > 0:
        for jsonResult in jsonResults['description']:
            resultsText += (jsonResult[jsonResult.index('-') + 2:] + '\n' if '-' in jsonResult else '')
    if 'links' in jsonResults and len(jsonResults['links']) > 0:
        for jsonResult in jsonResults['links']:
            resultsText += jsonResult + '\n'
    resultLinks = code[code.index('Search Results'):].split('href=')
    for resultLink in resultLinks[1:]:
        resultLink = resultLink[1:]
        foundLink = resultLink[:resultLink.index('"')]
        if foundLink != '#' and \
                        foundLink != 'javascript:;' and \
                        foundLink != 'javascript:void(0)' and \
                        foundLink != '//www.google.com/intl/en/policies/privacy/?fg=1' and \
                        foundLink != '//www.google.com/intl/en/policies/terms/?fg=1' and \
                        len(foundLink) < 50:
            resultsText += foundLink + '\n'
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    userWithCurrentChatAction = chat_id
    urlForCurrentChatAction = resultsText
    bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)


# retrieves reverse search html for processing. This actually does reverse image lookups
def retrieve_google_image_search_results(image_url):
    returned_code = StringIO()
    full_url = "https://www.google.com/searchbyimage?&image_url=" + image_url
    conn = pycurl.Curl()
    conn.setopt(conn.URL, str(full_url))
    conn.setopt(conn.CAINFO, certifi.where())
    conn.setopt(conn.FOLLOWLOCATION, 1)
    conn.setopt(conn.USERAGENT, "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11")
    conn.setopt(conn.WRITEFUNCTION, returned_code.write)
    conn.perform()
    conn.close()
    return returned_code.getvalue()

# Parses reverse search html and assigns to array using beautifulsoup
def google_image_results_parser(code):
    soup = BeautifulSoup(code, "html.parser")

    # initialize 2d array
    whole_array = {"links":[],
                   "description":[],
                   "title":[],
                   "result_qty":[]}

    # Links for all the search results
    for li in soup.findAll("li", attrs={"class":"g"}):
        sLink = li.find("a")
        whole_array["links"].append(sLink["href"])

    # Search Result Description
    for desc in soup.findAll("span", attrs={"class":"st"}):
        whole_array["description"].append(desc.get_text())

    # Search Result Title
    for title in soup.findAll("h3", attrs={"class":"r"}):
        whole_array["title"].append(title.get_text())

    # Number of results
    for result_qty in soup.findAll("div", attrs={"id":"resultStats"}):
        whole_array["result_qty"].append(result_qty.get_text())

    return json.dumps(whole_array)