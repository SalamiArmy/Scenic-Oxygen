from adapt.intent import IntentBuilder


def generate_vocab(engine):
    weather_keyword = [
        "how",
        "why",
        "when"
    ]

    for wk in weather_keyword:
        engine.register_entity(wk, "QuestionKeyword")

    return IntentBuilder("AnswerIntent").require('QuestionKeyword').build()
