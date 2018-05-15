# coding=utf-8

def get_command_code():
    return """# coding=utf-8
from threading import Thread
import json
import string
import urllib
import main

import sys

import io

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

retry_on_telegram_error = main.load_code_as_module('retry_on_telegram_error')

CommandName = 'get'

class WhosSeenImageUrls(ndb.Model):
    # key name: ImageUrl
    whoseSeenImage = ndb.StringProperty(indexed=False, default='')

# ================================

def setPreviouslySeenImagesValue(chat_id, NewValue):
    es = WhosSeenImageUrls.get_or_insert(NewValue)
    es.whoseSeenImage = str(chat_id)
    es.put()


def addPreviouslySeenImagesValue(chat_id, NewValue):
    es = WhosSeenImageUrls.get_or_insert(NewValue)
    if es.whoseSeenImage == '':
        es.whoseSeenImage = str(chat_id)
    else:
        es.whoseSeenImage += ',' + str(chat_id)
    es.put()


def getWhoseSeenImagesValue(image_link):
    es = WhosSeenImageUrls.get_or_insert(image_link)
    if es:
        return es.whoseSeenImage.encode('utf-8')
    return ''


def wasPreviouslySeenImage(chat_id, image_link):
    allWhoveSeenImage = getWhoseSeenImagesValue(image_link)
    if ',' + str(chat_id) + ',' in allWhoveSeenImage or \\
            allWhoveSeenImage.startswith(str(chat_id) + ',') or \\
            allWhoveSeenImage.endswith(',' + str(chat_id)) or \\
                    allWhoveSeenImage == str(chat_id):
        return True
    return False


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    print message
    requestText = str(message).replace(bot.name, "").strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_IMAGE_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': 'image',
            'safe': 'off',
            'q': requestText,
            'start': 1}
    Send_Images(bot, chat_id, user, requestText, args, keyConfig, totalResults)


def Google_Custom_Search(args):
    googurl = 'https://www.googleapis.com/customsearch/v1'
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.loads(urlfetch.fetch(realUrl).content)
    total_results = 0
    results_this_page = 0
    if 'searchInformation' in data and 'totalResults' in data['searchInformation']:
        total_results = data['searchInformation']['totalResults']
    if 'queries' in data and 'request' in data['queries'] and len(data['queries']['request']) > 0 and 'count' in \\
            data['queries']['request'][0]:
        results_this_page = data['queries']['request'][0]['count']
    return data, total_results, results_this_page

def is_valid_image(imagelink):
    return imagelink != '' and \\
           not imagelink.startswith('x-raw-image:///') and \\
           ImageIsSmallEnough(imagelink)


def ImageIsSmallEnough(imagelink):
    global image_file, fd
    try:
        fd = urllib.urlopen(imagelink)
        image_file = io.BytesIO(fd.read())
    except IOError:
        return False
    else:
        return int(sys.getsizeof(image_file)) < 10000000
    finally:
        try:
            if image_file:
                image_file.close()
            if fd:
                fd.close()
        except UnboundLocalError:
            print("image_file or fd local not defined")
        except NameError:
            print("image_file or fd global not defined")

def Image_Tags(imagelink, keyConfig):
    tags = ''
    strPayload = str({
        "requests":
            [
                {
                    "features":
                        [
                            {
                                "type": "WEB_DETECTION"
                            },
                            {
                                "type": "SAFE_SEARCH_DETECTION"
                            }
                        ],
                    "image":
                        {
                            "source":
                                {
                                    "imageUri": str(imagelink)
                                }
                        }
                }
            ]
    })
    try:
        raw_data = urlfetch.fetch(
            url='https://vision.googleapis.com/v1/images:annotate?key=' + keyConfig.get('Google', 'GCSE_APP_ID'),
            payload=strPayload,
            method='POST',
            headers={'Content-type': 'application/json'})
    except:
        return ''
    visionData = json.loads(raw_data.content)
    if 'error' not in visionData:
        if 'error' not in visionData['responses'][0]:
            webDetection = visionData['responses'][0]['webDetection']
            strAdult = visionData['responses'][0]['safeSearchAnnotation']['adult']
            if strAdult == 'POSSIBLE' or \\
                strAdult == 'LIKELY' or \\
                strAdult == 'VERY_LIKELY':
                tags += strAdult.replace('VERY_LIKELY', '').lower() + ' obscene adult content, '
            else:
                strViolence = visionData['responses'][0]['safeSearchAnnotation']['violence']
                if strViolence == 'POSSIBLE' or \\
                    strViolence == 'LIKELY' or \\
                    strViolence == 'VERY_LIKELY':
                    tags += strViolence.replace('VERY_LIKELY', '').lower() + ' offensive violence, '
                else:
                    strMedical = visionData['responses'][0]['safeSearchAnnotation']['medical']
                    if strMedical == 'POSSIBLE' or \\
                        strMedical == 'LIKELY' or \\
                        strMedical == 'VERY_LIKELY':
                        tags += strMedical.replace('VERY_LIKELY', '').lower() + ' shocking medical content, '
                    else:
                        strSpoof = visionData['responses'][0]['safeSearchAnnotation']['spoof']
                        if strSpoof == 'POSSIBLE' or \\
                            strSpoof == 'LIKELY' or \\
                            strSpoof == 'VERY_LIKELY':
                            strengthOfTag = strSpoof.replace('VERY_LIKELY', '').lower()
                            tags += 'a' + (' ' + strengthOfTag if strengthOfTag != '' else '') + ' meme, '
            if ('webEntities' in webDetection):
                for entity in webDetection['webEntities']:
                    if 'description' in entity:
                        tags += entity['description'].encode('utf-8') + ', '
        else:
            if visionData['responses'][0]['error']['message'][:10] == 'Image size' and visionData['responses'][0]['error']['message'][19:] == 'exceeding allowed max (4.00M).':
                tags += 'doesn\\'t look like anything to me, image is too large ' + visionData['responses'][0]['error']['message'][11:18]
            else:
                print(visionData['responses'][0]['error']['message'])
    else:
        print(visionData['error']['message'])
    if tags != '' and not tags.startswith('doesn\\'t look like anything to me'):
        tags = 'looks like: ' + tags
    return tags.rstrip(', ')

def Send_Images(bot, chat_id, user, requestText, args, keyConfig, total_number_to_send=1):
    data, total_results, results_this_page = Google_Custom_Search(args)
    if 'items' in data and total_results > 0:
        total_offset, total_results, total_sent = search_results_walker(args, bot, chat_id, data, total_number_to_send,
                                                                        user + ', ' + requestText, results_this_page,
                                                                        total_results, keyConfig)
        if int(total_sent) < int(total_number_to_send):
            if int(total_number_to_send) > 1:
                bot.sendMessage(chat_id=chat_id, text='I\\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\\'m afraid I can\\'t find any more images for ' +
                                                      string.capwords(requestText.encode('utf-8') + '.' +
                                                                      ' I could only find ' + str(
                                                          total_sent) + ' out of ' + str(total_number_to_send)))
            else:
                bot.sendMessage(chat_id=chat_id, text='I\\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\\'m afraid I can\\'t find any images for ' +
                                                      string.capwords(requestText.encode('utf-8')))
        else:
            return True
    else:
        if 'error' in data:
            bot.sendMessage(chat_id=chat_id, text='I\\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  data['error']['message'])
        else:
            bot.sendMessage(chat_id=chat_id, text='I\\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\\'m afraid I can\\'t find any images for ' +
                                                  string.capwords(requestText.encode('utf-8')))

def search_results_walker(args, bot, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                          total_offset=0, total_sent=0):
    offset_this_page = 0
    while int(total_sent) < int(number) and int(offset_this_page) < int(results_this_page):
        imagelink = data['items'][offset_this_page]['link']
        offset_this_page += 1
        total_offset = int(total_offset) + 1
        if '?' in imagelink:
            imagelink = imagelink[:imagelink.index('?')]
        if not wasPreviouslySeenImage(chat_id, imagelink):
            addPreviouslySeenImagesValue(chat_id, imagelink)
            if is_valid_image(imagelink):
                if number == 1:
                    if retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, requestText +
                            (' ' + str(total_sent + 1) + ' of ' + str(number) if int(number) > 1 else '')):
                        total_sent += 1
                    send_url_and_tags(bot, chat_id, imagelink, keyConfig, requestText)
                else:
                    message = requestText + ': ' + \\
                              (str(total_sent + 1) + ' of ' + str(number) + '\\n' if int(number) > 1 else '') + imagelink
                    bot.sendMessage(chat_id, message)
                    total_sent += 1
    if int(total_sent) < int(number) and int(total_offset) < int(total_results):
        args['start'] = total_offset + 1
        data, total_results, results_this_page = Google_Custom_Search(args)
        return search_results_walker(args, bot, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                                     total_offset, total_sent)
    return total_offset, total_results, total_sent

def send_url_and_tags(bot, chat_id, imagelink, keyConfig, requestText):
    imagelink_str = str(imagelink)
    image_tags = Image_Tags(imagelink_str, keyConfig)
    bot.sendMessage(chat_id=chat_id, text=requestText +
                                          (' ' + image_tags if image_tags != '' else '') +
                                          '\\n' + imagelink_str,
                    disable_web_page_preview=True)"""

