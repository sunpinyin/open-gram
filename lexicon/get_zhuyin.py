#!/usr/bin/python
# coding: utf-8 

from __future__ import with_statement
from sgmllib import SGMLParser
from HTMLParser import HTMLParser
import urllib2, urllib, sys, codecs
import htmlentitydefs

class URLLister(SGMLParser):
    def reset(self):       
        SGMLParser.reset(self)
        self.urls = []
        self.zhuyin = []
        self.data = []
        self.tab1 = ''
        self.tn = 0
        self.intag = 0
        self.status = 0

    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            self.urls.extend(href)

    def start_div(self, attrs):
        for k, v in attrs:
            if k == 'class' and v == 'tab-page':
                self.intag = 1
                self.tab1 = v
                #print (k,v)

    def end_div(self):
        self.intag = 0

    def start_p(self, attrs):
        self.intag = 1

    def end_p(self):
        self.intag = 0

    def start_script(self, attrs):
        for k, v in attrs:
            if k == 'language' and v == 'JavaScript':
                self.status = 1
                self.intag = 1
    
    def end_p(self):
        self.intag = 0


    def handle_data(self, data):
        if self.status == 1 and self.intag == 1:
            self.data.append(data);
            self.intag = 0
            
    def get_zhuyin(self):
        for line in self.data:
            #print line
            if line[0:3] in 'spf':
                if line[5:-3] not in self.zhuyin:
                    self.zhuyin.append(line[5:-3])
        return self.zhuyin



class HandianParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.dictpy = []
        self.in_strong = False
        self.in_dict_py = False
        self.in_tab = False
        
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'strong':
            self.in_strong = True
        elif tag == 'div':
            if 'class' in attrs and attrs['class'] == 'tab-page':
                self.in_tab = True
        elif tag == 'span':
            if 'class' in attrs and attrs['class'] == 'dicpy':
                self.in_dict_py = True
        elif tag == 'hr':
            if 'class' in attrs and attrs['class'] == 'dichr':
                self.in_tab = False
                
    def handle_endtag(self, tag):
        if tag == 'strong':
            pass
        elif tag == 'div':
            self.in_tab = False
        elif tag == 'span':
            self.in_dict_py = False

    def handle_data(self, data):
        if self.in_tab and self.in_dict_py:
            self.dictpy.append(data)
            self.in_dict_py = False
            
    def handle_entityref(self, name):
        if self.in_tab and self.in_dict_py:
            print 'entity'
            print name
            name = name.lower()
            self.handle_data(htmlentitydefs.entitydefs[name])

    def get_zhuyin(self):
        return self.dictpy
    
def post_zdic(zi):
    url = "http://www.zdic.net/search/default.asp"
    search = urllib.urlencode([('q', zi)])
    #print search
    #exit(0)
    req = urllib2.Request(url)
    fd = urllib2.urlopen(req, search)
    return fd
    while 1:
        data = fd.read(1024)
        if not len(data):
            break
        sys.stdout.write(data)

def normalize_hanzi_zhuyin(zhuyin):
    if zhuyin[-1] in '12345':
        return zhuyin[:-1]
    else:
        return zhuyin

def get_hanzi_zhuyin():
    inf = codecs.open(sys.argv[1], 'r', 'utf-8')
    out = codecs.open(sys.argv[2], 'w', 'utf-8')
    parser = URLLister()
    for line in inf:
        parser.reset()
        zi = line.strip()
        parser.feed(post_zdic(zi).read())
        zhuyins = parser.get_zhuyin()
        zhuyins = ' '.join(normalize_hanzi_zhuyin(zhuyin) for zhuyin in zhuyins)
        #zhuyins = ' '.join(zhuyins)
        print zi, zhuyins
        print >> out, zi, zhuyins

