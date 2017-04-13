# coding=utf-8
import json
import urllib2

from bs4 import BeautifulSoup


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    code = retrieve_google_image_search_results(requestText)
    parsedCode = google_image_results_parser(code)
    if parsedCode[:len("Error: ")] != "Error: ":
        jsonResults = json.loads(parsedCode)
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
        if resultsText:
            bot.sendMessage(chat_id=chat_id, text=resultsText, disable_web_page_preview=True)
            return True
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                  ', I\'m afraid I can\'t find any reverse image results for ' + \
                                                  requestText.encode('utf-8'))
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              " there was an " + parsedCode)


# retrieves reverse search html for processing. This spoofs a fake user-agent, so it's morally dubious.
def retrieve_google_image_search_results(image_url):
    searchUrl = 'https://www.google.com/searchbyimage?&image_url=' + image_url
    searchOpener = urllib2.build_opener()
    searchOpener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) ApleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]
    return searchOpener.open(searchUrl).read()

# Parses reverse search html and assigns to array using beautifulsoup
def google_image_results_parser(code):
    soup = BeautifulSoup(code, 'html.parser')

    for card in soup.findAll('div', attrs={'class': 'card-section'}):
        return "Error: " + card.get_text()

    # initialize 2d array
    whole_array = {'links': [],
                   'description': [],
                   'title': [],
                   'result_qty': []}

    # Links for all the search results
    for li in soup.findAll('li', attrs={'class': 'g'}):
        sLink = li.find('a')
        whole_array['links'].append(sLink['href'])

    # Search Result Description
    for desc in soup.findAll('span', attrs={'class': 'st'}):
        whole_array['description'].append(desc.get_text())

    # Search Result Title
    for title in soup.findAll('h3', attrs={'class': 'r'}):
        whole_array['title'].append(title.get_text())

    # Number of results
    for result_qty in soup.findAll('div', attrs={'id': 'resultStats'}):
        whole_array['result_qty'].append(result_qty.get_text())

    return json.dumps(whole_array)
