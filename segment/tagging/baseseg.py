#!/usr/bin/python

from __future__ import with_statement
import sys, errno
import os
import codecs
from optparse import OptionParser
import logging

import crfpp
import preprocess

class CRFPP(object):
    def __init__(self, **args):
        # args = '-m ../model -v 3 -n 2'
        arg_str = ' '.join([' '.join(['-'+k,str(v)]) for k,v in args.items()])
        self.tagger = crfpp.Tagger(arg_str)
        
    def segment(self, tokens):
        self.tagger.clear()
        for token in tokens:
            self.tagger.add(token.encode('utf-8'))
        logging.debug("column size: %d" % self.tagger.xsize())
        logging.debug("token size: %d" % self.tagger.size())
        logging.debug("tag size: %d" % self.tagger.ysize())
        self.tagger.parse()
        words = []
        word = []
        for i in xrange(self.tagger.size() - 1):
            tag = self.tagger.y2(i)
            if tag in ('B', 'S') and word:
                words.append(''.join(word))
                word = []
            word.append(tokens[i])
        if word:
            words.append(''.join(word))
        logging.debug(''.join(tokens))
        return words
                
    def __call__(self, tokens):
        return self.segment(tokens)

def process_file(segment, filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        for sentence in preprocess.process(f):
            yield segment(sentence)

def makedir(dirname):
    try:
        os.makedirs(dirname)
    except OSError, e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise
    
def make_output_dir(in_basedir, dirname, output_base):
    output_dir = os.path.join(output_base, dirname[len(in_basedir):])
    makedir(output_dir)
    return output_dir
        

def print_words(words, delimeter=u'/'):
    print delimeter.join(words)

def process_dir(segment, input_dir, dump_func=print_words):
    for root, dirs, files in os.walk(input_dir):
#         if files:
#             make_output_dir(input_dir, root, output_dir)
        for fn in files:
            for words in process_file(segment, os.path.join(root, fn)):
                dump_func(words)

def process(model, input_files, dump_func):
    segment = CRFPP(m=model)
    for filename in input_files:
        if os.path.isfile(filename):
            process_file(segment, filename)
        elif os.path.isdir(filename):
            process_dir(segment, filename, dump_func)

if __name__ == "__main__":
    
    default_datadir = '../data'
    default_model = os.path.join(default_datadir , 'model', 'pku-6-tags.model')

    parser = OptionParser()
    parser.add_option("-i", "--input")
    parser.add_option("-o", "--output")
    parser.add_option("-m", "--model", default=default_model)
    parser.add_option("-v", "--verbose", action="store_true", default=False)
    opts, args = parser.parse_args()

    if opts.input:
        input_files = [opts.input]
    else:
        input_files = args

    if opts.output:
        output_dir = opts.output
    else:
        output_dir = None

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)
    process(opts.model, opts.verbose, input_files, print_words)
