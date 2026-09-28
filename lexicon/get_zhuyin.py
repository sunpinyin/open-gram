#!/usr/bin/python3
# coding: utf-8 

from html.parser import HTMLParser
import urllib.request
import urllib.parse
import sys
import codecs

class URLLister(HTMLParser):
    def reset(self):       
        HTMLParser.reset(self)
        self.urls = []
        self.zhuyin = []
        self.data = []
        self.tab1 = ''
        self.tn = 0
        self.intag = 0
        self.status = 0

    def handle_starttag(self, tag, attrs):
        method = getattr(self, 'start_' + tag, None)
        if method is not None:
            method(attrs)

    def handle_endtag(self, tag):
        method = getattr(self, 'end_' + tag, None)
        if method is not None:
            method()

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

    def get_zhuyin(self):
        return self.dictpy
    
def response_html(response):
    """Return response body text for HTMLParser.feed."""
    data = response.read()
    headers = getattr(response, 'headers', None)
    encoding = None
    if headers is not None:
        encoding = headers.get_content_charset()
    return data.decode(encoding or 'utf-8')

def post_zdic(zi):
    url = "http://www.zdic.net/search/default.asp"
    search = urllib.parse.urlencode([('q', zi)]).encode('ascii')
    #print search
    #exit(0)
    req = urllib.request.Request(url, data=search)
    fd = urllib.request.urlopen(req)
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
        parser.feed(response_html(post_zdic(zi)))
        zhuyins = parser.get_zhuyin()
        zhuyins = ' '.join(normalize_hanzi_zhuyin(zhuyin) for zhuyin in zhuyins)
        #zhuyins = ' '.join(zhuyins)
        print(zi, zhuyins)
        print(zi, zhuyins, file=out)

vowels = {'ā':'a1',
          'á':'a2',
          'ǎ':'a3',
          'à':'a4',
          'a':'a5',
          
          'ō':'o1',
          'ó':'o2',
          'ǒ':'o3',
          'ò':'o4',
          
          'ē':'e1',
          'é':'e2',
          'ě':'e3',
          'è':'e4',
        
          'āi':'ai1',
          'ái':'ai2',
          'ǎi':'ai3',
          'ài':'ai4',
          
          'ēi':'ei1',
          'éi':'ei2',
          'ěi':'ei3',
          'èi':'ei4',
          
          'āo':'ao1',
          'áo':'ao2',
          'ǎo':'ao3',
          'ào':'ao4',

          'ōu':'ou1',
          'óu':'ou2',
          'ǒu':'ou3',
          'òu':'ou4',
          
          'ān':'an1',
          'án':'an2',
          'ǎn':'an3',
          'àn':'an4',
          'an':'an5',
          
          'ēn':'en1',
          'én':'en2',
          'ěn':'en3',
          'èn':'en4',

          'āng':'ang1',
          'áng':'ang2',
          'ǎng':'ang3',
          'àng':'ang4',
         
          'ēng':'eng1',
          'éng':'eng2',
          'ěng':'eng3',
          'èng':'eng4',

          'ēr':'er1',
          'ér':'er2',
          'ěr':'er3',
          'èr':'er4',

          'ī':'i1',
          'í':'i2',
          'ǐ':'i3',
          'ì':'i4',

          'iā':'ia1',
          'iá':'ia2',
          'iǎ':'ia3',
          'ià':'ia4',

          'iē':'ie1',
          'ié':'ie2',
          'iě':'ie3',
          'iè':'ie4', 

          'iāo':'iao1',
          'iáo':'iao2',
          'iǎo':'iao3',
          'iào':'iao4',
         
          'iū':'iu1',
          'iú':'iu2',
          'iǔ':'iu3',
          'iù':'iu4',
         
          'iān':'ian1',
          'ián':'ian2',
          'iǎn':'ian3',
          'iàn':'ian4',
         
          'īn':'in1',
          'ín':'in2',
          'ǐn':'in3',
          'ìn':'in4',
         
          'iāng':'iang1',
          'iáng':'iang2',
          'iǎng':'iang3',
          'iàng':'iang4',
         
          'īng':'ing1',
          'íng':'ing2',
          'ǐng':'ing3',
          'ìng':'ing4',
         
          'ū':'u1',
          'ú':'u2',
          'ǔ':'u3',
          'ù':'u4',
         
          'uā':'ua1',
          'uá':'ua2',
          'uǎ':'ua3',
          'uà':'ua4',
         
          'uō':'uo1',
          'uó':'uo2',
          'uǒ':'uo3',
          'uò':'uo4',
         
          'uāi':'uai1',
          'uái':'uai2',
          'uǎi':'uai3',
          'uài':'uai4',
         
          'uī':'ui1',
          'uí':'ui2',
          'uǐ':'ui3',
          'uì':'ui4',
         
          'uān':'uan1',
          'uán':'uan2',
          'uǎn':'uan3',
          'uàn':'uan4',

          'ūn':'un1',
          'ún':'un2',
          'ǔn':'un3',
          'ùn':'un4',
         
          'uāng':'uang1',
          'uáng':'uang2',
          'uǎng':'uang3',
          'uàng':'uang4',
         
          'ōng':'ong1',
          'óng':'ong2',
          'ǒng':'ong3',
          'òng':'ong4',

          'uē':'ue1',
          'ué':'ue2',
          'uě':'ue3',
          'uè':'ue4',
         
          'iōng':'iong1',
          'ióng':'iong2',
          'iǒng':'iong3',
          'iòng':'iong4',

          'ǖ':'v1',
          'ǘ':'v2',
          'ǚ':'v3',
          'ǜ':'v4'
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
    print(last_word, py)
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
            parser.feed(response_html(post_zdic(word)))
            zhuyins = parser.get_zhuyin()
            if zhuyins:
                zhuyin = zhuyins[0].strip()
                zhuyin = "'".join(normalize_word_zhuyin(py) for py in zhuyin.split())
                if zhuyin != py:
                    print(word, ":", zhuyin, "!=", py)
                    py = zhuyin
            else:
                print(word, 'not found in zdic')
        print(word, py, freq)
        print(word, py, freq, file=out)
        
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
                    print('%s %s %s' % (wds[0], wds[1], yin))
        f.close()
    except:
        print('can not open file:shengdiao.unKnow.utf8')

if __name__ == '__main__':
    get_hanzi_zhuyin()
