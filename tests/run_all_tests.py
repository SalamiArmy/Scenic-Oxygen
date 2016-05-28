
def run(self):
    testmodules = [
        'tests.test_bitcoin',
        'tests.test_cric',
        'tests.test_get',
        'tests.test_getbook',
        'tests.test_getfig',
        'tests.test_getgif',
        'tests.test_gethuge',
        'tests.test_gethugegif',
        'tests.test_getlyrics',
        'tests.test_getmovie',
        'tests.test_getquote',
        'tests.test_getshow',
        'tests.test_getvid',
        'tests.test_getweather',
        'tests.test_getxxx',
        'tests.test_giphy',
        'tests.test_iss',
        'tests.test_place',
        'tests.test_rand',
        'tests.test_torrent',
        'tests.test_translate',
        'tests.test_urban',
        'tests.test_wiki',
        'tests.test_define',
        'tests.test_getanswer',
        'tests.test_getgame',
        'tests.test_getsound',
        'tests.test_imgur',
        'tests.test_isis',
        'tests.test_launch',
        'tests.test_mc',
        'tests.test_reverseimage',
        'tests.test_define',
        'tests.test_getanswer',
        'tests.test_getgame',
        'tests.test_getsound',
        'tests.test_imgur',
        'tests.test_isis',
        'tests.test_launch',
        'tests.test_mc',
        'tests.test_reverseimage',
    ]
    suite = unittest.TestSuite()
    formattedResultText = ''
    for t in testmodules:
        try:
            getTest = unittest.defaultTestLoader.loadTestsFromName(t)
            suite.addTest(getTest)
        except:
            formattedResultText += "Unexpected error during import of module " + \
                                   t + ": " + str(sys.exc_info()[1]) + '\n'
    formattedResultText += str(unittest.TextTestRunner().run(suite)) \
        .replace('<unittest.runner.TextTestResult ', '') \
        .replace('>', '')
    self.response.write(formattedResultText)