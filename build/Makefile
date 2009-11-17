.PHONY: clean

install:
	cp -f ../tools/CRF++-0.53/python/.libs/_crfpp.so .
	cp -f ../tools/CRF++-0.53/python/crfpp.py .
	cp -f ../segment/tagging/*.py .
	cp -f ../lexicon/*.py .

clean:
	rm *.pyc
	rm *.py

test: clean install
	cp ../data/wordb.db .
	python extract_word.py -i ../data/raw --verbose
