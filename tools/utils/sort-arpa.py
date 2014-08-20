#!/usr/bin/python3
# vim:noet:ts=4:sw=4

import sys

ngrams = []
dic = {}
dics = sys.argv[1 :] if len(sys.argv) > 1 else \
	["../../lexicon/dict_head.utf8", "../../data/dict.full"]

def dic_key():
	key = lambda w: (dic[w] if w in dic else -1)
	return lambda ws: list(map(key, ws))

def proc_ngrams():
	ngrams.sort(key = dic_key())
	sys.stdout.write("".join([" ".join(ws) for ws in ngrams]))
	ngrams.clear()

i = 0
for f in dics:
	for l in open(f):
		dic[l.split()[0]] = i
		i += 1

for l in sys.stdin:
	if l[0] == "\\":
		proc_ngrams()
		sys.stdout.write(l)
	else:
		ngrams.append(l.split(" "))
proc_ngrams()

