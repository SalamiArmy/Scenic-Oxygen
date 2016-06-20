from adapt.intent import IntentBuilder
import commands.wiki as wiki
import commands.getanswer as getanswer
import commands.define as define
import commands.urban as urban


def generate_vocab(engine):
    engine.register_regex_entity('(is|do|was|can|much|many|does|will|far|near|close) (?P<WhoWhatHow>.*)')

    question_keywords = [
        'who',
        'what',
        'how',
        'why',
        'when'
    ]

    for wt in question_keywords:
        engine.register_entity(wt, 'QuestionKeywords')

    info_keywords = [
        'know',
        'understand',
        'think',
        'comprehend',
        'knowledge',
        'ask',
        'question',
        'theory',
        'theoretically'
    ]

    for wt in info_keywords:
        engine.register_entity(wt, 'InfoKeywords')

    return IntentBuilder('InfoIntent')\
        .require('QuestionKeywords')\
        .optionally('WhoWhatHow')\
        .optionally('InfoKeywords')\
        .build()

def run_command_hierarchy(bot, keyConfig, chat_id, fr_username, requestText, WhoWhatHow, confidence_percent):

    if getanswer.run(bot, keyConfig, chat_id, fr_username, requestText, confidence_percent):
        return True

    if WhoWhatHow != '':
        if wiki.run(bot, keyConfig, chat_id, fr_username, WhoWhatHow, confidence_percent):
            return True

        if define.run(bot, keyConfig, chat_id, fr_username, WhoWhatHow, confidence_percent):
            return True

        if urban.run(bot, keyConfig, chat_id, fr_username, WhoWhatHow, confidence_percent):
            return True

    found_info = False
    text_split = requestText.split()

    for word in text_split:
        if len(word) > 4:
            found_info = wiki.run(bot, keyConfig, chat_id, fr_username, word, confidence_percent)
        if found_info:
            return True

    for word_pair in [text_split[i]+' '+text_split[i+1] for i in range(len(text_split)-1)]:
        if len(word) > 4:
            found_info = wiki.run(bot, keyConfig, chat_id, fr_username, word_pair, confidence_percent)
        if found_info:
            return True

    for word in text_split:
        if len(word) > 4:
            found_info = define.run(bot, keyConfig, chat_id, fr_username, word, confidence_percent)
        if found_info:
            return True

    for word in text_split:
        if len(word) > 4:
            found_info = urban.run(bot, keyConfig, chat_id, fr_username, word, confidence_percent)
        if found_info:
            return True

    for word_pair in [text_split[i]+' '+text_split[i+1] for i in range(len(text_split)-1)]:
        if len(word) > 4:
            found_info = urban.run(bot, keyConfig, chat_id, fr_username, word_pair, confidence_percent)
        if found_info:
            return True

    print('Get info ' + str(confidence_percent) +
          '% intention with request text ' + requestText +
          ' could not be satisfied.')
