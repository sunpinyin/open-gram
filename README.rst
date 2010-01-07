open-gram
=========

open-gram is a project tries to collect lexicon and build n-gram dataset for NLP in Chinese. This project tries to leverage existing open source resources like crfpp and CC-CEDICT.

open-gram includes 4 parts
  - corpus collection
  - segmentation
  - (new) word extraction
  - n-gram info counting

corpus collection
=================

1. crawl Chinese web sites using scrapy, grab the body HTML pages of them
2. proprocess the pages
   - detect the encoding
   - remove HTML tags and other stuff we are not interested in
   - split the text into sentences

segmentation
============

there two ways to segment tokens into words
   * tagging
   * matching

word extraction
===============


n-gram info counting
====================

