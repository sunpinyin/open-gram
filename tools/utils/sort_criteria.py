#!/usr/bin/python3
# vim:noet:ts=4:sw=4

# Sort words by:
# 1. Length of words (eg. `啊' -> 1 ; `测试' -> 2).
# 2. Text of words in zh_CN.UTF-8 collation order.
# 3. Unicode code points of words.
#
# Q: Why change sorting criteria again?
# A: In this way, modification of pinyin will not change order of entries.
#    (BTW, the zh_CN.UTF-8 collation is VERY stable and should hopefully
#    not mess up these tables across updates of the locale itself.)
# Q: But some words with characters which correspond to multiple pinyins
#    seem to get into wrong positions.
# A: This should not interfere with our normal use of the tables, other
#    than visually slightly uncomfortable.

import functools
import locale

locale.setlocale(locale.LC_COLLATE, "zh_CN.UTF-8")

def ret_if_non_zero(funcs):
	def result(*args):
		for f in funcs:
			val = f(*args)
			if val != 0:
				return val
	return result

def cmp_from_gt_lt(x, y):
	return (x > y) - (x < y)

def cmp_from_key(f):
	return lambda x, y: f(x) - f(y)

def cmp_from_key_alt(f):
	return lambda x, y: cmp_from_gt_lt(f(x), f(y))

entry_sort_key = functools.cmp_to_key(ret_if_non_zero([
	cmp_from_key(len), locale.strcoll,
	cmp_from_key_alt(lambda w: list(map(ord, w)))
]))

