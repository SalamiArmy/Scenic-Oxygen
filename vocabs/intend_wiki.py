from adapt.intent import IntentBuilder

def generate_vocab(engine):
    engine.register_regex_entity("what is (?P<WhatIs>.*)")

    return IntentBuilder("ImageIntent").require('WhatIs')
