import vocabs

__author__ = 'seanfitz'
"""
A sample intent that uses a fixed vocabulary to extract entities for an intent

try with the following:
PYTHONPATH=. python examples/single_intent_parser.py "play some music by the clash"
"""
import json
import sys
from adapt.intent import IntentBuilder

engine = vocabs.engine

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

music_intent = IntentBuilder("MusicIntent")\
    .require("MusicVerb")\
    .optionally("MusicKeyword")\
    .optionally("Sound")\
    .build()

if __name__ == "__main__":
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))