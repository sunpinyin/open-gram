#!/usr/bin/python

# a script to extract syllable from cedict to sunpinyin lexicon format


#from __future__ import with_statement
import sys
import codecs
import re

# the format of cedit looks like
#   <traditional chinese word> <simplfied chinese word> [<pinyins with tones>] /translations|in|english/
# in which, the pinyins are in the form of "yi1 fen1 wei2 er4"
#
# the format of sunpinyin lexicon looks like
#  <simplified chinese word> <word id> pinyin
# in which, the pinyins are in the form of "yi'fen'wei'er"

def normalize_pinyins(pinyins):
    """lower case all pinyins, and remove the tones. if there is no tone, simply raise an exception
    """
    def normalize(py):
        tones = (u'1', u'2', u'3', u'4')
        if py[-1] not in tones:
            raise Exception("not a pinyin: %s" % py)
        return py[:-1].lower()
    return "'".join(normalize(py) for py in pinyins.split())
    
cedict_pattern = re.compile('\S+ (\S+) \[([^\]]+)\] .*')
def transform(line):
    try:
        sc_word, pinyins = cedict_pattern.match(line).groups()
        print sc_word, normalize_pinyins(pinyins)
    except:
        pass                            # just ran into an unknown line or a hybrid word
    
def main(cedict_fname):
    try:
        cedict_file = codecs.open(cedict_fname, "r", "utf-8")
    except:
        print >> sys.stderr, "failed to open %s" % cedict_fname
        sys.exit(1)
    for line in cedict_file:
        if line.startswith(u'#'): continue
        transform(line)
    cedict_file.close()
        
if __name__ == "__main__":
    #cedict_fname = sys.argv[1]
    cedict_fname = "/media/stuff/dev/dev/nlp/cedict_1_0_ts_utf-8_mdbg.txt"
    main(cedict_fname)
