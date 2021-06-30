#!/bin/bash

# python generate_wordcloud.py # (Run if not already done for department yearbook)

ROOT_DIR="collage_and_yearbook_personal/"
rm -rf $ROOT_DIR
mkdir $ROOT_DIR


echo "Creating personal yearbook directories..."
python personal_yb_collage_prep.py
echo "Creating personal yearbook directories... done"


echo "Generating collages..."
python collage/compose_collages_personal.py
echo "Generating collages... done"


echo "Generating personal yearbooks..."
python generate_personal_yb_latex.py > NUL
echo "Generating personal yearbooks... done"


echo "Merging pdfs..."
python merge_pdfs_personal_yb.py
echo "Merging pdfs... done"
