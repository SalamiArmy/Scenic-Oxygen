import vocabs

__author__ = 'salamiarmy'
"""
A sample intent that uses a regular expression entity to
extract location from a query
try with the following:
PYTHONPATH=. python examples/intend_get.py "i want to gaze upon the visage of gaben"
"""
import json
import sys
from adapt.intent import IntentBuilder

engine = vocabs.engine

# create regex to parse out sounds
engine.register_regex_entity("(of|show|show me) (?P<Image>.*)")

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

get_intent = IntentBuilder("ImageIntent")\
    .require("ImageVerb")\
    .optionally("ImageKeyword")\
    .optionally("Image")\
    .build()

if __name__ == "__main__":
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))