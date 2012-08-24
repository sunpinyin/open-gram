#!/usr/bin/python3 -OO
# coding=UTF-8

import re, sys

unihanReadings = "Unihan_Readings.txt"
dictInput = "/dev/stdin" if sys.argv[1] == '-' else sys.argv[1]
dictOutput = "/dev/stdout" if sys.argv[2] == '-' else sys.argv[2]
dictPy = {}

## Functions to process Unihan data.

def codepoint_to_chr(s):
	patcCodeptHdr = re.compile(r"^U\+")
	return chr(int(patcCodeptHdr.sub("", s), 16))

def get_unihan_properties(prop, fname):
	patLine = '\t'.join([r"(U\+[0-9A-F]+)", "(" + prop + ")", "([^\t]+)"])
	patcLine = re.compile("^" + patLine + "$")
	return map(
		(lambda ss: (codepoint_to_chr(ss[0]), ss[2])),
		[m.groups() for m in filter(
			(lambda x: x != None),
			map(patcLine.match, open(fname))
		)]
	)

def add_entry_info_to_dict(prop, py_proc):
	for (c, rawPys) in get_unihan_properties(prop, unihanReadings):
		if not c in dictPy and ord(c) < 0x20000:
			dictPy[c] = set()
			dictPy[c].update(py_proc(rawPys))

## Functions to process pinyin strings.

def py_translate(py):
	dictPyTrans = str.maketrans(
		"āáǎàōóǒòēéěèīíǐìūúǔùǖǘǚǜü", "aaaaooooeeeeiiiiuuuuuuuuu"
	)
	return py.translate(dictPyTrans)

def py_utov(py):
	patcUtoV = re.compile(r"([ln])[ǖǘǚǜü]")
	return patcUtoV.sub(r"\1v", py)

def py_rm_tone(py):
	patcPyTone = re.compile(r"[1-5]$")
	return patcPyTone.sub("", py)

## Process related Unihan entries.

def py_proc_kHanyuPinlu(pys):
	patcKHanyuPinlu = re.compile(r"([^0-9]+[1-5])\(([0-9]+)\)")
	return [py_utov(py_rm_tone(patcKHanyuPinlu.match(py).group(1)))
		for py in pys.split()]
add_entry_info_to_dict("kHanyuPinlu", py_proc_kHanyuPinlu)

def py_proc_kXHC1983(pys):
	patcKHanyuPinyin = re.compile(r"(?<=:).*")
	return [py_translate(py_utov(patcKHanyuPinyin.search(py).group(0)))
		for py in pys.split()]
add_entry_info_to_dict("kXHC1983", py_proc_kXHC1983)

def py_proc_kHanyuPinyin(pyss):
	patcKHanyuPinyin = re.compile(r"(?<=:).*")
	return [py_translate(py_utov(py)) for pys in pyss.split()
		for py in patcKHanyuPinyin.search(pys).group(0).split(',')]
add_entry_info_to_dict("kHanyuPinyin", py_proc_kHanyuPinyin)

## Format dictPy to output.

def fmt_chr_info(c, idx):
	return ' '.join([c, str(idx)] + [py for py in dictPy[c]])

patcPercent = re.compile(r"%")
with open(dictOutput, "w") as outputFile:
	for l in open(dictInput):
		if len(l) == 0:
			continue
		c = l.split()[0]
		idx = int(l.split()[1])
		if len(c) == 1 and c in dictPy and not patcPercent.search(l):
			outputFile.write(fmt_chr_info(c, idx) + "\n")
		else:
			outputFile.write(l)
		if c in dictPy:
			dictPy.pop(c)
	for c in dictPy:
		idx += 1
		outputFile.write(fmt_chr_info(c, idx) + "\n")

