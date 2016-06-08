import unittest

import vocabs.intend_getweather as intend_getweather


class TestIntendGetWeather(unittest.TestCase):
    def test_intend_getweather(self):
        intent = intend_getweather.engine.determine_intent("what's the weather like in tokyo", 1).next()
        self.assertIsNotNone(intent, 'Could not parse intent to get weather.')
        self.assertTrue(intent.get('confidence') > 0,
                        'Intent confidence is too weak for such an explicit utterance of intent.')
