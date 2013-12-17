#!/usr/bin/python3
# vim:noet:ts=4:sw=4
# coding=UTF-8

import re

# Functions to process Unihan data.

def codepoint_to_chr(s):
	return chr(int(re.sub(r"^U\+", "", s), 16))

def get_unihan_properties(prop, fname):
	patLine = "\t".join([r"(U\+[0-9A-F]+)", "(" + prop + ")", "([^\t]+)"])
	patcLine = re.compile("^" + patLine + "$")
	return map(
		(lambda ss: (codepoint_to_chr(ss[0]), ss[2])),
		[m.groups() for m in filter(
			(lambda x: x != None),
			map(patcLine.match, open(fname))
		)]
	)

# Functions to process pinyin strings.

def py_u_to_v(py):
	return re.sub(r"([ln])[ǖǘǚǜü]", r"\1v", py)

def py_rm_accent(py):
	dictPyTrans = str.maketrans(
		"āáǎàōóǒòēéěèīíǐìūúǔùǖǘǚǜüḿńňǹ", "aaaaooooeeeeiiiiuuuuuuuuumnnn"
	)
	# "m̀" is two characters!
	return re.sub("m̀", "m", py).translate(dictPyTrans)

def py_rm_tone(py):
	return re.sub(r"[1-5]$", "", py)

# Process related Unihan entries.

def py_proc_kHanyuPinlu(pys):
	return [py_u_to_v(py_rm_tone(
		re.match(r"([^0-9]+[1-5])\(([0-9]+)\)", py).group(1)
	)) for py in pys.split()]

def py_proc_kXHC1983(pys):
	return [py_rm_accent(py_u_to_v(re.search(r"(?<=:).*", py).group(0)))
		for py in pys.split()]

def py_proc_kHanyuPinyin(pyss):
	return [py_rm_accent(py_u_to_v(py)) for pys in pyss.split()
		for py in re.search("(?<=:).*", pys).group(0).split(",")]

def py_proc_kMandarin(pys):
	return [py_rm_accent(py_u_to_v(py)) for py in pys.split()]

def add_entry_info_to_dict(dictPy, unihanReadings, prop, py_proc):
	for (c, rawPys) in get_unihan_properties(prop, unihanReadings):
		if not c in dictPy and ord(c) >= 0x3400 and ord(c) <= 0x9FFF:
			dictPy[c] = set()
			dictPy[c].update(py_proc(rawPys))

# User interface.

def char_dict_gen(unihanReadings):
	dictPy = {}
	[add_entry_info_to_dict(dictPy, unihanReadings, *args) for args in [
		("kHanyuPinlu", py_proc_kHanyuPinlu),
		("kXHC1983", py_proc_kXHC1983),
		("kHanyuPinyin", py_proc_kHanyuPinyin),
		("kMandarin", py_proc_kMandarin)
	]]
	return dictPy

