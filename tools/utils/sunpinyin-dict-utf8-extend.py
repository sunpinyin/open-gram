#!/usr/bin/python3
# vim:noet:ts=4:sw=4

import sys
import sunpinyin_char_extend

dictPy = sunpinyin_char_extend.char_dict_gen(
	"Unihan_Readings.txt" if len(sys.argv) < 2 else sys.argv[1]
)

def fmt_chr_info(c, idx):
	return " ".join([c, str(idx)] + sorted([py for py in dictPy[c]]))

for l in sys.stdin:
	if len(l) == 0:
		continue
	c = l.split()[0]
	idx = int(l.split()[1])
	if len(c) == 1 and c in dictPy and not "%" in l:
		sys.stdout.write(fmt_chr_info(c, idx) + "\n")
	else:
		sys.stdout.write(l)
	if c in dictPy:
		dictPy.pop(c)

for c in dictPy:
	idx += 1
	sys.stdout.write(fmt_chr_info(c, idx) + "\n")

