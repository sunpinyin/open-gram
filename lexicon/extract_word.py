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
import logging

import wordb
import baseseg
from search_filter import get_search_engine
from filters import Filters

class WordExtractor(object):

    def __init__(self, output_file, get_word_freq = None):
        self.get_word_freq = get_word_freq
        self.new_words = wordb.open(output_file)
        self.filters = Filters()
        self.n_killed = 0
        self.n_added = 0

    def __call__(self, words):
        self.process_words(words, threshold=2560000)
        
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

    def process_words(self, words, threshold=1000000):
        for word in words:
            if self.filters.keep(word) and \
               word not in self.new_words:
                logging.info("%s\tadded into db" % word)
                if self.get_word_freq:
                    freq = self.get_word_freq(word)
                    if freq > threshold:
                        self.new_words[word] = freq
                else:
                    self.new_words[word] = 1
                self.n_added += 1
            else:
                self.n_killed +=1

def extract_using_crf():
    default_datadir = '../data'
    default_model = os.path.join(default_datadir , 'model', 'pku-6-tags.model')

    parser = OptionParser()
    parser.add_option("-s", "--search-engine",
                      dest="search_engine")
    parser.add_option("-i", "--input")
    parser.add_option("-o", "--output", default="./newords.db")
    parser.add_option("-m", "--model", default=default_model)
    parser.add_option("-v", "--verbose", action="store_true", default=False)
    opts, args = parser.parse_args()
        
    if opts.input:
        input_files = [opts.input]
    else:
        input_files = args

    if opts.verbose:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")
    if opts.search_engine is not None:
        get_word_freq = get_search_engine(opts.search_engine)
    else:
        get_word_freq = None

    word_extractor = WordExtractor(get_word_freq=get_word_freq, output_file=opts.output)
    baseseg.process(opts.model, 
                    input_files=input_files,
                    dump_func=word_extractor)
    logging.info("%d words added" % word_extractor.n_added)
    logging.info("%d words killed" % word_extractor.n_killed)

if __name__ == "__main__":
    extract_using_crf()
