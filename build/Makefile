.PHONY: clean

install:
	cp -f ../tools/CRF++-0.53/python/.libs/_crfpp.so .
	cp -f ../tools/CRF++-0.53/python/crfpp.py .
	cp -f ../segment/tagging/*.py .
	cp -f ../lexicon/*.py .
	cp -f ../data/wordb.db .

clean:
	$(RM) newords.db
	$(RM) *.pyc
	$(RM) *.py

test: clean install
	python extract_word.py -i ../data/raw -o ./newords.db --verbose
