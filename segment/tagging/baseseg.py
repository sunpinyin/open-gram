#!/usr/bin/python

from __future__ import with_statement
import sys
import os
import codecs
import crfpp
import preprocess

class CRFPP(object):
    def __init__(self, **args):
        # args = '-m ../model -v 3 -n 2'
        self.verbose = False
        if 'verbose' in args:
            self.verbose = args['verbose']
            del(args['verbose'])
        arg_str = ' '.join([' '.join(['-'+k,str(v)]) for k,v in args.items()])
        self.tagger = crfpp.Tagger(arg_str)
        
    def segment(self, tokens, delimeter=u'/'):
        self.tagger.clear()
        for token in tokens:
            self.tagger.add(token.encode('utf-8'))
        if self.verbose:
            print "column size: " , self.tagger.xsize()
            print "token size: " , self.tagger.size()
            print "tag size: " , self.tagger.ysize()
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
        if self.verbose:
            print ''.join(tokens)
        delimeter.join(words)
                
    def __call__(self, tokens):
        return self.segment(tokens)

def process_file(segment, filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        for sentence in preprocess.process(f):
            yield segment(sentence)


def process_dir(segment, dirname):
    for root, dirs, files in os.walk(dirname):
        for fn in files:
            process_file(segment, os.path.join(root, fn))
    
if __name__ == "__main__":
    datadir = '../data'
    model = os.path.join(datadir , 'model', 'pku-6-tags.model')
    segment = CRFPP(m=model, verbose=False)
    for dirname in sys.argv[1:]:
        process_dir(segment, dirname)

                
                    
