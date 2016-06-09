import ConfigParser
import unittest

import vocabs
import vocabs.intend_getweather as intend_getweather


class TestIntentions(unittest.TestCase):
    def test_intend_getweather(self):
        intent = vocabs.engine.determine_intent("what's the weather like in tokyo", 1).next()
        self.assertIsNotNone(intent, 'Could not parse intent to get weather.')
        self.assertTrue(intent.get('confidence') > 0,
                        'Intent confidence is too weak for such an explicit utterance of intent.')
        self.assertTrue(intent.get('Location') == 'tokyo', 'Cannot get location for intention to get weather.')

    def test_intend_getsound(self):
        intent = vocabs.engine.determine_intent("i want to listen to some music now please", 1).next()
        self.assertIsNotNone(intent, 'Could not parse intent to get sound.')
        self.assertTrue(intent.get('confidence') > 0,
                        'Intent confidence is too weak for such an explicit utterance of intent.')
