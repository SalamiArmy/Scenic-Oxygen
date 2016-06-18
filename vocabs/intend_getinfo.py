from adapt.intent import IntentBuilder
import commands.wiki as wiki
import commands.getanswer as getanswer
import commands.define as define
import commands.urban as urban


def generate_vocab(engine):
    engine.register_regex_entity('(who|what|how|why|when) (is|was|much|many|does|will) (?P<WhoWhatHow>.*)')

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

    return IntentBuilder("ImageIntent")\
        .require('WhoWhatHow')\
        .optionally('InfoKeywords')\
        .build()

def run_command_hierarchy(bot, keyConfig, chat_id, fr_username, requestText, confidence_percent):
    if getanswer.run(bot, keyConfig, chat_id, fr_username, requestText, confidence_percent):
        return True

    if wiki.run(bot, keyConfig, chat_id, fr_username, requestText, confidence_percent):
        return True

    canDefine = False
    for word in requestText.split(' '):
        if len(word) > 3:
            canDefine = define.run(bot, keyConfig, chat_id, fr_username, word, confidence_percent)
        if canDefine:
            return True

    for word in requestText.split(' '):
        if len(word) > 3:
            canDefine = urban.run(bot, keyConfig, chat_id, fr_username, word, confidence_percent)
        if canDefine:
            return True

    print('Get info ' + str(confidence_percent) +
          '% intention with request text ' + requestText +
          ' could not be satisfied.')
