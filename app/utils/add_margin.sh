#!/bin/bash
set -e
if [[ -z $(which pdf-crop-margins) ]]; then
	pip3 install -q pdfCropMargins;
fi;
if [[ -z $(which units) ]]; then
	sudo apt install units
fi;

infile=$(realpath $1) 
outfile=$(realpath $2)
margin=${$3:-'6 mm'}
margin=$(units -t "$margin" "inch")

margin=$(echo $margin*72| bc)
echo "Margin: " $margin
rand_str=$(echo $RANDOM | md5sum | head -c 8)
tmpfile="/tmp/${rand_str}.pdf"
pdf-crop-margins -o $tmpfile -p 100 -a4 -$margin -$margin -$margin -$margin $infile
pdfjam --outfile $outfile --paper a4paper $tmpfile