def retry_on_telegram_error_command_code():
    return """# coding=utf-8
import sys
import urllib2
from time import sleep
from google.appengine.api import urlfetch

import telegram


def IsTooLongForCaption(text):
    return len(text) > 200

def SendDocumentWithRetry(bot, chat_id, imagelink, requestText):
    encodedImageLink = imagelink.encode('utf-8')
    numberOfRetries = 5
    sendException = True
    while sendException and numberOfRetries > 0:
        try:
            if not IsTooLongForCaption(requestText):
                bot.sendDocument(chat_id=chat_id,
                                 document=encodedImageLink,
                                 filename=requestText.replace('.',''),
                                 caption=requestText)
            else:
                bot.sendDocument(chat_id=chat_id,
                                 document=encodedImageLink,
                                 filename=requestText.replace('.',''))
            sendException = False
        except telegram.error.BadRequest:
            break
        except urlfetch.DeadlineExceededError:
            break
        except urllib2.HTTPError:
            break
        except urllib2.URLError:
            break
        except:
            sendException = True
            numberOfRetries -= 1
            print(sys.exc_info()[0])
            sleep(10)
    DidSend = not sendException and numberOfRetries > 0
    if DidSend and IsTooLongForCaption(requestText):
        bot.sendMessage(chat_id=chat_id, text=requestText, disable_web_page_preview=True)
    return DidSend

def SendPhotoWithRetry(bot, chat_id, imagelink, requestText):
    encodedImageLink = imagelink.encode('utf-8')
    numberOfRetries = 5
    sendException = True
    while sendException and numberOfRetries > 0:
        try:
            if not IsTooLongForCaption(requestText):
                bot.sendPhoto(chat_id=chat_id,
                              photo=encodedImageLink,
                              caption=requestText)
            else:
                bot.sendPhoto(chat_id=chat_id,
                              photo=encodedImageLink)
            sendException = False
        except telegram.error.BadRequest:
            break
        except urlfetch.DeadlineExceededError:
            break
        except urllib2.HTTPError:
            break
        except urllib2.URLError:
            break
        except:
            sendException = True
            numberOfRetries -= 1
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            sleep(10)
    DidSend = not sendException and numberOfRetries > 0
    if DidSend and IsTooLongForCaption(requestText):
        bot.sendMessage(chat_id=chat_id, text=requestText, disable_web_page_preview=True)
    return DidSend"""

