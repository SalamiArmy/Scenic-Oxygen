import unittest

import vocabs


class TestIntentions(unittest.TestCase):
    def test_intend_getweather(self):
        testPassed = False
        for intent in vocabs.engine.determine_intent("what's the weather like in tokyo", 3):
            self.assertIsNotNone(intent, 'Could not parse intent to get weather.')
            self.assertTrue(intent.get('confidence') > 0,
                            'Intent confidence is too weak for such an explicit utterance of intent.')
            self.assertTrue(intent.get('Location') == 'tokyo', 'Cannot get location for intention to get weather.')
            testPassed = True
        self.assertTrue(testPassed, 'Cannot find intent to get image in multi-intent parser')

    def test_intend_getsound(self):
        testPassed = False
        for intent in vocabs.engine.determine_intent("i want to listen to some music now please", 3):
            self.assertIsNotNone(intent, 'Could not parse intent to get sound.')
            self.assertTrue(intent.get('confidence') > 0,
                            'Intent confidence is too weak for such an explicit utterance of intent.')
            testPassed = True
        self.assertTrue(testPassed, 'Cannot find intent to get image in multi-intent parser')

    def test_intend_get(self):
        testPassed = False
        for intent in vocabs.engine.determine_intent("i want to see the visage of gaben", 3):
            self.assertIsNotNone(intent, 'Could not parse intent to get image.')
            self.assertTrue('ImageVerb' in intent, 'Could not get ImageVerb from intent to get image.')
            self.assertTrue('Image' in intent, 'Could not get Image from intent to get image.')
            testPassed = True
        self.assertTrue(testPassed, 'Cannot find intent to get image in multi-intent parser')
