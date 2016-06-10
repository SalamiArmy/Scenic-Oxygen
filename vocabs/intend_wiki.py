from adapt.intent import IntentBuilder


def generate_vocab(engine):
    engine.register_regex_entity("(what is (?P<WhatWhoIs>.*))|(who is (?P<WhatWhoIs>.*))")

    return IntentBuilder("ImageIntent").require('WhatWhoIs').build()
