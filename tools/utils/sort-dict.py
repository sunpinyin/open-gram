#!/usr/bin/python3
# vim:noet:ts=4:sw=4

# Besides sorting entries bases on the words, this script will also sort
# pinyins of each entry in `hanzi_table.utf8' and `dict.full' in alphabet
# order.
#
# Q: Why bother?
# A: We will benefit from this when we apply mass modifications to pinyin"s
#	(if desirable) in the tables.  Using this script, we will be able to see
#	entries that actually changed ONLY (instead of mixed with changes like
#	that from `唵 n ng an" to `唵 an n ng").

import sys
import sort_criteria

def proc_line(line):
	words = line.strip().split()
	return words[0 : 1] + sorted(words[1 :])

data = [proc_line(l) for l in sys.stdin]
data.sort(key = lambda ws: sort_criteria.entry_sort_key(ws[0]))
sys.stdout.write("".join([" ".join(ws) + "\n" for ws in data]))

