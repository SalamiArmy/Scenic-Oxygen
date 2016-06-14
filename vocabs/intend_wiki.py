from adapt.intent import IntentBuilder


def generate_vocab(engine):
    engine.register_regex_entity("(what|who) is (?P<WhatWhoIs>.*)")

    wiki_keywords = [
        "know",
        "understand",
        "think",
        "comprehend",
        "knowledge"
    ]

    for wt in wiki_keywords:
        engine.register_entity(wt, "WikiKeywords")

    return IntentBuilder("ImageIntent")\
        .require('WhatWhoIs')\
        .optionally('WikiKeywords')\
        .build()
