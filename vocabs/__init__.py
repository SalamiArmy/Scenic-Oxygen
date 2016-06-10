from adapt.engine import IntentDeterminationEngine
engine = IntentDeterminationEngine()


import intend_getweather
engine.register_intent_parser(intend_getweather.generate_vocab(engine))

import intend_getsound
engine.register_intent_parser(intend_getsound.generate_vocab(engine))

import intend_get
engine.register_intent_parser(intend_get.generate_vocab(engine))

import intend_wiki
engine.register_intent_parser(intend_wiki.generate_vocab(engine))

import intend_getanswer
engine.register_intent_parser(intend_getanswer.generate_vocab(engine))
