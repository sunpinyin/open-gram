.PHONY: clean

DATA_DIR=../data

all: $(DATA_DIR)/dict.utf8

clean:
	$(RM) $(DATA_DIR)/dict.sort $(DATA_DIR)/dict.shrinked $(DATA_DIR)/dict.utf8


$(DATA_DIR)/dict.utf8: $(DATA_DIR)/dict.full dict_head.utf8
	python add_id.py -f $< -t $@

filter: $(DATA_DIR)/dict.new

$(DATA_DIR)/dict.new: $(DATA_DIR)/newords.utf8 $(DATA_DIR)/dict.full
	python merge.py -f $(DATA_DIR)/dict.full -n $(DATA_DIR)/newords.utf8 -t $(DATA_DIR)/dict.new

$(DATA_DIR)/dict.shrinked: $(DATA_DIR)/dict.new
	python shrink.py -f $^ -t $@

merge: $(DATA_DIR)/dict.full $(DATA_DIR)/dict.new
	cat $^ > dict.tmp
	mv dict.tmp $<