def getgif_command_code():
    return """# coding=utf-8
import string
from threading import Thread
import urllib
import io
import main

from google.appengine.ext import ndb

import sys
from PIL import Image

retry_on_telegram_error = main.load_code_as_module('retry_on_telegram_error')
get = main.load_code_as_module('get')

CommandName = 'getgif'

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).replace(bot.name, "").strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_GIF_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': "image",
            'safe': "off",
            'q': requestText,
            'fileType': 'gif',
            'start': 1}
    Send_Animated_Gifs(bot, chat_id, user, requestText, args, keyConfig, totalResults)


def is_valid_gif(imagelink):
    global gif, image_file, fd
    try:
        fd = urllib.urlopen(imagelink)
        image_file = io.BytesIO(fd.read())
        gif = Image.open(image_file)
    except:
        return False
    else:
        try:
            gif.seek(1)
        except EOFError:
            pass
        else:
            return int(sys.getsizeof(image_file)) < 10000000
    finally:
        try:
            if gif:
                gif.fp.close()
            if image_file:
                image_file.close()
            if fd:
                fd.close()
        except UnboundLocalError:
            print("gif, image_file or fd local not defined")
        except NameError:
            print("gif, image_file or fd global not defined")

def Send_Animated_Gifs(bot, chat_id, user, requestText, args, keyConfig, totalResults=1):
    data, total_results, results_this_page = get.Google_Custom_Search(args)
    if 'items' in data and int(total_results) > 0:
        total_sent = search_results_walker(args, bot, chat_id, data, totalResults, user + ', ' + requestText, results_this_page, total_results, keyConfig)
        if int(total_sent) < int(totalResults):
            if int(totalResults) > 1:
                bot.sendMessage(chat_id=chat_id, text='I\\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\\'m afraid I can\\'t find any more gifs for ' +
                                                      string.capwords(requestText.encode('utf-8')) + '.' +
                                                      ' I could only find ' + str(total_sent) + ' out of ' +
                                                      str(totalResults))
            else:
                bot.sendMessage(chat_id=chat_id, text='I\\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\\'m afraid I can\\'t find a gif for ' +
                                                      string.capwords(requestText.encode('utf-8')) +
                                                      '.'.encode('utf-8'))
        else:
            return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\\'m afraid I can\\'t find a gif for ' +
                                              string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8'))

def search_results_walker(args, bot, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                          total_sent=0, total_offset=0):
    offset_this_page = 0
    while int(total_sent) < int(number) and int(offset_this_page) < int(results_this_page):
        imagelink = data['items'][offset_this_page]['link']
        print 'got image link ' + imagelink
        offset_this_page += 1
        total_offset += 1
        if '?' in imagelink:
            imagelink = imagelink[:imagelink.index('?')]
        if not get.wasPreviouslySeenImage(chat_id, imagelink):
            get.addPreviouslySeenImagesValue(chat_id, imagelink)
            if is_valid_gif(imagelink):
                if number == 1:
                    if retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, requestText):
                        total_sent += 1
                    get.send_url_and_tags(bot, chat_id, imagelink, keyConfig, requestText)
                else:
                    message = requestText + ': ' + (str(total_sent + 1) + ' of ' + str(number) + '\\n' if int(number) > 1 else '') + imagelink
                    bot.sendMessage(chat_id, message)
                    total_sent += 1
    if int(total_sent) < int(number) and int(total_offset) < int(total_results):
        args['start'] = total_offset + 1
        data, total_results, results_this_page = get.Google_Custom_Search(args)
        return search_results_walker(args, bot, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                                     total_sent, total_offset)
    return int(total_sent)

"""

