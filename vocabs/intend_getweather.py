from adapt.intent import IntentBuilder

def generate_vocab(engine):
    # create and register weather vocabulary
    weather_keyword = [
        "weather"
    ]

    for wk in weather_keyword:
        engine.register_entity(wk, "WeatherKeyword")

    weather_types = [
        "snow",
        "rain",
        "wind",
        "sleet",
        "sun"
    ]

    for wt in weather_types:
        engine.register_entity(wt, "WeatherType")

    # create regex to parse out locations
    engine.register_regex_entity("in (?P<Location>.*)")

    # structure intent
    return IntentBuilder("WeatherIntent")\
        .require("WeatherKeyword")\
        .optionally("WeatherType")\
        .require("Location")\
        .build()