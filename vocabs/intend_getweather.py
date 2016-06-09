import vocabs

__author__ = 'seanfitz'
"""
A sample intent that uses a fixed vocabulary to extract entities for an intent

try with the following:
PYTHONPATH=. python examples/single_intent_parser.py "what's the weather like in tokyo"
"""
import json
import sys
from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine

weather_keyword = [
    "weather"
]

for wk in weather_keyword:
    vocabs.engine.register_entity(wk, "WeatherKeyword")

weather_types = [
    "snow",
    "rain",
    "wind",
    "sleet",
    "sun"
]

for wt in weather_types:
    vocabs.engine.register_entity(wt, "WeatherType")

locations = [
    "Seattle",
    "San Francisco",
    "Tokyo"
]

for loc in locations:
    vocabs.engine.register_entity(loc, "Location")

weather_intent = IntentBuilder("WeatherIntent")\
    .require("WeatherKeyword")\
    .optionally("WeatherType")\
    .require("Location")\
    .build()

if __name__ == "__main__":
    for intent in vocabs.engine.determine_intent(' '.join(sys.argv[1:])):
        if intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))