def github_webhook_payload():
    return "%7B%22zen%22%3A%22It%27s+not+fully+shipped+until+it%27s+fast.%22%2C%22hook_id%22%3A16912121%2C%22hook%22%3A%7B%22type%22%3A%22Repository%22%2C%22id%22%3A16912121%2C%22name%22%3A%22web%22%2C%22active%22%3Atrue%2C%22events%22%3A%5B%22push%22%5D%2C%22config%22%3A%7B%22content_type%22%3A%22form%22%2C%22insecure_ssl%22%3A%220%22%2C%22secret%22%3A%22%2A%2A%2A%2A%2A%2A%2A%2A%22%2C%22url%22%3A%22https%3A%2F%2Fhey-boet.com%2Fgithub_webhook%22%7D%2C%22updated_at%22%3A%222017-10-14T07%3A41%3A28Z%22%2C%22created_at%22%3A%222017-10-14T07%3A41%3A28Z%22%2C%22url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fhooks%2F16912121%22%2C%22test_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fhooks%2F16912121%2Ftest%22%2C%22ping_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fhooks%2F16912121%2Fpings%22%2C%22last_response%22%3A%7B%22code%22%3Anull%2C%22status%22%3A%22unused%22%2C%22message%22%3Anull%7D%7D%2C%22repository%22%3A%7B%22id%22%3A97470323%2C%22name%22%3A%22ImageBoet%22%2C%22full_name%22%3A%22SalamiArmy%2FImageBoet%22%2C%22owner%22%3A%7B%22login%22%3A%22SalamiArmy%22%2C%22id%22%3A8664897%2C%22avatar_url%22%3A%22https%3A%2F%2Favatars2.githubusercontent.com%2Fu%2F8664897%3Fv%3D4%22%2C%22gravatar_id%22%3A%22%22%2C%22url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%22%2C%22html_url%22%3A%22https%3A%2F%2Fgithub.com%2FSalamiArmy%22%2C%22followers_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Ffollowers%22%2C%22following_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Ffollowing%7B%2Fother_user%7D%22%2C%22gists_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Fgists%7B%2Fgist_id%7D%22%2C%22starred_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Fstarred%7B%2Fowner%7D%7B%2Frepo%7D%22%2C%22subscriptions_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Fsubscriptions%22%2C%22organizations_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Forgs%22%2C%22repos_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Frepos%22%2C%22events_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Fevents%7B%2Fprivacy%7D%22%2C%22received_events_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Freceived_events%22%2C%22type%22%3A%22User%22%2C%22site_admin%22%3Afalse%7D%2C%22private%22%3Afalse%2C%22html_url%22%3A%22https%3A%2F%2Fgithub.com%2FSalamiArmy%2FImageBoet%22%2C%22description%22%3A%22Stupid+Chat+Bot%22%2C%22fork%22%3Afalse%2C%22url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%22%2C%22forks_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fforks%22%2C%22keys_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fkeys%7B%2Fkey_id%7D%22%2C%22collaborators_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fcollaborators%7B%2Fcollaborator%7D%22%2C%22teams_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fteams%22%2C%22hooks_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fhooks%22%2C%22issue_events_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fissues%2Fevents%7B%2Fnumber%7D%22%2C%22events_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fevents%22%2C%22assignees_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fassignees%7B%2Fuser%7D%22%2C%22branches_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fbranches%7B%2Fbranch%7D%22%2C%22tags_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Ftags%22%2C%22blobs_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fgit%2Fblobs%7B%2Fsha%7D%22%2C%22git_tags_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fgit%2Ftags%7B%2Fsha%7D%22%2C%22git_refs_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fgit%2Frefs%7B%2Fsha%7D%22%2C%22trees_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fgit%2Ftrees%7B%2Fsha%7D%22%2C%22statuses_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fstatuses%2F%7Bsha%7D%22%2C%22languages_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Flanguages%22%2C%22stargazers_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fstargazers%22%2C%22contributors_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fcontributors%22%2C%22subscribers_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fsubscribers%22%2C%22subscription_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fsubscription%22%2C%22commits_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fcommits%7B%2Fsha%7D%22%2C%22git_commits_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fgit%2Fcommits%7B%2Fsha%7D%22%2C%22comments_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fcomments%7B%2Fnumber%7D%22%2C%22issue_comment_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fissues%2Fcomments%7B%2Fnumber%7D%22%2C%22contents_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fcontents%2F%7B%2Bpath%7D%22%2C%22compare_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fcompare%2F%7Bbase%7D...%7Bhead%7D%22%2C%22merges_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fmerges%22%2C%22archive_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2F%7Barchive_format%7D%7B%2Fref%7D%22%2C%22downloads_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fdownloads%22%2C%22issues_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fissues%7B%2Fnumber%7D%22%2C%22pulls_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fpulls%7B%2Fnumber%7D%22%2C%22milestones_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fmilestones%7B%2Fnumber%7D%22%2C%22notifications_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fnotifications%7B%3Fsince%2Call%2Cparticipating%7D%22%2C%22labels_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Flabels%7B%2Fname%7D%22%2C%22releases_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Freleases%7B%2Fid%7D%22%2C%22deployments_url%22%3A%22https%3A%2F%2Fapi.github.com%2Frepos%2FSalamiArmy%2FImageBoet%2Fdeployments%22%2C%22created_at%22%3A%222017-07-17T11%3A47%3A10Z%22%2C%22updated_at%22%3A%222017-07-17T12%3A23%3A58Z%22%2C%22pushed_at%22%3A%222017-10-11T08%3A11%3A35Z%22%2C%22git_url%22%3A%22git%3A%2F%2Fgithub.com%2FSalamiArmy%2FImageBoet.git%22%2C%22ssh_url%22%3A%22git%40github.com%3ASalamiArmy%2FImageBoet.git%22%2C%22clone_url%22%3A%22https%3A%2F%2Fgithub.com%2FSalamiArmy%2FImageBoet.git%22%2C%22svn_url%22%3A%22https%3A%2F%2Fgithub.com%2FSalamiArmy%2FImageBoet%22%2C%22homepage%22%3Anull%2C%22size%22%3A27%2C%22stargazers_count%22%3A0%2C%22watchers_count%22%3A0%2C%22language%22%3A%22Python%22%2C%22has_issues%22%3Atrue%2C%22has_projects%22%3Atrue%2C%22has_downloads%22%3Atrue%2C%22has_wiki%22%3Atrue%2C%22has_pages%22%3Afalse%2C%22forks_count%22%3A0%2C%22mirror_url%22%3Anull%2C%22open_issues_count%22%3A0%2C%22forks%22%3A0%2C%22open_issues%22%3A0%2C%22watchers%22%3A0%2C%22default_branch%22%3A%22master%22%7D%2C%22sender%22%3A%7B%22login%22%3A%22SalamiArmy%22%2C%22id%22%3A8664897%2C%22avatar_url%22%3A%22https%3A%2F%2Favatars2.githubusercontent.com%2Fu%2F8664897%3Fv%3D4%22%2C%22gravatar_id%22%3A%22%22%2C%22url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%22%2C%22html_url%22%3A%22https%3A%2F%2Fgithub.com%2FSalamiArmy%22%2C%22followers_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Ffollowers%22%2C%22following_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Ffollowing%7B%2Fother_user%7D%22%2C%22gists_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Fgists%7B%2Fgist_id%7D%22%2C%22starred_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Fstarred%7B%2Fowner%7D%7B%2Frepo%7D%22%2C%22subscriptions_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Fsubscriptions%22%2C%22organizations_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Forgs%22%2C%22repos_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Frepos%22%2C%22events_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Fevents%7B%2Fprivacy%7D%22%2C%22received_events_url%22%3A%22https%3A%2F%2Fapi.github.com%2Fusers%2FSalamiArmy%2Freceived_events%22%2C%22type%22%3A%22User%22%2C%22site_admin%22%3Afalse%7D%7D"

