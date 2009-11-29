#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
# use search engine as a filter,
#
# if the frequency of occurence of a given words is higher than a threshold,
# then we think it is a popular word
# 

import urllib, urllib2
import re
import sys, os
import codecs
import traceback
import time
import random
import socket

random.seed (time.time ())

class BlockedException(Exception):
    def __init__(self, ip):
        self.ip = ip

    def __str__(self):
        return repr(self.ip)

class SearchEngine(object):
    def choose_ip(self):
        # TODO: should be round-robin, and mark those banned IPs with lower priority
        return random.choice(filter(lambda ip: self.ips[ip] == 0, self.ips))

    def remove_ip(self, ip):
        self.ips[ip] = 1
        
    def is_miss(self, result):
        return self.re_miss.search(lines) is not None

    def get_freq(self, result):
        match = self.re_hit.findall(result)
        if match:
            return int (match[0].replace(',', ''))
        else:
            # could be search engine's suggestion or 
            # it just banned me
            return 0
        
class Baidu(SearchEngine):
    url = "http://%s/s?%s"
    ips = {"121.14.88.14":0,
           "121.14.89.14":0,
           "119.75.213.50":0,
           "119.75.213.51":0,
           "119.75.213.61":0,
           "202.108.22.5":0,
           "202.108.22.43":0,
           "220.181.38.4":0,
           "119.75.216.30":0}
    re_hit = u"找到相关网页约([0-9\,]+)篇"
    re_miss = u"没有找到与.*相关的网页"
    
    def build_url(self, query):
        query = urllib2.quote(query.encode('utf-8'))
        param = urllib.urlencode({'wd':'"%s"' % query, 'ie':'utf-8', 'oe':'utf-8'})
        ip = self.choose_ip()
        return self.url % (ip, param), ip
        
class Google(SearchEngine):
    url = "http://%s/search?%s"
    ips = {
        "203.208.37.104":0,
        "203.208.37.99":0,
        "216.239.51.100":0,
        "216.239.59.103":0,
        "216.239.59.104":0,
        "216.239.59.147":0,
        "216.239.59.99":0,
        "64.233.161.104":0,
        "64.233.161.99":0,
        "64.233.163.104":0,
        "64.233.163.99":0,
        "64.233.169.147":0,
        "64.233.183.91":0,
        "64.233.183.99":0,
        "64.233.187.104":0,
        "64.233.187.107":0,
        "64.233.187.99":0,
        "66.102.11.104":0,
        "66.102.11.99":0,
        "66.102.9.104":0,
        "66.102.9.107":0,
        "66.102.9.147":0,
        "66.102.9.99":0,
        "66.249.89.147":0,
        "72.14.203.104":0,
        "72.14.235.147":0,
        "74.125.19.147":0,
        "74.125.19.103":0}
    re_hit = re.compile (u"获得约 <b>([0-9\,]+)</b> 条结果")
    re_miss = re.compile(u"未找到符合.*的结果")

    def build_url(self, query):
        #query = urllib2.quote(query.encode('utf-8'))
        param = urllib.urlencode({'as_epq': query.encode('utf-8'),
                                  'ie':'utf-8',
                                  'oe':'utf-8',
                                  'hl':'zh_CN',
                                  'c2coff':'1',
                                  'lr':''})
        ip = self.choose_ip()
        return self.url % (ip, param), ip
    
class SearchEngineFilter(object):
    def __init__(self, search_engine, threshold = 100000):
        socket.setdefaulttimeout(15)
        self.threshold = threshold
        self.se = search_engine
        self.http_headers = {'User-agent' : ' '.join('Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.0.3)'
                                                     'Gecko/20080314'
                                                     'Firefox/3.0.3')}
    def get_freq(self, word):
        while True:
            try:
                url, ip = self.se.build_url(word)
                req = urllib2.Request (url, headers=self.http_headers)
                f = urllib2.urlopen (req)
                lines = unicode("".join(f.readlines()), "utf-8")
                return self.se.get_freq(lines)
            except urllib2.URLError,e:
                # this ip is not accessible
                self.se.remove_ip(ip)
            
    def get_freq__(self, word):
        ip = random.choice(filter(lambda ip: self.se.ips[ip] == 0, self.se.ips))
        freq = self.__get_word_freq_from_ip(word, ip)
        if freq >= 0:
            return freq
        else:
            raise BlockedException(ip)
        
    def get_freq_(self, word):
        try:
            ip = random.choice(filter(lambda ip: self.ips[ip] == 0, self.ips))
            freq = self.__get_word_freq_from_ip(word, ip)
            if freq >= 0:
                return freq
            else:
                raise BlockedException(ip)
        except socket.error, e:
            print socket.error,e
        except urllib2.URLError,e:
            g_list[ip] += 1
            print urllib2.URLError, e
        except KeyboardInterrupt, e:
            print >> sys.stderr, "Exit"
            sys.exit (1)
        except Exception, e:
            print e
            print >> sys.stderr, "retry"

def get_search_engine(engine='baidu'):
    if engine == 'baidu':
        search_engine = SearchEngineFilter(Baidu())
    else:
        search_engine = SearchEngineFilter(Google())
    def get_word_freq(word):
        freq = search_engine.get_freq(word)
        return freq
    return get_word_freq

if __name__ == "__main__":
    google_filter = SearchEngineFilter(Google())
    for word in [u'人间', u'大炮']:
        print word, ':', google_filter.get_freq(word)
