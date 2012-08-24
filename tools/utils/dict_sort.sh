#!/bin/bash

cat $1 | cut -d ' ' -f 1 | perl -nle 'print length' > tmp1
paste -d ' ' tmp1 $1 > tmp2
LC_COLLATE=zh_CN.UTF-8 sort -k1n -k3 -k2 tmp2 | cut -d ' ' -f 2- > $1
rm -f tmp1 tmp2