def get_launch_code():
    return """
# coding=utf-8
import datetime
import json
import urllib2

import telegram

from dateutil import tz


def run(bot, chat_id, user, keyConfig, message='', totalResults=1):
    formattedLaunchInfo = ''
    formattedLaunchInfo, has_results = get_launch_data(formattedLaunchInfo, keyConfig)
    if has_results:
        bot.sendMessage(chat_id=chat_id, text=formattedLaunchInfo,
                        parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\\'m sorry ' + (user if not user == '' else 'Dave') + \\
                                              ', I\\'m afraid I can\\'t find any upcoming rocket launches.')


def get_launch_data(formattedLaunchInfo, keyConfig):
    rocketUrl = 'https://launchlibrary.net/1.2.1/launch/next/5'
    rocketUrlRequest = urllib2.Request(rocketUrl, headers={'User-Agent': "Magic Browser"})
    rocketData = json.load(urllib2.urlopen(rocketUrlRequest))
    has_results = 'launches' in rocketData
    if has_results:
        blast = rocketData['launches']
        formattedLaunchInfo = formatted_launch_message(blast, keyConfig)
    return formattedLaunchInfo, has_results


def formatted_launch_message(blast, keyConfig):
    b1 = blast[0]
    b2 = blast[1]
    b3 = blast[2]
    b4 = blast[3]
    b5 = blast[4]
    utc_zone = tz.tzutc()
    timezone_string = keyConfig.get('BotAdministration', 'Timezone')
    local_zone = tz.tzoffset('Offset TZ from server to local',
                             int(timezone_string) * 60 * 60)
    blast1UtcTime = datetime.datetime.strptime(b1['net'], '%B %d, %Y %H:%M:%S %Z')
    if blast1UtcTime.hour >= '22' or blast1UtcTime.hour == 0:
        blast1UtcTime = blast1UtcTime + datetime.timedelta(days=1)
    blast1UtcTime = blast1UtcTime.replace(tzinfo=utc_zone)
    blast1LocalString = str(blast1UtcTime.astimezone(local_zone))
    blast1LocalTime = datetime.datetime.strptime(blast1LocalString, '%Y-%m-%d %H:%M:%S' + timezone_string + ':00')
    blast2UtcTime = datetime.datetime.strptime(b2['net'], '%B %d, %Y %H:%M:%S %Z')
    if blast2UtcTime.hour >= '22' or blast2UtcTime.hour == 0:
        blast2UtcTime = blast2UtcTime + datetime.timedelta(days=1)
    blast2UtcTime = blast2UtcTime.replace(tzinfo=utc_zone)
    blast2LocalString = str(blast2UtcTime.astimezone(local_zone))
    blast2LocalTime = datetime.datetime.strptime(blast2LocalString, '%Y-%m-%d %H:%M:%S' + timezone_string + ':00')
    blast3UtcTime = datetime.datetime.strptime(b3['net'], '%B %d, %Y %H:%M:%S %Z')
    if blast3UtcTime.hour >= '22' or blast3UtcTime.hour == 0:
        blast3UtcTime = blast3UtcTime + datetime.timedelta(days=1)
    blast3UtcTime = blast3UtcTime.replace(tzinfo=utc_zone)
    blast3LocalString = str(blast3UtcTime.astimezone(local_zone))
    blast3LocalTime = datetime.datetime.strptime(blast3LocalString, '%Y-%m-%d %H:%M:%S' + timezone_string + ':00')
    blast4UtcTime = datetime.datetime.strptime(b4['net'], '%B %d, %Y %H:%M:%S %Z')
    if blast4UtcTime.hour >= '22' or blast4UtcTime.hour == 0:
        blast4UtcTime = blast4UtcTime + datetime.timedelta(days=1)
    blast4UtcTime = blast4UtcTime.replace(tzinfo=utc_zone)
    blast4LocalString = str(blast4UtcTime.astimezone(local_zone))
    blast4LocalTime = datetime.datetime.strptime(blast4LocalString, '%Y-%m-%d %H:%M:%S' + timezone_string + ':00')
    blast5UtcTime = datetime.datetime.strptime(b5['net'], '%B %d, %Y %H:%M:%S %Z')
    if blast5UtcTime.hour >= '22' or blast5UtcTime.hour == 0:
        blast5UtcTime = blast5UtcTime + datetime.timedelta(days=1)
    blast5UtcTime = blast5UtcTime.replace(tzinfo=utc_zone)
    blast5LocalString = str(blast5UtcTime.astimezone(local_zone))
    blast5LocalTime = datetime.datetime.strptime(blast5LocalString, '%Y-%m-%d %H:%M:%S' + timezone_string + ':00')
    formattedLaunchInfo = 'Upcoming Rocket Launches: (all times UTC' + timezone_string + ')\\n\\n' + \\
                          str(blast1LocalTime) + '\\n*' + b1['name'] + \\
                          '*\\nLaunching from ' + ('[' if b1['location']['pads'][0]['mapURL'] != '' and b1['location']['pads'][0]['mapURL'] != None else '') + \\
                          b1['location']['pads'][0]['name'] + \\
                          ('](' + b1['location']['pads'][0]['mapURL'] + ')' if b1['location']['pads'][0][
                                                                                   'mapURL'] != '' and b1['location']['pads'][0]['mapURL'] != None else '') + \\
                          ('\\nWatch live at ' + b1['vidURL'] if 'vidURL' in b1 and b1['vidURL'] != '' and b1['vidURL'] != None else '') + \\
                          '\\n\\n' + str(blast2LocalTime) + '\\n*' + b2['name'] + \\
                          '*\\nLaunching from ' + ('[' if b2['location']['pads'][0]['mapURL'] != '' and b2['location']['pads'][0]['mapURL'] != None else '') + \\
                          b2['location']['pads'][0]['name'] + \\
                          ('](' + b2['location']['pads'][0]['mapURL'] + ')' if b2['location']['pads'][0][
                                                                                   'mapURL'] != '' and b2['location']['pads'][0]['mapURL'] != None else '') + \\
                          ('\\nWatch live at ' + b2['vidURL'] if 'vidURL' in b2 and b2['vidURL'] != '' and b2['vidURL'] != None else '') + \\
                          '\\n\\n' + str(blast3LocalTime) + '\\n*' + b3['name'] + \\
                          '*\\nLaunching from ' + ('[' if b3['location']['pads'][0]['mapURL'] != '' and b3['location']['pads'][0]['mapURL'] != None else '') + \\
                          b3['location']['pads'][0]['name'] + \\
                          ('](' + b3['location']['pads'][0]['mapURL'] + ')' if b3['location']['pads'][0][
                                                                                   'mapURL'] != '' and b3['location']['pads'][0]['mapURL'] != None else '') + \\
                          ('\\nWatch live at ' + b3['vidURL'] if 'vidURL' in b3 and b3['vidURL'] != '' and b3['vidURL'] != None else '') + \\
                          '\\n\\n' + str(blast4LocalTime) + '\\n*' + b4['name'] + \\
                          '*\\nLaunching from ' + ('[' if b4['location']['pads'][0]['mapURL'] != '' and b4['location']['pads'][0]['mapURL'] != None else '') + \\
                          b4['location']['pads'][0]['name'] + \\
                          ('](' + b4['location']['pads'][0]['mapURL'] + ')' if b4['location']['pads'][0][
                                                                                   'mapURL'] != '' and b4['location']['pads'][0]['mapURL'] != None else '') + \\
                          ('\\nWatch live at ' + b4['vidURL'] if 'vidURL' in b4 and b4['vidURL'] != '' and b4['vidURL'] != None else '') + \\
                          '\\n\\n' + str(blast5LocalTime) + '\\n*' + b5['name'] + \\
                          '*\\nLaunching from ' + ('[' if b5['location']['pads'][0]['mapURL'] != '' and b5['location']['pads'][0]['mapURL'] != None else '') + \\
                          b5['location']['pads'][0]['name'] + \\
                          ('](' + b5['location']['pads'][0]['mapURL'] + ')' if b5['location']['pads'][0][
                                                                                   'mapURL'] != '' and b5['location']['pads'][0]['mapURL'] != None else '') + \\
                          ('\\nWatch live at ' + b5['vidURL'] if 'vidURL' in b5 and b5['vidURL'] != '' and b5['vidURL'] != None else '')
    return formattedLaunchInfo
    """