vowels = {u'ā':'a1',
          u'á':'a2',
          u'ǎ':'a3',
          u'à':'a4',
          u'a':'a5',
          
          u'ō':'o1',
          u'ó':'o2',
          u'ǒ':'o3',
          u'ò':'o4',
          
          u'ē':'e1',
          u'é':'e2',
          u'ě':'e3',
          u'è':'e4',
        
          u'āi':'ai1',
          u'ái':'ai2',
          u'ǎi':'ai3',
          u'ài':'ai4',
          
          u'ēi':'ei1',
          u'éi':'ei2',
          u'ěi':'ei3',
          u'èi':'ei4',
          
          u'āo':'ao1',
          u'áo':'ao2',
          u'ǎo':'ao3',
          u'ào':'ao4',

          u'ōu':'ou1',
          u'óu':'ou2',
          u'ǒu':'ou3',
          u'òu':'ou4',
          
          u'ān':'an1',
          u'án':'an2',
          u'ǎn':'an3',
          u'àn':'an4',
          u'an':'an5',
          
          u'ēn':'en1',
          u'én':'en2',
          u'ěn':'en3',
          u'èn':'en4',

          u'āng':'ang1',
          u'áng':'ang2',
          u'ǎng':'ang3',
          u'àng':'ang4',
         
          u'ēng':'eng1',
          u'éng':'eng2',
          u'ěng':'eng3',
          u'èng':'eng4',

          u'ēr':'er1',
          u'ér':'er2',
          u'ěr':'er3',
          u'èr':'er4',

          u'ī':'i1',
          u'í':'i2',
          u'ǐ':'i3',
          u'ì':'i4',

          u'iā':'ia1',
          u'iá':'ia2',
          u'iǎ':'ia3',
          u'ià':'ia4',

          u'iē':'ie1',
          u'ié':'ie2',
          u'iě':'ie3',
          u'iè':'ie4', 

          u'iāo':'iao1',
          u'iáo':'iao2',
          u'iǎo':'iao3',
          u'iào':'iao4',
         
          u'iū':'iu1',
          u'iú':'iu2',
          u'iǔ':'iu3',
          u'iù':'iu4',
         
          u'iān':'ian1',
          u'ián':'ian2',
          u'iǎn':'ian3',
          u'iàn':'ian4',
         
          u'īn':'in1',
          u'ín':'in2',
          u'ǐn':'in3',
          u'ìn':'in4',
         
          u'iāng':'iang1',
          u'iáng':'iang2',
          u'iǎng':'iang3',
          u'iàng':'iang4',
         
          u'īng':'ing1',
          u'íng':'ing2',
          u'ǐng':'ing3',
          u'ìng':'ing4',
         
          u'ū':'u1',
          u'ú':'u2',
          u'ǔ':'u3',
          u'ù':'u4',
         
          u'uā':'ua1',
          u'uá':'ua2',
          u'uǎ':'ua3',
          u'uà':'ua4',
         
          u'uō':'uo1',
          u'uó':'uo2',
          u'uǒ':'uo3',
          u'uò':'uo4',
         
          u'uāi':'uai1',
          u'uái':'uai2',
          u'uǎi':'uai3',
          u'uài':'uai4',
         
          u'uī':'ui1',
          u'uí':'ui2',
          u'uǐ':'ui3',
          u'uì':'ui4',
         
          u'uān':'uan1',
          u'uán':'uan2',
          u'uǎn':'uan3',
          u'uàn':'uan4',

          u'ūn':'un1',
          u'ún':'un2',
          u'ǔn':'un3',
          u'ùn':'un4',
         
          u'uāng':'uang1',
          u'uáng':'uang2',
          u'uǎng':'uang3',
          u'uàng':'uang4',
         
          u'ōng':'ong1',
          u'óng':'ong2',
          u'ǒng':'ong3',
          u'òng':'ong4',

          u'uē':'ue1',
          u'ué':'ue2',
          u'uě':'ue3',
          u'uè':'ue4',
         
          u'iōng':'iong1',
          u'ióng':'iong2',
          u'iǒng':'iong3',
          u'iòng':'iong4',

          u'ǖ':'v1',
          u'ǘ':'v2',
          u'ǚ':'v3',
          u'ǜ':'v4'
         }

def normalize_word_zhuyin(zhuyin):
    for v in vowels:
        if zhuyin.endswith(v):
            zhuyin = zhuyin.replace(v, vowels[v])
            if zhuyin[-1] in '12345':
                zhuyin = zhuyin[:-1]
            break
    return zhuyin

def seek_to_last_word(input, output):
    last_word = None
    for line in output:
        last_word, py = line.split(' ', 1)
    if last_word is None:
        return
    print last_word, py                                                                                        
    for line in input:
        word, py = line.split(' ', 1)
        if word == last_word:
            break

def validate_words():
    inf = codecs.open(sys.argv[1], 'r', 'utf-8')
    out = codecs.open(sys.argv[2], 'a+', 'utf-8')
    parser = HandianParser()
    seek_to_last_word(inf, out)
    for line in inf:
        parser.reset()
        word, py, freq = line.strip().split()
        if len(word) > 1:
            parser.feed(post_zdic(word).read())
            zhuyins = parser.get_zhuyin()
            if zhuyins:
                zhuyin = zhuyins[0].strip()
                zhuyin = "'".join(normalize_word_zhuyin(py) for py in zhuyin.split())
                if zhuyin != py:
                    print word, ":", zhuyin, "!=", py
                    py = zhuyin
            else:
                print word, 'not found in zdic'
        print word, py, freq
        print >> out, word, py, freq
        
    #print >> out, zi, zhuyins
    
def get_zi():
    try: 
        f = codecs.open('shengdiao.unKnow.utf8', 'r', 'utf-8')
        for line in f:
            line.strip()
            wds = line.split()
            if wds[0] not in ('#', '<', '\n'):
                if wds[2] == '?':
                    yins = main_handle(wds[0])
                    yin = '\''.join(yins)
                    print '%s %s %s' % (wds[0], wds[1], yin)
        f.close()
    except:
        print 'can not open file:shengdiao.unKnow.utf8'

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    get_hanzi_zhuyin()
