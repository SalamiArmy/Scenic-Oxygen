from adapt.engine import IntentDeterminationEngine
engine = IntentDeterminationEngine()


import intend_getweather
engine.register_intent_parser(intend_getweather.generate_vocab(engine))

import intend_getsound
engine.register_intent_parser(intend_getsound.generate_vocab(engine))

import intend_get
engine.register_intent_parser(intend_get.generate_vocab(engine))

import intend_getinfo
engine.register_intent_parser(intend_getinfo.generate_vocab(engine))

import intend_getinfo
engine.register_intent_parser(intend_getinfo.generate_vocab(engine))