def get_wiki_code():
    return """# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).strip()

    wikiUrl = \\
        'https://simple.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&search='
    realUrl = wikiUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    total_sent = 0
    result = ''
    while len(data) > 2 and int(total_sent) < len(data[2]) and int(total_sent) < int(totalResults):
        result += ('\\n' if result != '' else '') + (user + ': ' if not user == '' else '') + \\
                  data[2][total_sent] + '\\nLink: ' + data[3][total_sent]
        total_sent += 1
    if result == '':
        wikiUrl = \\
            'https://en.wikipedia.org/w/api.php?action=opensearch&namespace=0&format=json&search='
        realUrl = wikiUrl + requestText.encode('utf-8')
        data = json.load(urllib.urlopen(realUrl))
        while len(data) > 2 and int(total_sent) < len(data[2]) and int(total_sent) < int(totalResults):
            result += ('\\n' if result != '' else '') + (user + ': ' if not user == '' else '') + \\
                      data[2][total_sent] + '\\nLink: ' + data[3][total_sent]
            total_sent += 1
        if result == '':
            return 'I\\'m sorry ' + (user if not user == '' else 'Dave') +\\
                   ', I\\'m afraid I can\\'t find any wiki articles for ' +\\
                   requestText.encode('utf-8') + '.'
        return result
    bot.sendMessage(chat_id=chat_id, text=result)
"""