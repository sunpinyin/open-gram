#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import with_statement
import codecs
import os, sys
from optparse import OptionParser
import logging

import wordb
from stopword_filter import is_stop_word
from hanzi_util import is_zh, is_punct

class Filters(object):
    def __init__(self):
        self.known_words = wordb.open('./words.db')

        self.filters = [self.is_single_character,
                        self.is_not_chinese_word,
                        self.is_AA,
                        is_stop_word,
                        self.is_known_word]
        
        self.filter_names = {self.is_single_character : "is_single_character",
                             self.is_not_chinese_word : "is_not_chinese_word",
                             self.is_AA               : "is_AA",
                             is_stop_word             : "is_stop_word",
                             self.is_known_word       : "is_known_word"}

    def keep(self, word):
        for i, kill_the_word in enumerate(self.filters):
            if not kill_the_word(word):
                logging.info("%s\tgets killed by %s" % \
                             (word, self.filter_names[kill_the_word]))
                return False
        else:
            return True
        
    def is_single_character(self, word):
        """returns True if we want keep this word
        """
        return len(word) == 1

    def is_not_chinese_word(self, word):
        return not (word and is_zh(word[0]))

    def is_known_word(self, word):
        return word in self.db

    def is_AA(self, word):
        return len(word) == 2 and word[0] == word[1]
