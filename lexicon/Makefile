.PHONY: clean

all: dict.index

clean:
	$(RM) dict.sort dict.shrinked dict.index

dict.sort: dict.full
	python sort.py -f $^ -t dict.tmp
	uniq < dict.tmp > $@
	rm dict.tmp

dict.shrinked: dict.sort
	python shrink.py -f $^ -t $@

dict.index: dict.shrinked dict_head.utf8
	python add_id.py -f $^ -t $@
