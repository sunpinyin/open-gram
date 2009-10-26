#!/usr/bin/python

# a script to extract syllable from cedict to sunpinyin lexicon format


#from __future__ import with_statement
import sys
import codecs
import re
from optparse import OptionParser

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

def transform(line, dump_func):
    try:
        sc_word, pinyins = cedict_pattern.match(line).groups()
        dump_func(sc_word, normalize_pinyins(pinyins))
    except:
        pass                            # just ran into an unknown line or a hybrid word
    
def dump(cedict_fname, dump_func):
    try:
        cedict_file = codecs.open(cedict_fname, "r", "utf-8")
    except:
        print >> sys.stderr, "failed to open %s" % cedict_fname
        sys.exit(1)
    for line in cedict_file:
        if line.startswith(u'#'): continue
        transform(line, dump_func)
    cedict_file.close()

def dump_to_file(filename):
    if filename == '-':
        f = sys.stdout
    else:
        f = file(filename)
    def dump_func(sc_word, pinyins):
        print >> f, sc_word, pinyins
    return dump_func

def dump_to_db(filename):
    import wordb
    db = wordb.open(filename)
    def dump_func(word, pinyins):
        db[word] = 1
    return dump_func
        
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--dict",
                      help="uncompressed cedict file",
                      metavar="DICT",
                      default="../data/cedict_1_0_ts_utf-8_mdbg.txt")
    parser.add_option("-m", "--db",
                      help="dump DICT to the sqlite3 DB",
                      metavar="DB")
    parser.add_option("-o", "--output",
                      help="dump simplified Chinese words and its pinyin from DICT to FILE",
                      metavar="FILE")
    opts, args = parser.parse_args()
    
    if opts.dict:
        cedict_fname = opts.dict
    elif args:
        cedict_fname = args[0]
    else:
        default_cedict = '../data/cedict_1_0_ts_utf-8_mdbg.txt'
        print >> sys.stderr, 'using %s as the dict' % default_cedict
        cedict_fname = default_cedict

    if opts.output:
        dump_func = dump_to_file(opts.output)
    elif opts.db:
        dump_func = dump_to_db(opts.db)
    else:
        dump_func = dump_to_file('-')
    dump(cedict_fname, dump_func)
