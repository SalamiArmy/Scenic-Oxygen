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

    def test_intend_get_shit(self):
        testPassed = False
        for intent in vocabs.engine.determine_intent("Show me a human shit"):
            self.assertIsNotNone(intent, 'Could not parse intent to get image.')
            self.assertTrue('Image' in intent, 'Could not parse Image from intent to get image.')
            self.assertTrue(intent.get('Image') == 'a human shit', 'Parsed wrong Image from intent to get image.')
            testPassed = True
        self.assertTrue(testPassed, 'Cannot find intent to get image in multi-intent parser')

    def test_intend_get_gaben(self):
        testPassed = False
        for intent in vocabs.engine.determine_intent("shOw gaben", 3):
            self.assertIsNotNone(intent, 'Could not parse intent to get image.')
            self.assertTrue('Image' in intent, 'Could not parse Image from intent to get image.')
            self.assertTrue(intent.get('Image') == 'gaben', 'Parsed wrong Image from intent to get image.')
            testPassed = True
        self.assertTrue(testPassed, 'Cannot find intent to get image in multi-intent parser')

    def test_multiintentionparser(self):
        count = 0
        for intent in vocabs.engine.determine_intent(
                "what's the weather like in tokyo and "
                "i want to listen to some music now please and "
                "i want to see the visage of gaben", 3):
            self.assertIsNotNone(intent, 'Could not parse intent.')
            self.assertTrue('Image' in intent if 'ImageVerb' in intent else True,
                            'Could not get Image from intent to get image.')
            self.assertTrue('Sound' in intent if 'MusicVerb' in intent else True,
                            'Cannot find intent to get image in multi-intent parser')
            self.assertTrue('Location' in intent and intent.get('Location') == 'tokyo' if 'WeatherKeyword' in intent else True,
                            'Cannot get location for intention to get weather.')
            count += 1
        self.assertEqual(count, 3, 'Not enough intentions found.')
