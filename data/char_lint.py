#!/usr/bin/env python3

char_set= set()
term_set = set()

def parse_term_pinyin(pinyin):
    return pinyin.split('\'')

def append(word, pinyin_list):
    global char_set, term_set
    if len(word) == 1:
        for py in pinyin_list:
            char_set.add(word + py)
    else:
        for py in pinyin_list:
            for ch, ch_py in zip(word, parse_term_pinyin(py)):
                term_set.add((ch + ch_py, word))

def check():
    global char_set, term_set
    print('check if all single char in included...')
    for ch, term in term_set:
        # print 'checking %s' % ch.encode('utf8')
        if not ch in char_set:
            print('%s missing, in term %s' % (ch, term))
    print('done')

def parse_line(line):
    fields = line[:-1].split(' ')
    pylist = []
    for field in fields[1:]:
        pos = field.find(':')
        if pos < 0:
            pylist.append(field)
        else:
            pylist.append(field[:pos])
    return fields[0], pylist

def main():
    with open('dict.full', 'r', encoding='utf-8') as f:
        for line in f:
            term, pylist = parse_line(line)
            append(term, pylist)
    check()


if __name__ == '__main__':
    main()

