# coding=utf-8

def get_command_code():
    return """# coding=utf-8
import hashlib
import sys

import logging

reload(sys)
sys.setdefaultencoding('utf8')
import json
import string
import urllib

import io

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import main
retry_on_telegram_error = main.get_platform_command_code('telegram', 'retry_on_telegram_error')
telegram_get = main.get_platform_command_code('telegram', 'get')

CommandName = 'get'

class SeenImageUrls(ndb.Model):
    # key name: ImageUrl
    seenImage = ndb.BooleanProperty(indexed=False, default=False)

class SeenHashDigests(ndb.Model):
    # key name: ImageHash
    seenHash = ndb.BooleanProperty(indexed=False, default=False)

# ================================

def addPreviouslySeenImagesValue(image_url):
    es = SeenImageUrls.get_or_insert(image_url)
    es.seenImage = True
    es.put()

def addPreviouslySeenHashDigest(image_hash):
    es = SeenHashDigests.get_or_insert(image_hash)
    es.seenHash = True
    es.put()

def getSeenImagesValue(image_link):
    es = SeenImageUrls.get_or_insert(image_link)
    return es.seenImage

def getSeenHashDigest(image_hash):
    es = SeenHashDigests.get_or_insert(image_hash)
    return es.seenHash


def wasPreviouslySeenImage(image_link):
    seenImage = getSeenImagesValue(image_link)
    if seenImage:
        return True
    addPreviouslySeenImagesValue(image_link)
    return False

def wasPreviouslySeenHash(image_hash):
    allWhoveSeenHash = getSeenHashDigest(image_hash)
    if allWhoveSeenHash:
        return True
    addPreviouslySeenHashDigest(image_hash)
    return False


def run(keyConfig, message, totalResults=1):
    args = {'cx': keyConfig.get('Google', 'GCSE_IMAGE_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': 'image',
            'safe': 'off',
            'q': message,
            'start': 1}
    return Send_Images(message, args, keyConfig, totalResults)


def Google_Custom_Search(args):
    googurl = 'https://www.googleapis.com/customsearch/v1'
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.loads(urlfetch.fetch(realUrl).content)
    total_results = 0
    results_this_page = 0
    if 'searchInformation' in data and 'totalResults' in data['searchInformation']:
        total_results = data['searchInformation']['totalResults']
    if 'queries' in data and 'request' in data['queries'] and len(data['queries']['request']) > 0 and 'count' in \
            data['queries']['request'][0]:
        results_this_page = data['queries']['request'][0]['count']
    return data, total_results, results_this_page

def is_valid_image(image_url):
    if image_url != '' and \
            not image_url.startswith('x-raw-image:///') and \
            not wasPreviouslySeenImage(image_url):
        return IsValidImageFile(image_url)
    return False

def ImageHasUniqueHashDigest(image_as_string):
    image_as_hash = hashlib.md5(image_as_string)
    image_hash_digest = image_as_hash.hexdigest()
    logging.info('hashed image as ' + image_hash_digest)
    hashed_before = wasPreviouslySeenHash(image_hash_digest)
    if hashed_before:
        logging.info('Hash collision!')
    return not hashed_before

def IsValidImageFile(image_url):
    global image_file, fd
    try:
        fd = urllib.urlopen(image_url)
        image_file = io.BytesIO(fd.read())
    except IOError:
        return False
    else:
        return telegram_get.ImageIsSmallEnough(image_file) and ImageHasUniqueHashDigest(image_file.getvalue())
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


def Send_Images(requestText, args, keyConfig, total_number_to_send=1):
    data, total_results, results_this_page = Google_Custom_Search(args)
    if 'items' in data and total_results > 0:
        total_offset, total_results, total_sent = search_results_walker(args, data, total_number_to_send, requestText, results_this_page,
                                                                        total_results, keyConfig)
        if len(total_sent) < int(total_number_to_send):
            if int(total_number_to_send) > 1:
                total_sent.append('I\'m sorry Dave, I\'m afraid I can\'t find any more images for ' + \
                                                      requestText + '. I could only find ' + str(
                                                          len(total_sent)) + ' out of ' + str(total_number_to_send))
            else:
                total_sent.append('I\'m sorry Dave, I\'m afraid I can\'t find any images for ' + requestText)
        return total_sent
    else:
        if 'error' in data:
            errorMsg = 'I\'m sorry Dave' + data['error']['message']
            return [errorMsg]
        else:
            errorMsg = 'I\'m sorry Dave, I\'m afraid I can\'t find any images for ' + requestText
            return [errorMsg]

def search_results_walker(args, data, number, requestText, results_this_page, total_results, keyConfig,
                          total_offset=0, total_sent=[]):
    offset_this_page = 0
    while len(total_sent) < int(number) and int(offset_this_page) < int(results_this_page):
        imagelink = str(data['items'][offset_this_page]['link'])
        offset_this_page += 1
        total_offset = int(total_offset) + 1
        if '?' in imagelink:
            imagelink = imagelink[:imagelink.index('?')]
        if is_valid_image(imagelink):
            if number == 1:
                total_sent.append(get_url_and_tags(imagelink, keyConfig, requestText))
            else:
                total_sent.append(requestText + ': ' +
                          (str(len(total_sent) + 1) + ' of ' +
                           str(number) + '\n' if int(number) > 1 else '') + imagelink)
    if len(total_sent) < int(number) and int(total_offset) < int(total_results):
        args['start'] = total_offset + 1
        data, total_results, results_this_page = Google_Custom_Search(args)
        return search_results_walker(args, data, number, requestText, results_this_page, total_results, keyConfig,
                                     total_offset, total_sent)
    return total_offset, total_results, total_sent

def get_url_and_tags( imagelink, keyConfig, requestText):
    imagelink_str = str(imagelink)
    image_tags = telegram_get.Image_Tags(imagelink_str, keyConfig)
    return requestText + (' ' + image_tags if image_tags != '' else '') + '\n' + imagelink_str
"""

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
import urllib
import io
import main

