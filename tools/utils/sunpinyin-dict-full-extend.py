#!/usr/bin/python3 -OO
# vim:noet:ts=4:sw=4

import re
import sys
from sunpinyin_char_extend import dictPy

dictInput = "/dev/stdin" if sys.argv[1] == '-' else sys.argv[1]
dictOutput = "/dev/stdout" if sys.argv[2] == '-' else sys.argv[2]

def fmt_chr_info(c):
	return ' '.join([c] + [py for py in dictPy[c]])

patcPercent = re.compile(r"%")
with open(dictOutput, "w") as outputFile:
	for l in open(dictInput):
		if len(l) == 0:
			continue
		c = l.split()[0]
		if len(c) == 1 and c in dictPy and not patcPercent.search(l):
			outputFile.write(fmt_chr_info(c) + "\n")
		else:
			outputFile.write(l)
		if c in dictPy:
			dictPy.pop(c)
	for c in dictPy:
		outputFile.write(fmt_chr_info(c) + "\n")

