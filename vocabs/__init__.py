from adapt.engine import IntentDeterminationEngine
engine = IntentDeterminationEngine()


import intend_getweather
engine.register_intent_parser(intend_getweather.weather_intent)

import intend_getsound
engine.register_intent_parser(intend_getsound.music_intent)

import intend_get
engine.register_intent_parser(intend_get.get_intent)
