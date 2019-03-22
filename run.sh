#!/bin/bash

set -e

OUTPUT_PATH=./data
rm -rf $OUTPUT_PATH
mkdir -p $OUTPUT_PATH

time scrapy runspider \
	--loglevel=INFO \
	-o $OUTPUT_PATH/festival-de-curitiba.csv \
	festival_cwb.py
