#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import with_statement
import codecs

__all__ = ['is_not_stop_word',
           'is_stop_word']

class StopWordFilter(object):
    def __init__(self):
        self.prefix = []
        self.postfix = []
        self.update()
        
    def update(self, path = '../data/stopword.utf8'):
        with codecs.open(path, 'r', 'utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                stopword, flag = line.split()
                if flag == u'1':
                    self.postfix.append(stopword)
                elif flag == u'0':
                    self.prefix.append(stopword)

    def is_stop_word(self, word):
        for prefix in self.prefix:
            if word.startswith(prefix):
                return True
        for postfix in self.postfix:
            if word.endswith(postfix):
                return True
        return False

stopword_filter = StopWordFilter()

def is_stop_word(word):
    return stopword_filter.is_stop_word(word)

def is_not_stop_word(word):
    return not stopword_filter.is_stop_word(word)

