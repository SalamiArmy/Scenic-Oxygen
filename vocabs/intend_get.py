from adapt.intent import IntentBuilder


def generate_vocab(engine):
    engine.register_regex_entity("(of|show) (?P<OfImage>.*)")
    engine.register_regex_entity("(show me|show us|show all of us|show us all) (?P<ShowMeImage>.*)")

    image_verbs = [
        "picture",
        "image",
        "see",
        "show"
    ]

    for mv in image_verbs:
        engine.register_entity(mv, "ImageVerb")

    image_keywords = [
        "pictures",
        "images",
        "look",
        "visage",
        "gaze"
    ]

    for mk in image_keywords:
        engine.register_entity(mk, "ImageKeyword")

    return IntentBuilder("ImageIntent") \
        .require("ImageVerb") \
        .optionally("ImageKeyword") \
        .optionally("OfImage") \
        .optionally("ShowMeImage") \
        .build()
