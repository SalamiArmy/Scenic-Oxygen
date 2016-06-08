import json
import unittest
import vocabs.intend_getweather as intend_getweather

class TestIntendGetWeather(unittest.TestCase):
    def test_intend_getweather(self):
        intents = intend_getweather.engine.determine_intent("what's the weather like in tokyo")
        self.assertIsNotNone(intents, 'Could not parse intent to get weather.')
        self.assertTrue(len(list(intents)) > 0, 'Could not parse any intents to get weather.')
        for intent in intents:
            self.assertTrue(intent.get('confidence') > 0, 'Intent confidence is too weak for such an explicit utterance of intent.')
            print(json.dumps(intent, indent=4))