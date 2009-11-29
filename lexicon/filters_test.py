#!/usr/bin/python
# -*- encoding: utf-8 -*-

import unittest
from filters import Filters
from stopword_filter import is_stop_word

class FilterStopWords(unittest.TestCase):
    def testPrefix(self):
        stop_words = [u'很多',
                      u'每个']
        for w in stop_words:
            self.assertTrue(is_stop_word(w))

    def testPostfix(self):
        stop_words = [u'吃的',
                      u'图中']
        for w in stop_words:
            self.assertTrue(is_stop_word(w))
            
class WordsToBeKilled(unittest.TestCase):
    def setUp(self):
        self.filters = Filters()

    def tearDown(self):
        self.filters = None
        
    def testKnownWords(self):
        known_words = [u'知识']
        for w in known_words:
            self.assertTrue(self.filters.is_known_word(w))

    def testNonChineseword(self):
        non_chinese = [u'Chinese',
                       u'[',
                       u'，',
                       u'   ']
        for w in non_chinese:
            self.assertTrue(self.filters.is_not_chinese_word(w))

    def testAA(self):
        aa_words = [u'天天',
                    u'年年']
        for w in aa_words:
            self.assertTrue(self.filters.is_AA(w))

    def testNumber(self):
        number_words = [u'千万',
                        u'几个亿',
                        u'一九三八',
                        u'十三万二千五百三十五']
        for w in number_words:
            self.assertTrue(self.filters.is_number(w))

if __name__ == '__main__':
    unittest.main()
    
