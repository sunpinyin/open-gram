#!/usr/bin/python3
# vim:noet:ts=4:sw=4

import sys

dictHead = "../../lexicon/dict_head.utf8" if len(sys.argv) < 2 else sys.argv[1]

for l in open(dictHead):
	sys.stdout.write(l)

i = 100
for l in sys.stdin:
	fields = l.strip().split()
	fields = fields[0 : 1] + [str(i)] + fields[1 :]
	sys.stdout.write(" ".join(fields) + "\n")
	i += 1

