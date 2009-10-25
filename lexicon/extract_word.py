#!/usr/bin/python

#
# extract word from segmented corpus, and filter it using a given dictionary
#
# the output will be list of (word, freq)

from __future__ import with_statement
import codecs
import sys
import wordb
from hanzi_util import is_zh, is_punct

db = wordb.open('../data/wordb.db')

#
# filters: returns True if we want keep this word
#
def is_not_single_character(word):
    return len(word) > 1:

def is_chinese_word(word):
    return word and is_zh(word[0])

def is_not_known_word(word):
    return word not in db:

def get_search_engine_filter(engine='baidu', threshold):
    if engine == 'baidu':
        search_engine = SearchEngineFilter(Baidu())
    else:
        search_engine = SearchEngineFilter(Google())
    def search_engine_filter(word):
        freq = search_engine.get_freq(word)
        if freq > threshold:
            db[word] = freq
            return True
        else:
            return False
    return search_engine_filter
    
def process(input_file):
    filters = [is_not_single_character,
               is_chinese_word,
               is_not_known_word,
               get_search_engine_filter('baidu', 100000)]
    for line in input_file:
        words = line.split(u'/')
        for word in words:
            for keep_the_word in filters:
                if not keep_the_word(word):
                    continue
            else:
                print 'adding', word, 'into db'

if __name__ == "__main__":
    for fn in sys.argv[1:]:
        with codecs.open(fn, 'r', 'utf-8') as f:
            process(fn)
