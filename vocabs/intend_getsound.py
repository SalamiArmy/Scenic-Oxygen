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

artists = [
    "third eye blind",
    "the who",
    "the clash",
    "john mayer",
    "kings of leon",
    "adelle"
]

for a in artists:
    vocabs.engine.register_entity(a, "Artist")

music_verbs = [
    "listen",
    "hear",
    "play"
]

for mv in music_verbs:
    vocabs.engine.register_entity(mv, "MusicVerb")

music_keywords = [
    "songs",
    "music"
]

for mk in music_keywords:
    vocabs.engine.register_entity(mk, "MusicKeyword")

music_intent = IntentBuilder("MusicIntent")\
    .require("MusicVerb")\
    .optionally("MusicKeyword")\
    .optionally("Artist")\
    .build()

if __name__ == "__main__":
    for intent in vocabs.engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))