.PHONY: clean

DATA_DIR=../data

all: $(DATA_DIR)/dict.utf8

clean:
	$(RM) $(DATA_DIR)/dict.sort $(DATA_DIR)/dict.shrinked $(DATA_DIR)/dict.utf8

$(DATA_DIR)/dict.sort: $(DATA_DIR)/dict.full
	python sort.py -f $^ -t dict.tmp
	uniq < dict.tmp > $@
	rm dict.tmp

$(DATA_DIR)/dict.shrinked: $(DATA_DIR)/dict.sort
	python shrink.py -f $^ -t $@

$(DATA_DIR)/dict.utf8: $(DATA_DIR)/dict.shrinked dict_head.utf8
	python add_id.py -f $^ -t $@

merge: $(DATA_DIR)/newords.utf8 $(DATA_DIR)/dict.full
	python merge.py -f $(DATA_DIR)/dict.full -n $(DATA_DIR)/newords.utf8 -t dict.tmp
	cat dict.tmp >> $(DATA_DIR)/dict.full
