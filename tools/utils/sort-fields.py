#!/usr/bin/python3
# vim:noet:ts=4:sw=4

# Sort pinyins in `hanzi_table.utf8' and `dict.full' in alphabet order.
#
# Q: Why bother?
# A: We will benefit from this when we apply mass modifications to pinyin"s
#	(if desirable) in the tables.  Using this script, we will be able to see
#	entries that actually changed ONLY (instead of mixed with changes like
#	that from `唵 n ng an" to `唵 an n ng").

import sys

for line in sys.stdin:
	words = line.strip().split()
	if len(words) < heads or line[0] == "#":
		sys.stdout.write(line + "\n")
	else:
		sys.stdout.write(" ".join(
			words[0 : heads] + sorted(words[heads :])
		) + "\n")

