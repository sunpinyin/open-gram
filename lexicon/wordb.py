#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import with_statement
import sqlite3
import collections
from operator import itemgetter
from optparse import OptionParser

__all__ = ['error', 'open']

class WordFreqDB(object):
    def __init__(self, filename = 'words.db'):
        self.conn = sqlite3.connect(filename)
        MAKE_TABLE = '''create table if not exists 
                        words (word text primary key, freq integer not null)'''
        MAKE_INDEX = '''create unique index if not exists keyidx on words (word)'''
        self.conn.execute(MAKE_TABLE)
        self.conn.execute(MAKE_INDEX)
        self.conn.commit()
        
    def keys(self):
        GET_KEYS = 'SELECT word FROM words ORDER BY ROWID'
        return map(itemgetter(0), self.conn.cursor().execute(GET_KEYS))

    def values(self):
        GET_VALUES = 'SELECT freq FROM words ORDER BY ROWID'
        return map(itemgetter(0), self.conn.cursor().execute(GET_VALUES))

    def items(self):
        GET_ITEMS = 'SELECT word, freq FROM words ORDER BY ROWID'
        return iter(self.conn.cursor().execute(GET_ITEMS))
    
    def __contains__(self, word):
        GET_ITEM = '''select freq from words where word = ?'''
        return self.conn.execute(GET_ITEM, (word,)).fetchone() is not None

    def __setitem__(self, word, freq):
        ADD_ITEM = '''replace into words (word, freq) values (?, ?)'''
        self.conn.execute(ADD_ITEM, (word, freq))
        # it's too slow to commit every time
        # self.conn.commit()
            
    def __getitem__(self, word):
        GET_ITEM = '''select freq from words where word = ?'''
        item = self.conn.execute(GET_ITEM, (word,)).fetchone()
        if item is None:
            raise KeyError(word)
        return item[0]

    def __delitem__(self, word):
        if word not in self:
            raise KeyError(word)
        DEL_ITEM = '''delete from words where key = ?'''
        self.conn.execute(DEL_ITEM, (key,))
        self.conn.commit()

    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def __del__(self):
        self.close()

def open(file=None, *args):
    if file is not None:
        return WordFreqDB(file)
    return WordFreqDB()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-d', '--db',
                      help='sqlite db file',
                      metavar='DB',
                      default='./wordb.db')
    parser.add_option('-l', '--list',
                      help='list all lemmas in DB',
                      action='store_true', default=False)
    parser.add_option('-q', '--query',
                      metavar='WORD',
                      help='query given WORD in DB')
    opts, args = parser.parse_args()
    if args:
        fname = args[0]
    else:
        fname = opts.db
    db = WordFreqDB(fname)

    if opts.list:
        for w in db.keys():
            print w
    
    if opts.query:
        query = opts.query.decode('utf-8')
        if query in db:
            print opts.query, 'found in', fname
        else:
            print opts.query, 'not found in', fname
