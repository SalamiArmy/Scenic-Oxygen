import unittest
import vocabs

class TestIntentions(unittest.TestCase):
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