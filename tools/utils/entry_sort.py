#!/usr/bin/python3
# vim:noet:ts=4:sw=4

import sys
import sort_criteria

data = [l.strip().split() for l in sys.stdin]
data.sort(key = lambda ws: sort_criteria.entry_sort_key(ws[0]))
sys.stdout.write("".join([" ".join(ws) + "\n" for ws in data]))

