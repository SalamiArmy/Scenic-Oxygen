from adapt.intent import IntentBuilder

def generate_vocab(engine):
    # create regex to parse out sounds
    engine.register_regex_entity("to (?P<Sound>.*)")

    music_verbs = [
        "listen",
        "hear",
        "play"
    ]

    for mv in music_verbs:
        engine.register_entity(mv, "MusicVerb")

    music_keywords = [
        "songs",
        "music"
    ]

    for mk in music_keywords:
        engine.register_entity(mk, "MusicKeyword")

    return IntentBuilder("MusicIntent")\
        .require("MusicVerb")\
        .optionally("MusicKeyword")\
        .optionally("Sound")\
        .build()
