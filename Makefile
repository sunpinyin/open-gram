install:
	cp -f tools/CRF++-0.53/python/.libs/_crfpp.so build
	cp -f tools/CRF++-0.53/python/crfpp.py build
	cp -f segment/tagging/baseseg.py build
	cp -f segment/tagging/cleanup.py build
