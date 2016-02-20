#!/usr/bin/python3
# vim:noet:ts=4:sw=4

import sys

dic = {}
ngrams = []
dicFiles = sys.argv[1 :] if len(sys.argv) > 1 else \
	["../../lexicon/dict_head.utf8", "../../data/dict.full"]

def proc_ngrams():
	ngrams.sort(key = lambda ws: [dic.get(w) for w in ws])
	sys.stdout.write("".join([" ".join(ws) for ws in ngrams]))
	ngrams.clear()

i = 0
for f in dicFiles:
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