import sys
from PIL import Image

CommandName = 'getgif'

retry_on_telegram_error = main.get_platform_command_code('telegram', 'retry_on_telegram_error')
get = main.get_platform_command_code('telegram', 'get')

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).replace(bot.name, "").strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_GIF_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': 'image',
            'safe': "off",
            'q': requestText,
            'fileType': 'gif',
            'start': 1}
    return Send_Animated_Gifs(bot, chat_id, user, requestText, args, keyConfig, totalResults)


def is_valid_gif(imagelink, chat_id):
    if not get.wasPreviouslySeenImage(imagelink, chat_id):
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
                return int(sys.getsizeof(image_file)) < 10000000 and \
                       get.ImageHasUniqueHashDigest(image_file.getvalue(), chat_id)
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
        if len(total_sent) < int(totalResults):
            if int(totalResults) > 1:
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t find any more gifs for ' +
                                                      string.capwords(requestText.encode('utf-8')) + '.' +
                                                      ' I could only find ' + str(len(total_sent)) + ' out of ' +
                                                      str(totalResults))
            else:
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t find a gif for ' +
                                                      string.capwords(requestText.encode('utf-8')) +
                                                      '.'.encode('utf-8'))
        return total_sent
    else:
        errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                   ', I\'m afraid I can\'t find a gif for ' + \
                   string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8')
        bot.sendMessage(chat_id=chat_id, text=errorMsg)
        return [errorMsg]

def search_results_walker(args, bot, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                          total_sent=[], total_offset=0):
    offset_this_page = 0
    while len(total_sent) < int(number) and int(offset_this_page) < int(results_this_page):
        imagelink = data['items'][offset_this_page]['link']
        print 'got image link ' + imagelink
        offset_this_page += 1
        total_offset += 1
        if '?' in imagelink:
            imagelink = imagelink[:imagelink.index('?')]
        if is_valid_gif(imagelink, chat_id):
            if number == 1:
                if retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, requestText):
                    total_sent.append(imagelink)
                    get.send_url_and_tags(bot, chat_id, imagelink, keyConfig, requestText)
            else:
                message = requestText + ': ' + (str(len(total_sent) + 1) + ' of ' + str(number) + '\n' if int(number) > 1 else '') + imagelink
                bot.sendMessage(chat_id, message)
                total_sent.append(imagelink)
    if len(total_sent) < int(number) and int(total_offset) < int(total_results):
        args['start'] = total_offset + 1
        data, total_results, results_this_page = get.Google_Custom_Search(args)
        return search_results_walker(args, bot, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                                     total_sent, total_offset)
    return total_sent

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