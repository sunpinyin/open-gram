#!/usr/bin/python
# -*- encoding: utf-8 -*-

#
# extract word from segmented corpus, and filter it using a given dictionary
#
# the output will be list of (word, freq)

from __future__ import with_statement
import codecs
import os, sys
from optparse import OptionParser

import wordb
import baseseg
from hanzi_util import is_zh, is_punct
from stopword_filter import is_not_stop_word
from search_filter import get_search_engine


class WordExtractor(object):

    def __init__(self, get_word_freq = None, verbose=False):
        self.get_word_freq = get_word_freq
        self.verbose = verbose
        self.db = wordb.open('./words.db')

        self.filters = [self.is_not_single_character,
                        self.is_chinese_word,
                        self.is_not_AA,
                        is_not_stop_word,
                        self.is_not_known_word]
        
        self.filter_names = {self.is_not_single_character:"is_not_single_character",
                             self.is_chinese_word        :"is_chinese_word",
                             self.is_not_AA              :"is_not_AA",
                             is_not_stop_word            :"is_not_stop_word",
                             self.is_not_known_word      :"is_not_known_word"}

    def __call__(self, words):
        self.process_words(words, 2560000)
        
    def process_files(files):
        """process file in batch
        """
        for fn in files:
            with codecs.open(fn, 'r', 'utf-8') as f:
                self.process_file(f)

    def process_file(self, input_file):
        """process segmented file
        """
        words = set()
        for line in input_file:
            words.add(set(line.split(u'/')))
        self.process_words(words)

    def process_words(self, words, threshold=2560000):
        for word in words:
            for i, keep_the_word in enumerate(self.filters):
                if not keep_the_word(word):
                    self.log("%s\tgets killed by %s" % \
                             (word, self.filter_names[keep_the_word]))
                    break
            else:
                self.log("%s\tadded into db" % word)
                if self.get_word_freq:
                    freq = self.get_word_freq(word)
                    if freq > threshold:
                        self.db[word] = freq
                else:
                    self.db[word] = 1

    def is_not_single_character(self, word):
        """returns True if we want keep this word
        """
        return len(word) > 1

    def is_chinese_word(self, word):
        return word and is_zh(word[0])

    def is_not_known_word(self, word):
        return word not in self.db

    def is_not_AA(self, word):
        return not(len(word) == 2 and word[0] == word[1])
    
    def log(self, message):
        if self.verbose:
            print message



def extract_using_crf():
    default_datadir = '../data'
    default_model = os.path.join(default_datadir , 'model', 'pku-6-tags.model')

    parser = OptionParser()
    parser.add_option("-s", "--search-engine",
                      dest="search_engine")
    parser.add_option("-i", "--input")
    parser.add_option("-m", "--model", default=default_model)
    parser.add_option("-v", "--verbose", action="store_true", default=False)
    opts, args = parser.parse_args()
        
    if opts.input:
        input_files = [opts.input]
    else:
        input_files = args

    
    if opts.search_engine is not None:
        get_word_freq = get_search_engine(search_engine)
    else:
        get_word_freq = None
        
    word_extractor = WordExtractor(get_word_freq, opts.verbose)
    baseseg.process(opts.model, verbose=False,
                    input_files=input_files,
                    dump_func=word_extractor)

if __name__ == "__main__":
    extract_using_crf()
    
