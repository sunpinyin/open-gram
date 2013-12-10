#!/usr/bin/python3
# vim:noet:ts=4:sw=4

import sys
from sunpinyin_char_extend import char_dict_gen

dictPy = char_dict_gen(
	"Unihan_Readings.txt" if len(sys.argv) < 2 else sys.argv[1]
)

def fmt_chr_info(c):
	return " ".join([c] + sorted([py for py in dictPy[c]]))

for l in sys.stdin:
	if len(l) == 0:
		continue
	c = l.split()[0]
	if len(c) == 1 and c in dictPy and not "-" in l:
		sys.stdout.write(fmt_chr_info(c) + "\n")
	else:
		sys.stdout.write(l)
	if c in dictPy:
		dictPy.pop(c)

for c in dictPy:
	sys.stdout.write(fmt_chr_info(c) + "\n")

