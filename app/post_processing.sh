#!/bin/bash

# Run if not already done for personal yearbook
# echo "Generating wordclouds..."
# python generate_wordcloud.py
# echo "Generating wordclouds... done"

echo "Fixing group pics"
python fix_collage.py
echo "Fixing group pics... done"

echo "Generating collages..."
ROOT_DIR="media/collage_and_yearbook/"
rm -rf $ROOT_DIR
mkdir $ROOT_DIR

departments=(
    chemical
    civil
    cse
    ee
    maths
    mech
    physics
    textile
    dbeb
)

for dept in ${departments[@]}; do
    if [ -d media/$dept ]; then
        cp -R media/$dept/temp $ROOT_DIR/$dept
    fi
done

python collage/compose_collages.py

for dept in ${departments[@]}; do
    if [ -d media/$dept ]; then
        mkdir $ROOT_DIR/$dept/collages/
        mv $ROOT_DIR/$dept/*.pdf $ROOT_DIR/$dept/collages/
        mv $ROOT_DIR/$dept/*.jpg $ROOT_DIR/$dept/collages/
    fi
done

echo "Generating collages... done"