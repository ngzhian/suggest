import unittest

from .views import _filter_nyt_keywords, clean_url


class KeywordTest(unittest.TestCase):
    def test_keywords(self):
        KEYWORDS = [{
            "rank": "1",
            "name": "persons",
            "value": "Earnest, Josh"
        }, {
            "rank": "2",
            "name": "persons",
            "value": "Obama, Barack"
        }, {
            "rank": "1",
            "name": "subject",
            "value": "Vetoes (US)"
        }, {
            "rank": "3",
            "name": "subject",
            "value": "Vetoes (US)",
            "is_major": "N"
        }]

        expected = ['Earnest, Josh', 'Vetoes (US)', 'Obama, Barack']
        self.assertEquals(expected, _filter_nyt_keywords(KEYWORDS))

    def test_url(self):
        url = 'http:\/\/www.nytimes.com\/politics\/first-draft\/2014\/11\/13\/white-house-hints-at-xl-pipeline-veto\/'
        expected = 'http://www.nytimes.com/politics/first-draft/2014/11/13/white-house-hints-at-xl-pipeline-veto/'
        self.assertEquals(expected, clean_url(url))
